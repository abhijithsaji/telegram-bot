from django.db import models

# Create your models here.


class UserDetails(models.Model):
    user_id = models.IntegerField(default=0)
    first_name = models.CharField(max_length=50)
    calls = models.IntegerField(default=0)


