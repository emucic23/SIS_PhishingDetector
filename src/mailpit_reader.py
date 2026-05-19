import requests
from language_checker import provjeri_jezik
from config import MAILPIT_API


def dohvati_mailove():
    url = f"{MAILPIT_API}/v1/messages"
    response = requests.get(url)
    response.raise_for_status()
    return response.json().get("messages", [])


def dohvati_mail(message_id):
    url = f"{MAILPIT_API}/v1/message/{message_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def izvuci_tekst_maila(mail):
    subject = mail.get("Subject", "")

    text_body = mail.get("Text", "")
    html_body = mail.get("HTML", "")

    body = text_body if text_body else html_body

    return subject, body


def analiziraj_mailove():
    poruke = dohvati_mailove()

    if not poruke:
        print("Nema mailova u Mailpitu.")
        return

    for poruka in poruke:
        message_id = poruka.get("ID")

        mail = dohvati_mail(message_id)
        subject, body = izvuci_tekst_maila(mail)

        rezultat = provjeri_jezik(subject, body)

        print("=" * 60)
        print("Subject:", subject)
        print("Language score:", rezultat["bodovi"])
        print("Sumnjivo:", rezultat["sumnjivo"])

        for indikator in rezultat["indikatori"]:
            print("-", indikator)


if __name__ == "__main__":
    analiziraj_mailove()