import pandas as pd
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import PRAG_PHISHING, PRAG_SUMNJIVO
from sender_checker import provjeri_posiljatelja
from language_checker import provjeri_jezik
from url_checker import provjeri_urlove


def ucitaj_dataset():
    df = pd.read_excel("data/phishing_dataset.xlsx")
    print(f"Učitano {len(df)} emailova")
    print(f"Stupci: {list(df.columns)}")
    return df


def odredi_klasifikaciju(ukupni_bodovi):
    if ukupni_bodovi >= PRAG_PHISHING:
        return "PHISHING"
    elif ukupni_bodovi >= PRAG_SUMNJIVO:
        return "SUMNJIVO"
    return "LEGITIMNO"


def analiziraj_email(row):
    from_adresa = str(row.get("sender", ""))
    subject = str(row.get("subject", ""))
    body = str(row.get("email_text", ""))
    reply_to = ""

    rezultat_posiljatelja = provjeri_posiljatelja(from_adresa, reply_to)
    rezultat_jezika = provjeri_jezik(subject, body)
    rezultat_urlova = provjeri_urlove(subject, body)

    ukupni_bodovi = (
        rezultat_posiljatelja["bodovi"] +
        rezultat_jezika["bodovi"] +
        rezultat_urlova["bodovi"]
    )

    label_raw = str(row.get("label", "legitimate")).lower()
    stvarna_oznaka = 1 if "phishing" in label_raw else 0

    return {
        "subject": subject[:50],
        "ukupni_bodovi": ukupni_bodovi,
        "klasifikacija": odredi_klasifikaciju(ukupni_bodovi),
        "stvarna_oznaka": stvarna_oznaka
    }


def izracunaj_metriku(rezultati):
    tp = sum(1 for r in rezultati if r["klasifikacija"] in ["PHISHING", "SUMNJIVO"] and r["stvarna_oznaka"] == 1)
    tn = sum(1 for r in rezultati if r["klasifikacija"] == "LEGITIMNO" and r["stvarna_oznaka"] == 0)
    fp = sum(1 for r in rezultati if r["klasifikacija"] in ["PHISHING", "SUMNJIVO"] and r["stvarna_oznaka"] == 0)
    fn = sum(1 for r in rezultati if r["klasifikacija"] == "LEGITIMNO" and r["stvarna_oznaka"] == 1)

    ukupno = len(rezultati)
    tocnost = (tp + tn) / ukupno * 100 if ukupno > 0 else 0
    stopa_detekcije = tp / (tp + fn) * 100 if (tp + fn) > 0 else 0
    lazno_pozitivni = fp / (fp + tn) * 100 if (fp + tn) > 0 else 0
    lazno_negativni = fn / (tp + fn) * 100 if (tp + fn) > 0 else 0

    print("\n" + "=" * 50)
    print("REZULTATI EVALUACIJE")
    print("=" * 50)
    print(f"Ukupno emailova:  {ukupno}")
    print(f"Točnost:          {tocnost:.1f}%")
    print(f"Stopa detekcije:  {stopa_detekcije:.1f}%")
    print(f"Lažno pozitivni:  {lazno_pozitivni:.1f}%")
    print(f"Lažno negativni:  {lazno_negativni:.1f}%")
    print(f"TP: {tp}, TN: {tn}, FP: {fp}, FN: {fn}")


def spremi_rezultate(rezultati):
    putanja = "results/evaluacija.csv"
    with open(putanja, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "subject", "ukupni_bodovi", "klasifikacija", "stvarna_oznaka"
        ])
        writer.writeheader()
        writer.writerows(rezultati)
    print(f"\nRezultati spremljeni u {putanja}")


def pokreni_evaluaciju():
    df = ucitaj_dataset()

    rezultati = []
    for i, row in df.iterrows():
        rezultat = analiziraj_email(row)
        rezultati.append(rezultat)

        if (i + 1) % 100 == 0:
            print(f"Analizirano {i + 1}/{len(df)} emailova...")

    phishing_primjeri = [r for r in rezultati if r["stvarna_oznaka"] == 1][:3]
    print("\nPrimjeri phishing emailova:")
    for p in phishing_primjeri:
        print(f"  Subject: {p['subject']}")
        print(f"  Bodovi: {p['ukupni_bodovi']}")
        print(f"  Klasifikacija: {p['klasifikacija']}")
        print()

    izracunaj_metriku(rezultati)
    spremi_rezultate(rezultati)


if __name__ == "__main__":
    pokreni_evaluaciju()