'''
Script for sending emails
'''

import smtplib
def send_email(full_name, email, time, content):
    server  = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login("gadlegalconsult@gmail.com", "GadLegali$live!")
    server.sendmail("gadlegalconsult@gmail.com",
                    "victormomodu25@gmail.com", 
                    f"{full_name} has booked a session at {time} with the following content: *{content}*. Please do well do  get back to them at {email}, Thank you. ")
    server.quit()
