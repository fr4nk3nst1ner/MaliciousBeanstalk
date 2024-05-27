# Malicious Beanstalk

## Introduction
Malicious Beanstalk is an application designed for privilege escalation within AWS Elastic Beanstalk. It requires admin access to deploy the application and leverages higher privileges associated with an available instance profile.

The idea is you obtain credentials that have permissions to deploy a Beanstalk application and there is an overly permissive Instance Profile (e.g., `AdministratorAccess`) that can be attached to an ec2 instance. 

There are two mechanisms that are involved with this script (application.py). If you choose to use one or the other but not both, you will need to update `application.py` accordingly. 

### Payload execution 

- A payload (e.g., [Poseidon](https://github.com/MythicAgents/poseidon) with [Mythic C2](https://github.com/its-a-feature/Mythic)) will need to be generated to be delivered and executed on the ec2 instance that is created 
- This will establish an interactive shell on the ec2 instance, for further testing 


### Exfiltration of ec2 Instance Profile Temporary Credentials 

- Risky method: if GuardDuty is enabled, it will default trigger an alert when Instance Profile creds are used outside the ec2 instance 
- Retrieves credentials from the following path: `http://169.254.169.254/latest/meta-data/iam/security-credentials/{iam_role_name}`
- You need to determine the target Instance Profile role to be used in the script for `{iam_role_name}` 
- The credential material is encrypted and sent to your listener using the 32-byte AES key 


Follow the steps below to set up and deploy Malicious Beanstalk. Ensure you review the application code as you proceed through each step.

## Step 1: Setup Listener, Payload, and Hosting

1. **Run Listener**: Start the listener on your VPS.
    ```bash
    python3 listen.py
    ```

2. **Setup Web Host**: Host your payload on a web server. Ensure it is accessible by the application.

3. **Configure Application**: Modify `application.py` with the necessary settings such as the URL of your hosted payload.

## Step 2: Install Beanstalk Application

1. **Zip Application Folder**: Compress the application folder into a zip file.
    ```bash
    zip -r malicious_beanstalk.zip application_folder/
    ```

2. **Upload and Deploy**: Upload the zipped application to AWS Elastic Beanstalk as a new application.

3. **Deploy to Target Instance Profile**: During the deployment phase, ensure you use the target instance profile with higher privileges.

4. **Python Version**: The application is configured to use Python 3.11. If you change the Python version, adjust the `Procfile` accordingly.

## Step 3: Gain Access

1. **Receive Shell**: If your payload is set up correctly, you should receive a shell on your listener.

2. **Capture Instance Profile Role Session Token**: You should be able to catch the EC2 instance profile role session token, which can be used for privilege escalation.

## Notes

- Ensure you have the necessary permissions and have reviewed AWS policies and security guidelines before using this application.
- This tool is for educational and authorized testing purposes only.


## To Do 

- [ ] Create interactive menu for generating `application.py` 
- [ ] Create functionality to create reverse shell with Netcat or Socat 
