# CS11 Team Project - Cisco Meraki Dashboard
## Contributors
| Name | Role | Email |
| ------ | ------ | ------ |
| Johnathan Dominick Sciallo | Checker | 2326843s@student.gla.ac.uk |
| Fraser Dale | Demonstrator | 2387625d@student.gla.ac.uk |
| Jake Haakanson | Note Taker | 2407682H@student.gla.ac.uk |
| Ruofan Guo | Checker | 2431011g@student.gla.ac.uk |
| Ben Lynch | Meeting Chair | 2381564l@student.gla.ac.uk |
| Ollie Gardner | Team Coach | 2310049G@student.gla.ac.uk |

## Project Overview
Cisco Systems is a California-based multinational technology company well known for its contributions to networking technology. Meraki, a cloud-managed IT company, was acquired by Cisco Systems in 2012 as part of their cloud networking group. Cisco Meraki's cloud architecture allows users and businesses to create and deploy secure and scalable networks that can be managed from anywhere.

The aims of the project were seperated into two phases:
- The first phase was to use existing Cisco Meraki hardware and APIs in order to create an analytics dashboard for non-technical users to gain insight into the health and activity of their networks
- The goals of the second phase were for the team to decide. Based on the outcome of the first phase and the COVID-19 global pandemic, the team decided to use the capabilities of the hardware they were provided with in order to create a notification system that ensures users of the network are complying with social distancing measures.

Throughout the project, the team used Microsoft Teams as their communications platform as this was provided by the university. Initially the clients communicated with the team through Microsoft Teams, but later into the project team-client communications were moved to Cisco's Webex Teams as this was the client's preferred platform.

Issues and their priorities and associated risks were determined by the team on customer days, days where project progress was documented and displayed to the client and a member of university staff, and then documented on Gitlab. The discussion of tasks, priorities, and risks were held with the client in order for them to both gain more insight into how the team was interacting with their hardware and APIs, and also for the client to have more input into how the project developed.

## Functionality and Features
- Support for unique user profiles with Cisco Meraki API key functionality
- Overview of organisations and networks using Cisco Meraki API
- Device detection on network access points
- Device location detection
- Alerts system when devices become too close*
- Camera detection of people in frame
- Camera image capturing and storage functionality

*For the collision detection functionality to work, a listening server must be set up in order to interface with the Scanning API listed below. Details of how to set up a listening server can be found in the [User Guide](UserGuide.md)

## Technologies Used
- [Python version 3.6 and later](https://www.python.org/)
    - The Python requests library
- [Django version 3.1.2](https://www.djangoproject.com/)
- [Pylint static analysis tool](https://www.pylint.org/)
- [Cisco Meraki API Python library version 1.2.0](https://developer.cisco.com/meraki/api-v1/#!python)
- [Cisco Meraki MV Sense Camera API](https://developer.cisco.com/meraki/mv-sense/)
- [Cisco Meraki Scanning API](https://documentation.meraki.com/MR/Monitoring_and_Reporting/Scanning_API)
- Cisco Meraki MR30H Cloud Managed Access Points
- Cisco Meraki MV12 Mini Dome Cameras
- Google cloud functions & Firestore

## User Guide
A guide detailing how users can set up the project on their own hardware can be found [here](UserGuide.md).

## Screenshots and Demonstrations
To begin using our application users will have to register and login to take advantage of all of its features.

Registration can be accessed by the appropriate link, displayed in the top right of the home page after launching the site.

![image](/uploads/8adab12951473c66f5edf6a165134315/image.png)

Following the highlighted link will lead to the page displayed below. In this demonstration example credentials have been provided for each image to to aid in the users understanding.
In this example we will use:
- Username: "userdemo"
- Email: "demo@demo.com"
- Password: "demopass"
- Apikey: "demoapikey"

 In practical use more appropriate credentials should be used to ensure the security of accounts. For the purposes of this demonstration we will not be providing a functional apikey during the registraion phase to avoid confusion, since this information can be updated after creating a profile.

![image](/uploads/5415b09aa1c0da0b0931923b2deb0ab0/image.png)

The user can now attempt to login. This process can be started by navigating to the login page using the appropriate link highlighted in the top right corner of the home page.

After successfully navigating to the login page the user can then enter their credentials. An example of this using the registration demo credentials has been provided.

![image](/uploads/47f52beb9e4a6995fb4206b970d7323c/image.png)

Congratulations, you have successfully managed to register and login to the Cisco Meraki Dashboard.

![image](/uploads/c5e0046c3e18b773bece7349c23d0aab/image.png)
