import pandas as pd
import requests
import csv
import os
from config import PUTANJA_DATASET


def ucitaj_dataset():
    df = pd.read_csv(PUTANJA_DATASET)
    ham = df[df["label"] == 0].sample(n=100, random_state=42)
    phishing = df[df["label"] == 1].sample(n=100, random_state=42)
    df = pd.concat([ham, phishing]).sample(frac=1, random_state=42).reset_index(drop=True)
    print(f"Učitano {len(df)} emailova (stratificirani uzorak: 100 phishing + 100 ham)")
    return df


def analiziraj_rspamd(row):
    subject = str(row.get("subject", ""))
    sender = str(row.get("sender", ""))
    body = str(row.get("body", ""))

    raw_email = (
        f"From: {sender}\r\n"
        f"To: test@test.com\r\n"
        f"Subject: {subject}\r\n"
        f"Date: Thu, 23 May 2026 12:00:00 +0000\r\n"
        f"Message-ID: <test123@test.com>\r\n"
        f"MIME-Version: 1.0\r\n"
        f"Content-Type: text/plain; charset=UTF-8\r\n"
        f"\r\n"
        f"{body}"
    )

    try:
        odgovor = requests.post(
            "http://localhost:11334/checkv2",
            data=raw_email.encode("utf-8"),
            headers={
                "Content-Type": "text/plain",
                "Password": "test123"
            },
            timeout=5
        )
        rezultat = odgovor.json()
        score = rezultat.get("score", 0)
        action = rezultat.get("action", "no action")
        return score, action

    except Exception as e:
        print(f"Greška: {e}")
        return 0, "error"


def odredi_klasifikaciju_rspamd(action, score):
    if action == "reject":
        return "PHISHING"
    elif action == "add header" and score >= 10:
        return "PHISHING"
    elif action == "add header" and score >= 6:
        return "SUMNJIVO"
    elif action == "greylist":
        return "SUMNJIVO"
    return "LEGITIMNO"


def pokreni_rspamd_evaluaciju():
    df = ucitaj_dataset()

    rezultati = []
    for i, row in df.iterrows():
        score, action = analiziraj_rspamd(row)
        stvarna_oznaka = int(row.get("label", 0))

        rezultati.append({
            "subject": str(row.get("subject", ""))[:50],
            "rspamd_score": score,
            "rspamd_action": action,
            "klasifikacija": odredi_klasifikaciju_rspamd(action, score),
            "stvarna_oznaka": stvarna_oznaka
        })

        if (i + 1) % 50 == 0:
            print(f"Analizirano {i + 1}/200 emailova...")

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
    print("RSPAMD REZULTATI EVALUACIJE")
    print("=" * 50)
    print(f"Ukupno emailova:  {ukupno}")
    print(f"Točnost:          {tocnost:.1f}%")
    print(f"Stopa detekcije:  {stopa_detekcije:.1f}%")
    print(f"Lažno pozitivni:  {lazno_pozitivni:.1f}%")
    print(f"Lažno negativni:  {lazno_negativni:.1f}%")
    print(f"TP: {tp}, TN: {tn}, FP: {fp}, FN: {fn}")

    os.makedirs("results", exist_ok=True)
    with open("results/rspamd_evaluacija.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "subject", "rspamd_score", "rspamd_action", "klasifikacija", "stvarna_oznaka"
        ])
        writer.writeheader()
        writer.writerows(rezultati)
    print("\nRezultati spremljeni u results/rspamd_evaluacija.csv")


if __name__ == "__main__":
    pokreni_rspamd_evaluaciju()