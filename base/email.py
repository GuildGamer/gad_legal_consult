import smtplib
from .models import Session

qs = Session.objects.all().filter(sent=False)


server = smtplib.SMTP_SSL("smpt.gmail.com", 465)
server.login("tobi4steve@gmail.com", "password")
for user in qs:
    server.sendmail("tobi4steve@gmail.com",
                    user.email,
                    "Your booking was sucessful! await a response from Victor Momodu. cheers!")
server.quit()