<div align="center">
<image src="https://github.com/k-arthik-r/Vaidhya/assets/111432615/15e13045-27eb-47bd-8d3e-00b7dc9cc64d"/>
</div>

------------------------

<div align="center">
  <a><img src="https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white"></a> &nbsp;
  <a><img src="https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E"></a> &nbsp;
  <a><img src="https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white"></a> &nbsp;
  <a><img src="https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white"></a> &nbsp;
  <a><img src="https://img.shields.io/badge/Tkinter-ff0000?style=for-the-badge&logo=python&logoColor=ffdd54" /></a> &nbsp;
  <a><img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54"></a> &nbsp;
  <a><img src="https://img.shields.io/badge/MongoDB_Atlas-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white"></a> &nbsp;
  <a><img src="https://img.shields.io/badge/google colab-F9AB00?style=for-the-badge&logo=googlecolab&logoColor=white"></a> &nbsp;
  <a><img src="https://custom-icon-badges.demolab.com/badge/Huggingface-FF9D00?style=for-the-badge&logo=huggingface-logo"></a> &nbsp;
  <a><img src="https://img.shields.io/badge/Llama 2-0467DF?style=for-the-badge&logo=meta&logoColor=white"></a> &nbsp;
  <a><img src="https://custom-icon-badges.demolab.com/badge/Mistral AI-000000?style=for-the-badge&logo=mistralai"></a> &nbsp;
  <a><img src="https://custom-icon-badges.demolab.com/badge/HKUNLP Instructor L-FFFFFF?style=for-the-badge&logo=hkunlp"></a> &nbsp;
  <a><img src="https://custom-icon-badges.demolab.com/badge/Transformer-gold?style=for-the-badge&logo=package&logoColor=black"></a> &nbsp;
  <a><img src="https://custom-icon-badges.demolab.com/badge/Langchain-FBEEE9?style=for-the-badge&logo=ln"></a> &nbsp;
  <a><img src="https://custom-icon-badges.demolab.com/badge/Samantara-FFFFFF?style=for-the-badge&logo=sam"></a> &nbsp;
  <a><img src="https://img.shields.io/badge/Cloudflare-F38020?style=for-the-badge&logo=Cloudflare&logoColor=white"></a> &nbsp;
  <a><img src="https://custom-icon-badges.demolab.com/badge/Random Forest-99EDC3?style=for-the-badge&logo=randforest"></a> &nbsp;
  <a><img src="https://custom-icon-badges.demolab.com/badge/SMTP MIME-FBEC5D?style=for-the-badge&logo=server-smtp"></a> &nbsp;
  <a><img src="https://img.shields.io/badge/Canva-%2300C4CC.svg?style=for-the-badge&logo=Canva&logoColor=white"></a> &nbsp;
  
</div>

------------------------

Vaidhya is a mental healthcare assistance platform designed to facilitate secure and seamless interactions between patients and doctors. It offers a user-friendly environment where patients can access mental health support, book appointments, and receive personalized care, while doctors can manage patient reports and appointments efficiently. Vaidhya aims to enhance the overall mental health management experience through innovative and secure solutions.

The Project Focuss on 6 Mental Abnormalities, namely:
- Depression
- Anxiety Disorder
- Schizophrenia
- Bipolar Disorder
- Obsessive-Compulsive Disorder (OCD)
- Post-Traumatic Stress Disorder (PTSD)
  
------------------------

## Requirements
Python

<a href="https://www.python.org/downloads/release/python-3913/" alt="python">
        <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" /></a>

<br>
<br>

Mongo DB Atlas Account(To Save data in cloud) or Mongo DB Compass(To Save the Data Locally)

<a href="https://www.mongodb.com/" alt="mongo">
      <img src="https://img.shields.io/badge/MongoDB_Atlas-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white"></a>
        
<br>
<br>

App Password from your Google Account(To Connect and Send Mails through MIEME(SMTP))

<a href="https://www.google.co.in/" alt="mongo">
      <img src="https://img.shields.io/badge/google-4285F4?style=for-the-badge&logo=google&logoColor=white"></a>

--------------------

## Modules/Libraries Used

All The Modules/Libraries Used in the Project can be installed using [requirements.txt](requirements.txt)

- Flask
- Pymongo
- requests
- joblib
- smtplib
- pandas
- configparser 
- email.mime.text 
- email.mime.multipart
- docx
- datetime 
- os
- random

--------------------

## Setup

### Database
Use the Database Configuration File to Setup all the Collections with the name given in the Document.
<br>
- Database Name: Vaidhya
- Total Number of Collections: 12

<br>

You can Access the Document [Here](database_configuration.pdf)
<br>
Add your Mongo DB Connection String [Here](config.ini)

<br>

### Google App Password
create a google app password for the google account from which other rescive all mails.

- SENDER_EMAIL -> Source Mail Address.
- SENDER_PASSWORD -> App Password Corresponding to the Source Mail Address.
- RECEIVER_EMAIL -> Maild ID which receives responses from contact us section in About Page.

Add all these Data [Here](config.ini)

<br>

### Coloab URLS
Add the Corresponding Chatbot, Translation, Feeing Expressor Endpoints [Here](config.ini)

<br>

### Flask Secret Key
Add a Custom made FLASK APP SECRET KEY [Here](config.ini)

