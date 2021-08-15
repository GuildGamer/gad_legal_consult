import smtplib
from .models import Session

qs = Session.objects.all().filter(sent=False)


server = smtplib.SMTP_SSL("smpt.gmail.com", 465)
server.login("tobi4steve@gmail.com", "codingiScooL1")
for session_request in qs:
    server.sendmail("tobi4steve@gmail.com",
                    session_request.email,
                    "Your booking was sucessful! await a response from Victor Momodu. cheers!")

    session_request.sent = True
server.quit()