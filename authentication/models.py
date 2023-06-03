from django.db import models
from django.contrib.auth.models import User
from djongo import models as djongo_models

class MemberDetail(models.Model):
    _id = djongo_models.ObjectIdField(primary_key=True, db_column='_id')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    # Add other fields as needed

    def __str__(self):
        return self.user.username