--------------------------
## How to Run?

- Intialize a Git Repository.
  
```bash
  git init
```

- Clone the Current Git Repository.
  
```bash
  git clone https://github.com/Mukuta-Manit-D/Vaidhya.git
```

- Crete a Virtual Environment named env and Activate it(PowerShell)
  
```bash
  python -m venv env

  .\env\Scripts\Activate.ps1
```

- Install all the Modules Present in [requirements](requirements.txt)
  
```bash
  pip install -r requirements.txt
```

- Comeplete the Above setup phase and add all the required credentials in [config.ini](config.ini)

  
```bash
  python app.py
```


-------------------------

## Architecture

![vaidhya_archetecture drawio](https://github.com/k-arthik-r/Vaidhya/assets/111432615/d000cdb0-e798-4e55-a464-86591686b673)

You can find the Editable Archetecture Copy [Here](Architecture/vaidhya_architecture.drawio)


-------------------------

## Working

The Entire Project is Divided into 2 Parts:
- Patient's Interface
- Doctor's Interface

### Patient's Interface

#### Patient Login Page

Features:
- Input fields for username and password to authenticate the patient.
- Links for creating a new account and resetting the password.
- Language selection dropdown to accommodate other languages.
- Navigation link to the About Page.

<br>
  
#### Account Management

Create New Account:
- Form to collect user details including name, email, password, and other necessary information.
- Email verification step for account activation.

Reset Password:
- Email-based password reset link or security question-based password reset option.

<br>
  
#### Patient Dashboard

Features:
- Access to the Helpline Chatbot for immediate support and inquiries.
- Disease Prediction section where patients can undergo tests to predict their mental state.
- Feeling Submission section to schedule appointments based on the user's emotional state.
- Display upcoming appointments and recent interactions with doctors.

<br>
  
#### Test Page

Features:
- A set of 10 scenario-based questions to help predict the patient's mental state.
- Immediate feedback or result based on the responses.

<br>
  
#### Feel Page

Features:
- Powered by a Language Model (LLM) to classify and interpret the patient's feelings.
- Predicts the mental state based on the submitted feelings.
- Option to schedule an appointment with a doctor based on the assessment.
  
<br>
<br>

### Doctor's Interface

#### Doctor Login Page

Features:
- Input fields for username and password to authenticate the doctor.
- Links for creating a new account and resetting the password.
- Language selection dropdown to accommodate multiple languages.
- Navigation link to the About Page.

<br>
  
#### Account Management

Create New Account:
- Form to collect user details including name, email, password, licence, and other necessary information.
- Email verification step for account activation.

Reset Password:
- Email-based password reset link or security question-based password reset option.

<br>

#### Doctor Dashboard

Features:
- View and manage patient reports.
- Offer and manage appointments based on predefined slots and custom availability.
- Access to patient interactions and historical data.

<br>

#### Report Page

Features:
- Fetch patient report using patient ID and doctor access key (constructed as: doctor id + first 2 letters of doctor's name in lowercase).
- Download patient reports in a pre-defined template for record-keeping and analysis.

<br>
  
#### Appointment Page

Features:
- Offer appointments in predefined time slots.
- Option to set one custom slot based on the doctor's availability.
- View and manage scheduled appointments.

------------------------------

## Working - Admin
Admin is a tkinter application which is made an exe file capable of being installed on a system. 
3 Features of Admin:
- Able to Delete Patient Records.
- Able to Delete Doctor Records.
- Maps Doctor with the Patient (Needs to be manually Done Via Admin.)

Both Patients and Doctor would not have the direct authority to delete their account, insted they need to mail admin in order to delete. 

------------------------------

## Google Colab URL's

### Chatbot
The ChatBot is a Model used to answer user Query. you can access the  document Used to Answer User Question [Here](chatbot_document.pdf). 

RAG Implementation:
- Storage: T4 GPU Disk(Online)
- Framework: Langchain
- Generative Model: meta-llama/Llama-3.2-3B
- Embedding Model: hkunlp/instructor-large
- Retriever: RetrievalQA
- connection: ngrok

#### Multilingual System
- Dataset: Samanantar
- Base Model: Helsinki-NLP
- connection: ngrok

#### Feeling Predictor
- Model: mistralai/Mistral-7B-Instruct-v0.2
- connection: ngrok

You can contact us for all the colab files @ voidex.developer@gmail.com

------------------------------

## Key Features
- Mental Health Prediction and Diagnosis Based on Tests and Felling Analysis.
- Proactive and Advance Chat-Bots to help the Users.
- Multingual Support to Diversify the Usage of the System.
- Doctor Appointment System.
- Personalized Treatment Recommendations.
- Real-time Monitoring and Updates.
- 100% API Free Infrastructure.
- Use of Large Language Models (LLMs).
- The Database used to Manage the data of the Medix is MongoDB Atlas, a Cloud storage service. One of the advantage of such is that multiple users can manipulate data from different places simutaneously.

-------------------------

## Important Notes:
- Each of the endpoint in the flask application is associated with an error code located at the first line of its function definition, which are showed in the Error 500 Page to locate which function is causing the applicarion to fail. The List of Endpoints and corresponding error codes can be located [Here](error_codes.xlsx)
  

----------------------------

## Feedback
If you have any feedback, please reach out to us at mukutamanitd6@gmail.com .
