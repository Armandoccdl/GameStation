#encoding:utf-8
from django.db import models

class Game(models.Model):
    name = models.CharField(max_length=100)
    platform = models.CharField(max_length=100)
    year_of_Release = models.IntegerField()
    genre = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    na_Sales = models.FloatField()
    eu_Sales = models.FloatField()
    jp_Sales = models.FloatField()
    other_Sales = models.FloatField()
    global_Sales = models.FloatField()
    critic_Score = models.FloatField()
    user_Score = models.FloatField()
    developer = models.CharField(max_length=100)
    rating = models.CharField(max_length=10)

    def __unicode__(self):
        return self.name


class Cluster(models.Model):
    numCluster = models.IntegerField()
    game = models.ForeignKey(Game)