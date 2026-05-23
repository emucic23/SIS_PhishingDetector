BODOVI_SUMNJIVI_URL = 3
BODOVI_LAZNI_POSILJATELJ = 2
BODOVI_REPLY_TO = 2
BODOVI_ANOMALIJE_JEZIKA = 3

PRAG_PHISHING = 4      # sniženo s 5 — Nigerian_Fraud teško skupi 5 bodova
PRAG_SUMNJIVO = 2

MAILPIT_HOST = "mailpit"
MAILPIT_PORT = 1025
MAILPIT_API = "http://mailpit:8025/api"

PUTANJA_DATASET = "data/phishing_dataset_novi.csv"   # novi CSV umjesto xlsx
PUTANJA_REZULTATI = "results/results.csv"

POZNATE_DOMENE = [
    "gmail.com",
    "outlook.com",
    "yahoo.com",
    "fer.hr",
    "foi.hr",
    "unizg.hr"
]

URGENTNE_RIJECI = [
    "urgent", "immediately", "suspended", "verify",
    "click here", "limited time", "winner", "congratulations",
    "account blocked", "unusual activity", "confirm now",
    "click link", "verify now", "update your", "expires today",
    "avoid restriction", "reset now", "dear user",
    "account suspended", "password expiry", "bvn update"
]

FRAUD_FRAZE = [
    "dear friend", "strictly confidential", "god bless",
    "million dollars", "next of kin", "transfer of funds",
    "royal majesty", "i am a barrister", "foreign account",
    "business proposal", "partnership", "keep this secret",
    "claim your inheritance", "blessed opportunity"
]