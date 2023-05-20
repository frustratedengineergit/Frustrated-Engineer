from django.db import models

class EmailMessage(models.Model):
    subject = models.CharField(max_length=200)
    message = models.TextField()
