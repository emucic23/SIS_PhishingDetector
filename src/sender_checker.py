#Obmanjivanje prikaznim imenom
#Neusklađenost Reply-To

import email.utils
from config import BODOVI_LAZNI_POSILJATELJ, BODOVI_REPLY_TO


POZNATE_MARKE = [
    "paypal", "google", "microsoft", "apple",
    "amazon", "netflix", "erste", "zaba", "pbz",
    "facebook", "instagram", "linkedin",
    "hep", "hrvatski telekom", "a1"
]


def izvuci_ime_i_domenu(zaglavlje_from):
    ime, adresa = email.utils.parseaddr(zaglavlje_from)
    domena = adresa.split("@")[-1] if "@" in adresa else ""
    return ime, adresa, domena


def ima_lazno_prikazno_ime(zaglavlje_from):
    ime, _, domena = izvuci_ime_i_domenu(zaglavlje_from)

    if not ime:
        return False

    ime_malo = ime.lower()
    for marka in POZNATE_MARKE:
        if marka in ime_malo and marka not in domena:
            return True

    return False


def ima_neuskladenost_reply_to(zaglavlje_from, zaglavlje_reply_to):
    if not zaglavlje_reply_to:
        return False

    _, _, domena_from = izvuci_ime_i_domenu(zaglavlje_from)
    _, _, domena_reply = izvuci_ime_i_domenu(zaglavlje_reply_to)

    return domena_from != domena_reply


def provjeri_posiljatelja(zaglavlje_from, zaglavlje_reply_to):
    rezultat = {"bodovi": 0, "objasnjenje": []}

    if ima_lazno_prikazno_ime(zaglavlje_from):
        rezultat["bodovi"] += BODOVI_LAZNI_POSILJATELJ
        rezultat["objasnjenje"].append("Prikazno ime ne odgovara domeni pošiljatelja")

    if ima_neuskladenost_reply_to(zaglavlje_from, zaglavlje_reply_to):
        rezultat["bodovi"] += BODOVI_REPLY_TO
        rezultat["objasnjenje"].append("Reply-To domena razlikuje se od From domene")

    if not rezultat["objasnjenje"]:
        rezultat["objasnjenje"].append("Pošiljatelj izgleda legitimno")

    return rezultat