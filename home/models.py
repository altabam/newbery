from django.db import models
from django.contrib.auth.models import Group

# Create your models here.


class Menu(models.Model):
    url = models.CharField(max_length=250, blank=False,unique=True)
    nombre = models.CharField(max_length=250,unique=True)

    # no es el mejor modo de retornar la URL pero es facil de entender :D
    def get_absolute_url(self):
        return "%s" % self.url 
        
    def __unicode__(self):
        return u'%s' % self.nombre

    def __str__(self):
      return f"{self.url} {self.nombre}"
    

class MenuGroup(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    groups = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
      return f"{self.menu} {self.groups}"


