from django.db import models

# Create your models here.


class BPerson(models.Model):
    bperson_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=500, null=True, blank=True)
    phone = models.CharField(max_length=500, null=True, blank=True)
    name_set = models.TextField(null=True, blank=True)
    ads_amount = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return "{} - {}".format(self.name, self.phone)


class Ads(models.Model):
    ad_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=500, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    bperson_name = models.CharField(max_length=300, null=True, blank=True)
    phone = models.CharField(max_length=500, null=True, blank=True)
    price = models.CharField(max_length=50, blank=True)
    classification = models.CharField(max_length=500, blank=True)
    datetime = models.DateTimeField(null=True, blank=True)
    bperson = models.ForeignKey(
        BPerson, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return "{} - {}".format(self.title, self.content)
