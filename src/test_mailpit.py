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


# Test 1 - jezik + pošiljatelj
pošalji_testni_email(
    from_adresa='"PayPal Support" <hacker@gmail.com>',
    reply_to="kradja@russia.ru",
    subject="URGENT VERIFY ACCOUNT NOW!!!",
    body="""
    Dear user,

    Poštovani korisniče, your accout is suspended!!!
    Confrm your pasword immediatly.     Click now!!!
    free money winner limited time
    """
)

# Test 2 - sumnjivi URL-ovi
pošalji_testni_email(
    from_adresa='"Netflix Support" <support@netflix-verify.tk>',
    reply_to="support@netflix-verify.tk",
    subject="Your Netflix account needs verification",
    body="""
    Dear customer,

    Please verify your account by clicking:
    http://netflix-login.ru/verify
    
    Or visit: http://bit.ly/netflix-verify
    """
)

# Test 3 - legitimni email
pošalji_testni_email(
    from_adresa='"Google" <no-reply@google.com>',
    reply_to="no-reply@google.com",
    subject="Your Google account security update",
    body="""
    Hi,

    We updated your account security settings.
    No action required.

    The Google Team
    """
)