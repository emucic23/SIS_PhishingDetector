import re
from config import BODOVI_ANOMALIJE_JEZIKA


def provjeri_jezik(subject="", body=""):
    tekst = f"{subject} {body}"
    tekst_lower = tekst.lower()

    bodovi = 0
    indikatori = []

    if tekst.count("!") >= 3:
        bodovi += 1
        indikatori.append("Puno uskličnika u poruci")

    slova = [z for z in subject if z.isalpha()]
    velika = [z for z in subject if z.isupper()]

    if len(slova) > 5 and len(velika) / len(slova) > 0.6:
        bodovi += 1
        indikatori.append("Subject sadrži neuobičajeno puno velikih slova")

    if re.search(r"\s{4,}", tekst):
        bodovi += 1
        indikatori.append("Poruka sadrži neobično velike razmake")

    hrvatske_rijeci = [
        "poštovani", "račun", "lozinka", "potvrdite",
        "uplata", "banka", "korisnik", "sigurnost",
        "obavijest", "plaćanje", "kartica"
    ]

    engleske_rijeci = [
        "account", "password", "verify", "login",
        "security", "payment", "confirm", "urgent",
        "suspended", "locked", "update"
    ]

    ima_hr = any(rijec in tekst_lower for rijec in hrvatske_rijeci)
    ima_en = any(rijec in tekst_lower for rijec in engleske_rijeci)

    if ima_hr and ima_en:
        bodovi += 1
        indikatori.append("Poruka sadrži miješanje hrvatskog i engleskog jezika")

    greske = [
        "verfy", "pasword", "securty", "accout",
        "immediatly", "recieve", "confrm", "logn",
        "adress", "informacion", "succesfull"
    ]

    pronadene_greske = [g for g in greske if g in tekst_lower]

    if pronadene_greske:
        bodovi += 1
        indikatori.append(
            "Pronađene moguće pravopisne greške: " + ", ".join(pronadene_greske)
        )

    if re.search(r"[$€]{2,}|[@#*]{3,}", tekst):
        bodovi += 1
        indikatori.append("Poruka sadrži neobično formatiranje ili sumnjive znakove")

    genericki_pozdravi = [
        "dear user",
        "dear customer",
        "hello customer",
        "poštovani korisniče",
        "dragi korisniče"
    ]

    if any(pozdrav in tekst_lower for pozdrav in genericki_pozdravi):
        bodovi += 1
        indikatori.append("Poruka koristi generički pozdrav umjesto imena korisnika")

    naredbene_fraze = [
        "click now",
        "act now",
        "verify now",
        "confirm now",
        "login now",
        "respond immediately",
        "potvrdite odmah",
        "kliknite odmah",
        "prijavite se odmah"
    ]

    pronadene_naredbe = [f for f in naredbene_fraze if f in tekst_lower]

    if pronadene_naredbe:
        bodovi += 1
        indikatori.append(
            "Poruka koristi naredbeni/agresivan stil: " + ", ".join(pronadene_naredbe)
        )

    if re.search(r"[^\x00-\x7F]{8,}", tekst):
        bodovi += 1
        indikatori.append("Poruka sadrži veći broj neuobičajenih Unicode znakova")

    sumnjivo_formatiranje = [
        "!!!",
        "???",
        "free money",
        "limited time",
        "winner",
        "claim your prize"
    ]

    pronadeno_formatiranje = [f for f in sumnjivo_formatiranje if f in tekst_lower]

    if pronadeno_formatiranje:
        bodovi += 1
        indikatori.append(
            "Pronađeno sumnjivo marketinško/phishing formatiranje: "
            + ", ".join(pronadeno_formatiranje)
        )

    
    if len(indikatori) >= 2:
        bodovi = max(bodovi, BODOVI_ANOMALIJE_JEZIKA)

    return {
        "naziv": "Anomalije jezika ili formatiranja",
        "bodovi": bodovi,
        "indikatori": indikatori,
        "sumnjivo": bodovi > 0
    }


if __name__ == "__main__":
    # Testiranje funkcije s primjerom sumnjivog maila
    
    rezultat = provjeri_jezik(
        subject="URGENT VERIFY ACCOUNT NOW!!!",
        body="""
        Dear user,

        Poštovani korisniče, your accout is suspended.
        Confrm your pasword immediatly.     Click now!!!
        """
    )

    print(rezultat)