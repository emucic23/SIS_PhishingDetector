import re
import email.utils
from urllib.parse import urlparse
from config import BODOVI_LAZNI_POSILJATELJ, BODOVI_REPLY_TO

POZNATE_MARKE = [
    "paypal", "google", "microsoft", "apple",
    "amazon", "netflix", "facebook", "instagram", "linkedin",
    "twitter", "whatsapp", "dropbox", "ebay", "spotify",
    "adobe", "chase", "wellsfargo", "bankofamerica", "citibank",
    "dhl", "fedex", "ups", "usps",
    "steam", "discord", "twitch",
    "yahoo", "outlook", "gmail"
]

BESPLATNI_MAIL_SERVISI = [
    "gmail.com", "yahoo.com", "hotmail.com", "outlook.com",
    "aol.com", "mail.com", "protonmail.com", "icloud.com",
    "maktoob.com", "spinfinder.com", "epatra.com",
    "postmark.net", "lycos.com", "netscape.net",
    "virgilio.it", "latinmail.com", "walla.com"
]


def izvuci_ime_i_domenu(zaglavlje_from):
    ime, adresa = email.utils.parseaddr(zaglavlje_from)
    domena = adresa.split("@")[-1].lower() if "@" in adresa else ""
    return ime, adresa, domena


def ima_lazno_prikazno_ime(zaglavlje_from):
    ime, _, domena = izvuci_ime_i_domenu(zaglavlje_from)
    if not ime:
        return False

    ime_malo = ime.lower()

    for marka in POZNATE_MARKE:
        if marka in ime_malo and marka not in domena:
            return True

    # Generička provjera: ime sadrži domenu koja se razlikuje od stvarne
    domena_u_imenu = re.search(r"[\w-]+\.(com|org|net|hr|ba|rs|eu|co\.uk)", ime_malo)
    if domena_u_imenu:
        domena_iz_imena = domena_u_imenu.group(0)
        if domena_iz_imena not in domena:
            return True

    return False


def ima_neuskladenost_reply_to(zaglavlje_from, zaglavlje_reply_to):
    if not zaglavlje_reply_to:
        return False
    _, _, domena_from = izvuci_ime_i_domenu(zaglavlje_from)
    _, _, domena_reply = izvuci_ime_i_domenu(zaglavlje_reply_to)
    return domena_from != domena_reply


def koristi_besplatni_servis_s_imenom_firme(zaglavlje_from):
    ime, _, domena = izvuci_ime_i_domenu(zaglavlje_from)
    if not ime or not domena:
        return False
    if domena not in BESPLATNI_MAIL_SERVISI:
        return False
    ime_malo = ime.lower()
    poslovne_rijeci = [
        "barrister", "attorney", "prince", "princess", "king", "royal",
        "director", "manager", "secretary", "minister", "officer",
        "dr.", "prof.", "rev.", "pastor", "bishop", "general"
    ]
    return any(rijec in ime_malo for rijec in poslovne_rijeci)


def provjeri_konzistentnost_domene(zaglavlje_from, body):
    _, _, domena_from = izvuci_ime_i_domenu(zaglavlje_from)
    if not domena_from:
        return False

    urlovi = re.findall(r"https?://[^\s\"'<>]+", body)

    for url in urlovi:
        try:
            domena_url = urlparse(url).netloc.lower()
            if domena_url.startswith("www."):
                domena_url = domena_url[4:]
            domena_url = domena_url.split(":")[0]
        except Exception:
            continue

        if not domena_url:
            continue

        if domena_from not in domena_url and domena_url not in domena_from:
            return True

    return False


def provjeri_posiljatelja(zaglavlje_from, zaglavlje_reply_to, body=""):
    rezultat = {"bodovi": 0, "objasnjenje": []}

    if ima_lazno_prikazno_ime(zaglavlje_from):
        rezultat["bodovi"] += BODOVI_LAZNI_POSILJATELJ
        rezultat["objasnjenje"].append("Prikazno ime ne odgovara domeni pošiljatelja")

    if ima_neuskladenost_reply_to(zaglavlje_from, zaglavlje_reply_to):
        rezultat["bodovi"] += BODOVI_REPLY_TO
        rezultat["objasnjenje"].append("Reply-To domena razlikuje se od From domene")

    if koristi_besplatni_servis_s_imenom_firme(zaglavlje_from):
        rezultat["bodovi"] += 1
        rezultat["objasnjenje"].append("Poslovna titula/ime šalje s besplatnog mail servisa")

    if provjeri_konzistentnost_domene(zaglavlje_from, body):
        rezultat["bodovi"] += 2
        rezultat["objasnjenje"].append("Domena pošiljatelja ne odgovara domenama URL-ova u poruci")

    if not rezultat["objasnjenje"]:
        rezultat["objasnjenje"].append("Pošiljatelj izgleda legitimno")

    return rezultat


if __name__ == "__main__":
    print(provjeri_posiljatelja(
        '"Microsoft Outlook" <recepcao@unimedceara.com.br>',
        "",
        "Please verify your account at http://microsoft-login.ru/verify"
    ))

    print(provjeri_posiljatelja(
        '"Barrister Tunde Dosumu" <tunde_dosumu@lycos.com>',
        "",
        "Please contact me for business proposal"
    ))

    print(provjeri_posiljatelja(
        '"Google" <no-reply@google.com>',
        "",
        "Visit https://google.com for more info"
    ))