import re
from config import BODOVI_ANOMALIJE_JEZIKA


HRVATSKE_RIJECI = [
    "poštovani", "račun", "lozinka", "potvrdite",
    "uplata", "banka", "korisnik", "sigurnost",
    "obavijest", "plaćanje", "kartica"
]

ENGLESKE_RIJECI = [
    "account", "password", "verify", "login",
    "security", "payment", "confirm", "urgent",
    "suspended", "locked", "update"
]

PRAVOPISNE_GRESKE = [
    "verfy", "pasword", "securty", "accout",
    "immediatly", "recieve", "confrm", "logn",
    "adress", "informacion", "succesfull"
]

GENERICKI_POZDRAVI = [
    "dear user",
    "dear customer",
    "hello customer",
    "poštovani korisniče",
    "dragi korisniče"
]

NAREDBENE_FRAZE = [
    "click now",
    "act now",
    "verify now",
    "confirm now",
    "login now",
    "respond immediately",
    "potvrdite odmah",
    "kliknite odmah",
    "prijavite se odmah",
    "click link",
    "reset now",
    "update your",
    "expires today",
]

SUMNJIVE_FRAZE = [
    "!!!",
    "???",
    "free money",
    "limited time",
    "winner",
    "claim your prize"
]


def dodaj_indikator(indikatori, poruka):
    indikatori.append(poruka)


def ima_puno_usklicnika(tekst):
    return tekst.count("!") >= 3


def ima_previse_velikih_slova(subject):
    slova = [z for z in subject if z.isalpha()]
    velika = [z for z in subject if z.isupper()]

    if len(slova) <= 5:
        return False

    return len(velika) / len(slova) > 0.6


def ima_cudne_razmake(tekst):
    return re.search(r"\s{4,}", tekst) is not None


def mijesa_jezike(tekst):
    ima_hr = any(rijec in tekst for rijec in HRVATSKE_RIJECI)
    ima_en = any(rijec in tekst for rijec in ENGLESKE_RIJECI)

    return ima_hr and ima_en


def pronadi_pravopisne_greske(tekst):
    return [greska for greska in PRAVOPISNE_GRESKE if greska in tekst]


def ima_sumnjive_znakove(tekst):
    return re.search(r"[$€]{2,}|[@#*]{3,}", tekst) is not None


def koristi_genericki_pozdrav(tekst):
    return any(pozdrav in tekst for pozdrav in GENERICKI_POZDRAVI)


def pronadi_naredbene_fraze(tekst):
    return [fraza for fraza in NAREDBENE_FRAZE if fraza in tekst]


def ima_neobicne_unicode_znakove(tekst):
    return re.search(r"[^\x00-\x7F]{8,}", tekst) is not None


def pronadi_sumnjive_fraze(tekst):
    return [fraza for fraza in SUMNJIVE_FRAZE if fraza in tekst]


def provjeri_jezik(subject="", body=""):
    tekst = f"{subject} {body}"
    tekst_lower = tekst.lower()

    bodovi = 0
    indikatori = []

    if ima_puno_usklicnika(tekst):
        bodovi += 1
        dodaj_indikator(indikatori, "Puno uskličnika u poruci")

    if ima_previse_velikih_slova(subject):
        bodovi += 1
        dodaj_indikator(
            indikatori,
            "Subject sadrži neuobičajeno puno velikih slova"
        )

    if ima_cudne_razmake(tekst):
        bodovi += 1
        dodaj_indikator(
            indikatori,
            "Poruka sadrži neobično velike razmake"
        )

    if mijesa_jezike(tekst_lower):
        bodovi += 1
        dodaj_indikator(
            indikatori,
            "Poruka sadrži miješanje hrvatskog i engleskog jezika"
        )

    pravopisne_greske = pronadi_pravopisne_greske(tekst_lower)

    if pravopisne_greske:
        bodovi += 1
        dodaj_indikator(
            indikatori,
            "Pronađene moguće pravopisne greške: "
            + ", ".join(pravopisne_greske)
        )

    if ima_sumnjive_znakove(tekst):
        bodovi += 1
        dodaj_indikator(
            indikatori,
            "Poruka sadrži neobično formatiranje ili sumnjive znakove"
        )

    if koristi_genericki_pozdrav(tekst_lower):
        bodovi += 1
        dodaj_indikator(
            indikatori,
            "Poruka koristi generički pozdrav umjesto imena korisnika"
        )

    naredbene_fraze = pronadi_naredbene_fraze(tekst_lower)

    if naredbene_fraze:
        bodovi += 1
        dodaj_indikator(
            indikatori,
            "Poruka koristi naredbeni/agresivan stil: "
            + ", ".join(naredbene_fraze)
        )

    if ima_neobicne_unicode_znakove(tekst):
        bodovi += 1
        dodaj_indikator(
            indikatori,
            "Poruka sadrži veći broj neuobičajenih Unicode znakova"
        )

    sumnjive_fraze = pronadi_sumnjive_fraze(tekst_lower)

    if sumnjive_fraze:
        bodovi += 1
        dodaj_indikator(
            indikatori,
            "Pronađeno sumnjivo phishing formatiranje: "
            + ", ".join(sumnjive_fraze)
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

    rezultat = provjeri_jezik(
        subject="URGENT VERIFY ACCOUNT NOW!!!",
        body="""
        Dear user,

        Poštovani korisniče, your accout is suspended.
        Confrm your pasword immediatly.     Click now!!!
        """
    )

    print(rezultat)