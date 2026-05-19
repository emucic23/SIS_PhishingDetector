import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def pošalji_testni_email(from_adresa, reply_to, subject, body):
    poruka = MIMEMultipart()
    poruka["From"] = from_adresa
    poruka["To"] = "test@test.com"
    poruka["Subject"] = subject
    poruka["Reply-To"] = reply_to
    poruka.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("localhost", 1025) as server:
        server.sendmail(from_adresa, "test@test.com", poruka.as_string())
        print(f"Email poslan: {subject}")

# Test - lazni PayPal
pošalji_testni_email(
    from_adresa='"PayPal Support" <hacker@gmail.com>',
    reply_to="kradja@russia.ru",
    subject="Urgent: Your account is suspended!",
    body="Click here to verify: http://totally-fake.ru/login"
)