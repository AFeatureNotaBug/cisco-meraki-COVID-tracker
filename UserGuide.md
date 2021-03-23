# Meraki Dashboard User Guide
The following guide attempts to generalise the installation and setup process of the Meraki Dashboard application in order for users to setup the web app with their own hardware. It is important to note that the project was specially desgined and developed on the recommended hardware below, and users may find that the functionality may not be the same on their own hardware.

## Recommended Hardware
Below is a list of hardware that the team used when designing the project. (Note: You will also require a Meraki license in order to use the hardware):
#### Hardware
- 6 Meraki MR30H Cloud Managed Access Points (MR30H-HW)
- 3 Meraki MV12 Mini Dome HD Cameras (MV12N-HW)
- 6 Meraki 802.3at PoE Injector (MA-INJ-4-UK)
- 16 Ethernet Cables

#### Licenses
- 3 Meraki MV Enterprise License and Support
- 3 Meraki MR Enterprise License

## Required Software
- Python 3.6 or later
- Python requests library
- Django version 3.1 or later
- Meraki version 1.2.0 or later

The requirements for Python can be found on the [Python website](https://www.python.org/)

## Setup
### Setting up the Meraki account
- Register an account via the [Cisco Meraki Dashboard](https://account.meraki.com/login/new_account)  
- Create a network for your devices [[additional documentation from meraki](https://documentation.meraki.com/General_Administration/Organizations_and_Networks/Creating_and_Deleting_Dashboard_Networks)]
- Claim your Meraki Devices by going to 'Organisation' -> 'Inventory' -> 'Claim' and typing in the serial numbers of the devices you would like to use
- Configure your SSID for each device in a manor that you think is appropriate, it is recommended to use a password protected private network (WPA2-PSK).
- You can now plug in the hardware

### Setting up the Hardware
- To connect the access points, plug the PoE Injector into a outlet power socket, plug an ethernet connection into the 'Data In' and connect via ethernet an access point to the 'Data & Power Out', repeat this for the other access points.   
- To connect a camera, from the powered ethernet output on an access point (labeled 1 and has a thunderbolt next to it, indicating power) connect via ethernet to the ethernet socket on the camera.

### Final steps
- Via the Cisco Meraki Dashboard go to Wireless -> Port profiles and create a profile with the first port enabled and select the SSID you previously created. Apply this profile to all the access points that are connected to cameras.
- The hardware should auto-connect and update the firmware in a few minutes.

[Helpful YouTube video](https://www.youtube.com/watch?v=uI7AUpQIWco&t=451s)


### Optional: Creating a Virtual Environment


### Initialising the Database
The database must be created before the web app can be used. The default supported database in Django is SQLite, the following instructions relate to the default SQLite database.


After navigating to the cisco\_dashboard folder, or the folder containing the "manage.py" file, the first step is to create the database and migrations for the database as the database does not currently exist. The database and migrations can be created by running the command ```python manage.py makemigrations```. This command will update the database in order to apply the most recent changes to the Models.py file. Assuming that the migrations in the folder cisco\_dashboard/main/migrations/ folder are up to date, the output should read "No changes detected".


Next, these migrations must be applied using the command ```python manage.py migrate```. If this command fails, the command ```python manage.py migrate --run-syncdb ``` may work but is not recommended.

### Running the Web App
The web app can be run and hosted locally by navigating to the cisco\_dashboard folder, or the folder containing the "manage.py" file, and using the command ```python manage.py runserver```. You may wish to test that the code will execute successfully, in which case use the command ```python manage.py test```, the output should read "OK" if all tests were passed, or it will indicate which of the tests has failed.


### Using the Web App
If the command ```python manage.py runserver``` executes successfully, you may navigate to the URL "127.0.0.1:8000" by default in order to view the web app when hosted locally.

From here you may wish to register an account with your Meraki API key. Guidance on allowing API access and generating an API key for your Meraki Dashboard can be found [here](https://documentation.meraki.com/General_Administration/Other_Topics/Cisco_Meraki_Dashboard_API) ```IMAGE FOR ACCOUNT CREATION HERE```

After creating an account and logging in, the overview page will be populated with your Meraki organisation details once visited. Initial load times may be slow, this is due to the system populating the database with all obtainable Meraki details based on your API key, on later visits to the overview page these details will be updated and load times will be much shorter. ```IMAGE OF POPULATED OVERVIEW PAGE```.

### Collision Detection
```IMAGE OF SCANNING API URL INPUT BOX``` ```DETAILS ABOUT SETTING UP LISTENING SERVER``` Once the listening server is created, the URL can be entered into the field on the Overview page which will then populate the database with details of device positions.

When devices are detected as being within two metres of one another, a minor alert will be flagged in the system and a relevant camera will be checked to see if it has detected people within two metres of one another. If the camera has detected two or more people within two metres of one another, the alert will be moved into the "major alerts" category and a picture will be grabbed from the camera. If the camera has not detected two or more people within two metres of one another, the alert will remain in the "minor alerts" category.

Alerts, as described above, may be viewed on the Alerts page. ```IMAGE OF ALERTS PAGE```




