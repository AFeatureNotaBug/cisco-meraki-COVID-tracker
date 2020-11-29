from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.template.defaultfilters import slugify


# Create your models here.
class Organisation(models.Model):
    orgID   = models.CharField(max_length = 200)
    orgName = models.CharField(max_length = 200)
    orgURL  = models.CharField(max_length = 200)
    apikey = models.CharField(max_length=200)
    #orgAPIOverview = models.JSONField(default=list)
    
    slug    = models.SlugField(unique = True, default = "")
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.orgID)
        super(Organisation, self).save(*args, **kwargs)


class Network(models.Model):
    org     = models.ForeignKey(Organisation, on_delete = models.CASCADE)
    
    netID   = models.CharField(max_length = 200)
    netName = models.CharField(max_length = 200)
    
    slug    = models.SlugField(unique = True, default = "")
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.netID)
        super(Network, self).save(*args, **kwargs)

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    apikey = models.CharField(max_length=128, unique=False,default=None)
    # The additional attributes we wish to include.
    
    def __str__(self):
        return self.user.username
        

class Device(models.Model):
    net       = models.ForeignKey(Network, on_delete = models.CASCADE)
    
    #devName   = models.CharField(max_length = 200)
    #devNotes  = models.CharField(max_length = 200)
    devAddr   = models.CharField(max_length = 200)
    
    devSerial = models.CharField(max_length = 200)
    devMac    = models.CharField(max_length = 200)
    devModel  = models.CharField(max_length = 200)
    #devLanIP  = models.CharField(max_length = 200)
    
    devLat    = models.FloatField()
    devLong   = models.FloatField()
    
    slug      = models.SlugField(unique = True, default = "")
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.devMac)
        super(Device, self).save(*args, **kwargs)

