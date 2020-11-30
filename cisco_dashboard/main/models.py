"""Django database models file
 *  - Organisation Model   - Stores details of organisations retrieved from API
 *  - Network Model        - Stores details of networks under organisations
 *  - UserProfile Model    - Stores user account details
 *  - Device Model         - Stores details of devices retrieved using Networks
"""

# The below line disables an error caused due to Django formatting
# pylint: disable=E:101


from django.db import models
from django.contrib.auth.models import User
#from django.db.models.signals import post_save
#from django.dispatch import receiver
from django.template.defaultfilters import slugify


class Organisation(models.Model):
    """Stores details of organisations retrieved from API calls
     *  - orgID     - The organisations unique ID
     *  - orgName   - Name given to the organisation
     *  - orgURL    - URL of the organisations Cisco dashboard
    """
    orgID   = models.CharField(max_length = 200)
    orgName = models.CharField(max_length = 200)
    orgURL  = models.CharField(max_length = 200)
    apikey = models.CharField(max_length=200)
    #orgAPIOverview = models.JSONField(default=list)

    slug    = models.SlugField(unique = True, default = "")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.orgID)
        super().save(*args, **kwargs)


class Network(models.Model):
    """Stores details of networks retrieved from API calls using Organisations
     *  - org       - Organisation that this Network belongs to
     *  - netID     - Network's unique ID
     *  - netName   - Name given to this network
    """
    org     = models.ForeignKey(Organisation, on_delete = models.CASCADE)

    netID   = models.CharField(max_length = 200)
    netName = models.CharField(max_length = 200)

    slug    = models.SlugField(unique = True, default = "")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.netID)
        super().save(*args, **kwargs)


class UserProfile(models.Model):
    """Stores user details
     *  - user      - Links UserProfile to User model instance
     *  - apikey    - User's Cisco Meraki API key
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    apikey = models.CharField(max_length=128, unique=False,default=None)
    # The additional attributes we wish to include.

    def __str__(self):
        return self.user.username


class Device(models.Model):
    """Stores details of devices on a Network
     *  - net   - The Network that this Device belongs to
     *  - devAddr - Device's address
     *  - devSerial - Device's serial number
     *  - devMac    - Device's hardware address
     *  - devModel  - Model number of device
     *  - devLat    - Latitude of device
     *  - devLong   - Longitude of device
    """
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
        super().save(*args, **kwargs)
