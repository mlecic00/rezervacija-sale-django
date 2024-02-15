from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    SALA_CHOICES = [
        ('sala1', 'sala1'),
        ('sala2', 'sala2'),
        ('sala3', 'sala3'),
        ('sala4', 'sala4'),
        ('sala5', 'sala5'),
        ('sala6', 'sala6'),
        ('sala7', 'sala7')
    ]
    sala = models.CharField(max_length=100, choices=SALA_CHOICES)
    dolazak = models.TimeField()
    odlazak = models.TimeField()
    datum = models.DateField()
    ime = models.ForeignKey(User, on_delete = models.CASCADE) #ako je user obrisan onda cemo obrisati i rezervacije od njega
    razlog = models.TextField()
    napomena = models.TextField()



    def __str__(self):
        return str(self.id)


    def get_absolute_url(self):
        return reverse("reservation-home")