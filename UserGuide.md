# Meraki Dashboard User Guide
The following guide attempts to generalise the installation and setup process of the Meraki Dashboard application in order for users to setup the web app with their own hardware. It is important to note that the project was specially desgined and developed on the recommended hardware below, and users may find that the functionality may not be the same on their own hardware.

## Recommended Hardware
Below is a list of hardware that the team used when designing the project. (Note: You will also require a Meraki license in order to use the hardware):
- 6 Meraki MR30H Cloud Managed Access Points
- 3 Meraki MV12 Mini Dome Cameras

## Required Software
- Django version 3.1 or later
- Python 3.6 or later  

The requirements for Python can be found on the [Python website](https://www.python.org/)

## Setup
### Setting up the Hardware


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

After creating an account and logging in, the overview page will be populated with your Meraki organisation details once visited ```IMAGE OF POPULATED OVERVIEW PAGE```.




