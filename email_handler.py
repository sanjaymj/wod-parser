import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class MailHandler:
    def __init__(self, subject, content):
        self.subject = subject
        self.content = content

    def send_email(self):
        msg = MIMEMultipart()
        msg["From"] = "crossfit.erlangen@gmail.com"
        msg["To"] = "sanjay.mj62@gmail.com,likithkrishna@gmail.com"
        msg["Subject"] = self.subject

        msg.attach(MIMEText(self.content, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        server.login("crossfit.erlangen@gmail.com", "@crossfitPass1")
        server.sendmail("crossfit.erlangen@gmail.com", msg["To"].split(","), msg.as_string())
        server.quit()