'''
Script for sending emails
'''

from django.core.mail import send_mail
from django.conf import settings
import smtplib
import mimetypes
import email
import email.mime.application
def send_email(subject, message, recipient_list, send_ebook):
    email_from = settings.EMAIL_HOST_USER
    email_pass = settings.EMAIL_HOST_PASSWORD

    if send_ebook == True:

        msg = email.mime.multipart.MIMEMultipart()
        msg['Subject'] = "GLC EBOOK"
        msg['From'] = 'gadlegalconsult@gmail.com'
        msg['To'] = str(recipient_list[0])

        txt= email.mime.text.MIMEText('Enjoy your Ebook!')
        msg.attach(txt)
        ebook_dir = settings.EBOOK_DIR

        filename = ebook_dir
        fo=open(filename,'rb')
        file = email.mime.application.MIMEApplication(fo.read(),_subtype="pdf")
        fo.close()
        file.add_header('Content-Disposition','attachment',filename=filename)
        msg.attach(file)

        s = smtplib.SMTP('smtp.gmail.com')
        s.starttls()
        s.login(email_from,email_pass)
        s.sendmail(email_from, recipient_list, msg.as_string())
        s.quit()
    else:
        send_mail( subject, message, email_from, recipient_list ) 
