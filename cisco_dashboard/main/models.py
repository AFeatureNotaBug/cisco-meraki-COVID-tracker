"""Django database models file
 *  - Organisation Model   - Stores details of organisations retrieved from API
 *  - Network Model        - Stores details of networks under organisations
 *  - UserProfile Model    - Stores user account details
 *  - Device Model         - Stores details of devices retrieved using Networks
"""
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class Organisation(models.Model):
    """Stores details of organisations retrieved from API calls
     *  - orgID     - The organisations unique ID
     *  - orgName   - Name given to the organisation
     *  - orgURL    - URL of the organisations Cisco dashboard
    """
    org_id = models.CharField(max_length=200)
    org_name = models.CharField(max_length=200)
    org_url = models.CharField(max_length=200)
    apikey = models.CharField(max_length=200)

    slug = models.SlugField(unique=True, default="")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.org_id)
        super().save(*args, **kwargs)


class Network(models.Model):
    """Stores details of networks retrieved from API calls using Organisations
     *  - org       - Organisation that this Network belongs to
     *  - netID     - Network's unique ID
     *  - netName   - Name given to this network
     *  - scanningAPIURL    - get request URL for scanning api middle server
    """
    org = models.ForeignKey(Organisation, on_delete=models.CASCADE)

    net_id = models.CharField(max_length=200)
    net_name = models.CharField(max_length=200)

    slug = models.SlugField(unique=True, default="")
    scanningAPIURL = models.CharField(max_length=128, unique=False, default=None, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.net_id)
        super().save(*args, **kwargs)


class UserProfile(models.Model):
    """Stores user details
     *  - user      - Links UserProfile to User model instance
     *  - apikey    - User's Cisco Meraki API key
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    apikey = models.CharField(max_length=128, unique=False, default=None)

    def __str__(self):
        return self.user.username


class Device(models.Model):
    """Stores details of devices on a Network
     *  - net       - The Network that this Device belongs to
     *  - devAddr   - Device's address
     *  - devSerial - Device's serial number
     *  - devMac    - Device's hardware address
     *  - devModel  - Model number of device
     *  - devLat    - Latitude of device
     *  - devLong   - Longitude of device
    """
    net = models.ForeignKey(Network, on_delete=models.CASCADE)

    devAddr = models.CharField(max_length=200)
    devSerial = models.CharField(max_length=200)
    devMac = models.CharField(max_length=200)
    devModel = models.CharField(max_length=200)

    devLat = models.FloatField()
    devLong = models.FloatField()

    slug = models.SlugField(unique=True, default="")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.devMac)
        super().save(*args, **kwargs)


class Snapshot(models.Model):
    """Stores camera snapshots after collision detection
     *  - org   - Organisation the snapshot belongs to
     *  - url   - URL of the image
     *  - time  - time of collision
    """
    org  = models.ForeignKey(Organisation, on_delete = models.CASCADE)

    url  = models.CharField(max_length=500)
    time = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class AccessAlert(models.Model):
    """Stores access point alerts for devices within two metres
     *  - dev_type_1    - Type of one of the devices involved in the collision
     *  - dev_type_2    - Type of one other device involved in the collision
     *  - time          - Time that the collision was observed
    """
    org = models.ForeignKey(Organisation, on_delete = models.CASCADE)

    dev_type_1 = models.CharField(max_length = 50)
    dev_type_2 = models.CharField(max_length = 50)
    time       = models.CharField(max_length = 50)
    distance = models.CharField(max_length = 10,default=.1)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
