import time

import RPi.GPIO as GPIO
import numpy as np

import cv2

from datetime import datetime

import os

import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


# Set up SMTP server
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = 'minor4377@gmail.com'
smtp_password = 'pcgowelawjnzvggh'

# Set up message
sender = 'Sender Email Id'
recipient = 'Recipient Email Id'
subject = 'Security Alert'
body = 'There is some activity in your home. Email sent from a Raspberry Pi. cam'



sensor = 4


GPIO.setmode(GPIO.BCM)

GPIO.setup(sensor, GPIO.IN, GPIO.PUD_DOWN)


previous_state = False

current_state = False


while True:

    previous_state = current_state

    current_state = GPIO.input(sensor)


    if current_state != previous_state:

        new_state = "HIGH" if current_state else "LOW"

        print("GPIO pin %s is %s" % (sensor, new_state))

        
        if current_state:

            cap = cv2.VideoCapture(0)

            ret, frame = cap.read()

            cap = cv2.VideoCapture(0)

    
            print ("Saving Photo")

            picname = datetime.now().strftime("%y-%m-%d-%H-%M")

            picname = picname+'.jpg'

            cv2.imwrite(picname,frame)

    
            print ("Sending email")
            # Create a multipart message object to hold the text and image parts
            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = recipient
            msg['Subject'] = subject

            # Add the text part to the message
            text = MIMEText(body)
            msg.attach(text)
            
            attach = picname

 
            # Open the image file and attach it to the message
            with open(attach, 'rb') as f:
                img = MIMEImage(f.read())
            img.add_header('Content-Disposition', 'attachment', filename='image.jpg')
            msg.attach(img)

            # Connect to SMTP server and send email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.sendmail(sender, recipient, msg.as_string())
                print('success')


  

            print ("Email Sent")

            os.remove(picname)

