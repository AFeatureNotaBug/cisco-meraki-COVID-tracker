from django.db import models
from django.contrib.auth.models import User


from django.template.defaultfilters import slugify


# Create your models here.
class Organisation(models.Model):
    orgID   = models.CharField(max_length = 200)
    orgName = models.CharField(max_length = 200)
    orgURL  = models.CharField(max_length = 200)
    
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
    # The additional attributes we wish to include.

    def __str__(self):
        return self.user.username