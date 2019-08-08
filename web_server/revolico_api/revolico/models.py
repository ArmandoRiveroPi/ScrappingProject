from django.db import models

# Create your models here.


class Ads(models.Model):
    ad_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=500)
    content = models.TextField()
    phone = models.CharField(max_length=500)

    def __str__(self):
        return "{} - {}".format(self.title, self.content)


class BPerson(models.Model):
    bperson_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=500)
    phone = models.CharField(max_length=500)

    def __str__(self):
        return "{} - {}".format(self.name, self.phone)
