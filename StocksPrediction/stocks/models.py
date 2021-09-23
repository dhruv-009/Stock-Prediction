from django.db import models

# Create your models here.


class Companies(models.Model):
    name = models.CharField(max_length=50)
    field = models.CharField(max_length=50)
    current_closed_price= models.CharField(max_length=100)
    type_of_investment = models.CharField(choices=(("safe","safe"),("risk","risk")),default="safe",max_length=100)
    company_id = models.IntegerField()

    def __str__(self):
        return self.name
