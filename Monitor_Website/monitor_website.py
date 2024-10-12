import requests
import smtplib
import os
import paramiko
import time
import schedule
from google.cloud import compute_v1

# get email username & passwd form env var
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

# send email to me
def send_notification(email_msg):
    print('Sending an email...')
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        msg = f"Subject: SITE DOWN\n{email_msg}"
        smtp.sendmail(EMAIL_ADDRESS,EMAIL_ADDRESS, msg)

# restart the server
def restart_server_and_app():
    client = compute_v1.InstancesClient()
    operation = client.reset(project="plated-course-434908-v4", zone="asia-southeast1-a", instance="jenkins-server")
    print(f"Rebooting instance")
    operation.result()
    print(f"Instance has been rebooted.")

    # restart the application
    while True:
        instance = client.get(project="plated-course-434908-v4", zone="asia-southeast1-a", instance="jenkins-server")
        if instance.status == 'RUNNING':
            time.sleep(20)
            restart_container()
            break

# restart the container
def restart_container():
    print('Restarting the application...')
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('34.87.48.210', username='jayce', key_filename='C:/Users/NC/.ssh/id_rsa')
    stdout = ssh.exec_command('docker start nginx')
    print(stdout.readlines())
    ssh.close()

# monitor the app status
def monitor_application():
    try:
        # website response
        response = requests.get('http://34.87.48.210:8081/')
        if response.status_code == 200:
            print('Application is running successfully!')
        else:
            print('Application is DOWN. Fix it!')
            send_notification(f"Application returned {response.status_code}")
            restart_container()

    except Exception as ex:
        # website not response
        print(f'Connection error happened: {ex}')
        send_notification("Application not accessible!!!")
        restart_server_and_app()

# check the web status every 5 mins
schedule.every(5).minutes.do(monitor_application)

while True:
    schedule.run_pending()