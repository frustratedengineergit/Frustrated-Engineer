from django.db import models
from djongo import models as djongo_models

class ContactData(models.Model):
    _id = djongo_models.ObjectIdField(primary_key=True, db_column='_id')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.IntegerField()
    message = models.TextField()

    def __str__(self):
        return self.name
