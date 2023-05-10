from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):

    STATUS = (
        ('regular', 'regular'),
    )
    SEX_CHOICES = (
        ('H', 'Hombre'),
        ('M', 'Mujer'),
        ('ND', 'Prefiero no decirlo'),
    )

    CAREER_CHOICES = (
        ('M', 'Matemática'),
        ('F', 'Física'),
    )

    email = models.EmailField(unique=True)
    status = models.CharField(max_length=100, choices=STATUS, default='regular')
    description = models.TextField("Description", max_length=600, default='', blank=True)
    sex = models.CharField(max_length=2, choices=SEX_CHOICES, default='ND')
    career = models.CharField(max_length=1, choices=CAREER_CHOICES, blank=True, null=True)
    cui = models.CharField(max_length=13)

    def __str__(self):
        return self.username
