from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True) #El campo puede quedar como un espacio en blanco
    created = models.DateTimeField(auto_now_add=True)#Fecha automatica, no se especifica
    datecompleted = models.DateTimeField(null=True, blank=True)#El campo puede quedar vacío en la base de datos y en la consola de Admin
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)#Llave foranea

    def __str__(self):
        return self.title + '- de '+ self.user.username

