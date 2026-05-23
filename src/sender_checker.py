# Obmanjivanje prikaznim imenom
# Neusklađenost Reply-To
# Neusklađenost domene pošiljatelja

import email.utils
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
    """Hvata Nazario tip — 'Microsoft Outlook' <recepcao@unimedceara.com.br>"""
    ime, _, domena = izvuci_ime_i_domenu(zaglavlje_from)

    if not ime:
        return False

    ime_malo = ime.lower()
    for marka in POZNATE_MARKE:
        if marka in ime_malo and marka not in domena:
            return True

    return False


def ima_neuskladenost_reply_to(zaglavlje_from, zaglavlje_reply_to):
    """Hvata slučajeve gdje odgovor ide na drugu domenu"""
    if not zaglavlje_reply_to:
        return False

    _, _, domena_from = izvuci_ime_i_domenu(zaglavlje_from)
    _, _, domena_reply = izvuci_ime_i_domenu(zaglavlje_reply_to)

    return domena_from != domena_reply


def koristi_besplatni_servis_s_imenom_firme(zaglavlje_from):
    """Hvata Nigerian_Fraud tip — 'Barrister Tunde' <tunde@yahoo.com>
    Ime sugerira poslovnu osobu/organizaciju ali šalje s besplatnog servisa"""
    ime, _, domena = izvuci_ime_i_domenu(zaglavlje_from)

    if not ime or not domena:
        return False

    if domena not in BESPLATNI_MAIL_SERVISI:
        return False

    # Provjeri sadrži li ime sumnjive poslovne/titule riječi
    ime_malo = ime.lower()
    poslovne_rijeci = [
        "barrister", "attorney", "prince", "princess", "king", "royal",
        "director", "manager", "secretary", "minister", "officer",
        "dr.", "prof.", "rev.", "pastor", "bishop", "general"
    ]

    return any(rijec in ime_malo for rijec in poslovne_rijeci)


def provjeri_posiljatelja(zaglavlje_from, zaglavlje_reply_to):
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

    if not rezultat["objasnjenje"]:
        rezultat["objasnjenje"].append("Pošiljatelj izgleda legitimno")

    return rezultat


if __name__ == "__main__":
    # Test Nazario tip
    print(provjeri_posiljatelja(
        '"Microsoft Outlook" <recepcao@unimedceara.com.br>', ""
    ))

    # Test Nigerian_Fraud tip
    print(provjeri_posiljatelja(
        '"Barrister Tunde Dosumu" <tunde_dosumu@lycos.com>', ""
    ))

    # Test legitimni
    print(provjeri_posiljatelja(
        '"Google" <no-reply@google.com>', ""
    ))