from django.db import models

# Create your models here.


class Ads(models.Model):
    # title
    title = models.CharField(max_length=500)
    # ad content
    content = models.TextField()

    def __str__(self):
        return "{} - {}".format(self.title, self.content)


class BPerson(models.Model):
    name = models.CharField(max_length=500)
    phone = models.CharField(max_length=500)

    def __str__(self):
        return "{} - {}".format(self.name, self.phone)
