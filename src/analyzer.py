import sys
import requests
import time
import csv
import os
from config import MAILPIT_API, PRAG_PHISHING, PRAG_SUMNJIVO, PUTANJA_REZULTATI
from sender_checker import provjeri_posiljatelja
from language_checker import provjeri_jezik
from url_checker import provjeri_urlove

def dohvati_poruke():
    url = f"{MAILPIT_API}/v1/messages"
    odgovor = requests.get(url)
    odgovor.raise_for_status()
    return odgovor.json().get("messages", [])


def dohvati_poruku(message_id):
    url = f"{MAILPIT_API}/v1/message/{message_id}"
    odgovor = requests.get(url)
    odgovor.raise_for_status()
    return odgovor.json()


def odredi_klasifikaciju(ukupni_bodovi):
    if ukupni_bodovi >= PRAG_PHISHING:
        return "PHISHING"
    elif ukupni_bodovi >= PRAG_SUMNJIVO:
        return "SUMNJIVO"
    return "LEGITIMNO"


def analiziraj_poruku(poruka):
    message_id = poruka.get("ID")
    mail = dohvati_poruku(message_id)

    zaglavlje_from = mail.get("From", {})
    from_adresa = f'"{zaglavlje_from.get("Name", "")}" <{zaglavlje_from.get("Address", "")}>'

    reply_to_lista = mail.get("ReplyTo", [])
    reply_to = reply_to_lista[0].get("Address", "") if reply_to_lista else ""

    subject = mail.get("Subject", "")
    body = mail.get("Text", "") or mail.get("HTML", "")

    rezultat_posiljatelja = provjeri_posiljatelja(from_adresa, reply_to)
    rezultat_jezika = provjeri_jezik(subject, body)
    rezultat_urlova = provjeri_urlove(subject, body)
    ukupni_bodovi = rezultat_posiljatelja["bodovi"] + rezultat_jezika["bodovi"] + rezultat_urlova["bodovi"]
    klasifikacija = odredi_klasifikaciju(ukupni_bodovi)

    return {
        "id": message_id,
        "subject": subject,
        "from": from_adresa,
        "ukupni_bodovi": ukupni_bodovi,
        "klasifikacija": klasifikacija,
        "detalji_posiljatelja": rezultat_posiljatelja["objasnjenje"],
        "detalji_jezika": rezultat_jezika["indikatori"],
        "detalji_urlova": rezultat_urlova["indikatori"]
    }


def ispisi_rezultat(rezultat):
    print("=" * 60)
    print(f"Subject:      {rezultat['subject']}")
    print(f"Od:           {rezultat['from']}")
    print(f"Bodovi:       {rezultat['ukupni_bodovi']}")
    print(f"Klasifikacija: {rezultat['klasifikacija']}")
    print(f"Pošiljatelj:  {rezultat['detalji_posiljatelja']}")
    print(f"Jezik:        {rezultat['detalji_jezika']}")
    print(f"URL-ovi:       {rezultat['detalji_urlova']}")

def spremi_rezultat(rezultat):
    datoteka_postoji = os.path.exists(PUTANJA_REZULTATI)
    
    with open(PUTANJA_REZULTATI, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "id", "subject", "from", "ukupni_bodovi", 
            "klasifikacija", "detalji_posiljatelja", "detalji_jezika", "detalji_urlova"
        ])
        
        if not datoteka_postoji:
            writer.writeheader()
        
        writer.writerow(rezultat)

def pokreni():
    print("Analyzer pokrenut, čekam emailove...")
    analizirani = set()

    while True:
        poruke = dohvati_poruke()

        for poruka in poruke:
            message_id = poruka.get("ID")

            if message_id not in analizirani:
                rezultat = analiziraj_poruku(poruka)
                ispisi_rezultat(rezultat)
                spremi_rezultat(rezultat)
                analizirani.add(message_id)

        time.sleep(5)


if __name__ == "__main__":
    pokreni()