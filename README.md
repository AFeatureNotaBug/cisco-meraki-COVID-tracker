# Group CS11 Team Project - Cisco Meraki COVID Tracker
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
