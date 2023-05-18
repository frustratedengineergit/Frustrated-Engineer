from django.db import models

class ContactData(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.IntegerField()
    message = models.TextField()

    def __str__(self):
        return self.name
    