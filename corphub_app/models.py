from django.db import models

# Create your models here.
class SearchModel(models.Model):
    search = models.CharField(max_length=100)

    def __str__(self):
        return "Search Bar"
