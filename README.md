# A Learning Scraping Project

This a learning project to get familiar with several aspects of data science.

1. We scrap data from a collection (in disk) of html documents from the [Revolico](https://revolico.com) site,
   the most important classified ads site in Cuba. For that we use Python and in
   particular BeautifulSoup.

2. We clean and process this data. For instance, there is the field of phone numbers
   that each can input in a different way. We try to extract the properly formated
   number from that field with a set of regular expressions.

3. Revolico showcases a list of ads but not of users that created the ads, we
   build the list of users based on the assumption that ads with the same phone numbers
   can be ascribed to the same users. The name field is a lot less reliable than
   the phones.

4. We feed a transformed version of this data into a database for powering
   a django web app. The web app is built with the Django Rest Framework as
   a backend and VUEJS as the frontend.

## Where can the different parts of the code be found

The classes that support the tasks are in the `RevolicoProject` folder
while the tasks themselves are found in the `scripts` folder. In particular,
the more tried and tested scripts that perform the most important tasks
are in the `scripts/build_scripts`
folder, while in the `scripts/test_scripts` there is a variety of scripts
in different states.
