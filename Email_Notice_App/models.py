from django.db import models
from djongo import models as djongo_models

class EmailMessage(models.Model):
    _id = djongo_models.ObjectIdField(primary_key=True, db_column='_id')
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.subject