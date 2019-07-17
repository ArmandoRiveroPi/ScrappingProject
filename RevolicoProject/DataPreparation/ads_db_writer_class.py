import json
import itertools


class AdsDBWriter:
    """Handles the merging of duplicates adverts

    Depends on the criteria to consider ads to be duplicates
    Provides a DB of merged ads, given a DB of ads and a list of (preprocessed) ads
    Requires a list of ads and a DB accessor
    """

    def __init__(self, dbAccessor):
        self.db = dbAccessor

    def find_duplicate(self, ad):
        # search the db for an ad with the same title
        candidates = self.db.find_ads_by_title(ad['title'])
        # if you find an identical ad, return the duplicate
        for candidate in candidates:
            if self.are_ads_equal(ad, candidate):
                return candidate
        # when you don't find a duplicate
        return None

    def merge_ads(self, ad1, ad2):
        # Loop through adList merging the ad with the next
        # The merging includes
        #   - IDs (keep the first ad ID, but include other IDs in the ID list)
        #   - Datetimes (add the new Datetimes)
        #   - Classifications
        #   - Extra Data (find out how to merge JSONs)
        merged = ad1
        # merged['id'] = ad1['id']
        merged['classification'] = self.merge_list_fields(
            'classification', ad1, ad2)
        merged['extra_data'] = self.merge_json_fields('extra_data', ad1, ad2)

        return merged

    def merge_json_fields(self, jsonField, ad1, ad2):
        """Merges json fields (encoded as strings)

        Arguments:
            jsonField {string} -- name of the json field in the dicts
            ad1 {dict} -- dictionary 1
            ad2 {dict} -- dictionary 1

        Returns:
            string -- the resulting merged and encoded json field
        """
        if jsonField in ad1:
            dic1 = json.loads(ad1[jsonField])
        else:
            dic1 = {}

        if jsonField in ad2:
            dic2 = json.loads(ad2[jsonField])
        else:
            dic2 = {}

        result = {}
        fields = list(set(list(dic1.keys()) + list(dic2.keys())))
        for field in fields:
            result[field] = []
            if field in dic1:
                result[field].append(dic1[field])
            if field in dic2:
                result[field].append(dic2[field])
            result[field] = list(itertools.chain.from_iterable(result[field]))
            result[field] = list(set(result[field]))
        return json.dumps(result)

    def merge_list_fields(self, field, ad1, ad2):
        sep = ','
        if ad1[field] != ad2[field]:
            return sep.join([ad1[field], ad2[field]])
        else:
            return ad1[field]

    def are_ads_equal(self, ad1, ad2):
        # Check equality of some fields
        equalFields = ['title', 'content', 'user_phone', 'user_name']
        # If all of them are equal then return true
        text1 = ' '.join([ad1[field] for field in equalFields])
        text2 = ' '.join([ad2[field] for field in equalFields])
        return text1 == text2

    def write_ads(self, ads):
        for ad in ads:
            # Find if the ad has a duplicate
            duplicate = self.find_duplicate(ad)
            if duplicate:
                # If there's a duplicate add the data to the duplicate
                ad = self.merge_ads(duplicate, ad)
            self.db.write_ad(ad)
