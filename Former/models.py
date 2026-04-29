from django.db import models
from django.contrib.auth.models import User

class Register_Model(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='User_Photos/', blank=True, null=True)

    gender = models.CharField(
        max_length=1,
        choices=[
            ('M', 'Male'),
            ('F', 'Female'),
            ('O', 'Others'),
        ],
        blank=True,
        null=True
    )

    date_of_birth = models.DateField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name