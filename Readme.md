# Malicious Beanstalk

## Intro
Malicious beanstalk is an application that can be used for privilege escalation in Beanstalk. It is most useful when IMDSv1 is enabled, you have admin in Beanstalk, and there are higher privileges associated with an available instance profile. 

There is some setup involved so you'll need to review the application code as you go through the steps below. 

## Step 1: Setup listener, payload, and hosting 
- Run `python3 listen.py` on your VPS 
- Setup a webhost to host your payload 
- Configure the application.py with associated settings 

## Step 2: Install Beanstalk Application
- zip the application folder and upload as a new application in beanstalk 
- Install the application in to beanstalk 
- Be sure to use the target instance profile during this phase
- This application is configured to use Python 3.11. If you change this, you need to adjust the Procfile accordingly. 

## Step 3: Profit 
- Should receive a shell if your payload is setup correctly 
- Should catch the EC2 instance profile role session token 
