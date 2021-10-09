from django.db import models


class Restroom(models.Model):
    # Set yelp_id max length to 100 based on this:
    # https://github.com/Yelp/yelp-fusion/issues/183
    yelp_id = models.CharField(max_length=100)
    rating = models.FloatField(default=0.0)
