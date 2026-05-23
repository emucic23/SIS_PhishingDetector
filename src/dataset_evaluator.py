import pandas as pd
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import PRAG_PHISHING, PRAG_SUMNJIVO, PUTANJA_DATASET, PUTANJA_REZULTATI
from sender_checker import provjeri_posiljatelja
from language_checker import provjeri_jezik
from url_checker import provjeri_urlove


def ucitaj_dataset():
    df = pd.read_csv(PUTANJA_DATASET)          
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
    body = str(row.get("body", ""))            
    reply_to = ""

    rezultat_posiljatelja = provjeri_posiljatelja(from_adresa, reply_to)
    rezultat_jezika = provjeri_jezik(subject, body)
    rezultat_urlova = provjeri_urlove(subject, body)

    ukupni_bodovi = (
        rezultat_posiljatelja["bodovi"] +
        rezultat_jezika["bodovi"] +
        rezultat_urlova["bodovi"]
    )

    stvarna_oznaka = int(row.get("label", 0))  

    return {
        "subject": subject[:50],
        "from": from_adresa[:50],
        "bodovi_posiljatelj": rezultat_posiljatelja["bodovi"],
        "bodovi_jezik": rezultat_jezika["bodovi"],
        "bodovi_url": rezultat_urlova["bodovi"],
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

    return {
        "tp": tp, "tn": tn, "fp": fp, "fn": fn,
        "tocnost": tocnost,
        "stopa_detekcije": stopa_detekcije,
        "lazno_pozitivni": lazno_pozitivni,
        "lazno_negativni": lazno_negativni
    }


def spremi_rezultate(rezultati):
    os.makedirs("results", exist_ok=True)
    putanja = "results/evaluacija.csv"
    with open(putanja, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "subject", "from", "bodovi_posiljatelj", "bodovi_jezik",
            "bodovi_url", "ukupni_bodovi", "klasifikacija", "stvarna_oznaka"
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

        if (i + 1) % 500 == 0:
            print(f"Analizirano {i + 1}/{len(df)} emailova...")

    # Primjeri phishing emailova
    print("\nPrimjeri phishing emailova:")
    phishing_primjeri = [r for r in rezultati if r["stvarna_oznaka"] == 1][:3]
    for p in phishing_primjeri:
        print(f"  Subject: {p['subject']}")
        print(f"  Bodovi:  {p['ukupni_bodovi']} (posiljatelj={p['bodovi_posiljatelj']}, jezik={p['bodovi_jezik']}, url={p['bodovi_url']})")
        print(f"  Klasifikacija: {p['klasifikacija']}")
        print()

    # Primjeri lažno pozitivnih (ham klasificiran kao phishing)
    print("Primjeri lažno pozitivnih (ham → PHISHING/SUMNJIVO):")
    fp_primjeri = [r for r in rezultati if r["klasifikacija"] in ["PHISHING", "SUMNJIVO"] and r["stvarna_oznaka"] == 0][:3]
    for p in fp_primjeri:
        print(f"  Subject: {p['subject']}")
        print(f"  Bodovi:  {p['ukupni_bodovi']} (posiljatelj={p['bodovi_posiljatelj']}, jezik={p['bodovi_jezik']}, url={p['bodovi_url']})")
        print()

    izracunaj_metriku(rezultati)
    spremi_rezultate(rezultati)


if __name__ == "__main__":
    pokreni_evaluaciju()