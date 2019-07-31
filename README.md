# FaceAttendance

This is a face recognition based attendance system which is used to mark the attendance of students appearing in front of the camera. It stores the face image of the student by using the Enrolment button in the UI, and stores the 'Base64' encoding of the face, along the student name and roll number in the database.
The database used for this purpose is [MongoDB](https://docs.mongodb.com/)

## Requirements

* Python v3.6.5 or higher: Download from [here](https://www.python.org/downloads/release/python-360/)
* MongoDB for setting up database
* Web Camera
* HaarCascade

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required packages using the following command:

```bash
pip3 install -r requirements.txt
```

## Usage
Clone the repository using Git command:
```bash
git clone https://github.com/shreyak1911/FaceAttendance.git
```
For viewing the working of the model use:
```bash
python3 login.py
```
Create your credentials and use the same for login.

Tutorial for setting up of database can be found [here](https://www.tutorialspoint.com/mongodb/mongodb_create_database)


