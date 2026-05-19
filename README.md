# Phishing Detector

Alat za detekciju phishing e-poruka razvijen u sklopu kolegija Sigurnost informacijskih sustava.

## O projektu

Program analizira e-poruke i detektira phishing kombinirajući više indikatora:
- Analiza sumnjivih URL-ova
- Detekcija lažnog pošiljatelja
- Provjera neusklađenosti Reply-To zaglavlja
- Detekcija anomalija jezika

Svaki indikator donosi bodove, a ukupni score odlučuje o klasifikaciji:
- 0-3 → Legitimno
- 4-6 → Sumnjivo  
- 7-10 → Phishing

## Tehnologije

- Python 3.11
- Docker (Mailpit + Rspamd + analyzer)
- Kaggle phishing email dataset

Mailpit web sučelje: `http://localhost:8025`  
Rspamd web sučelje: `http://localhost:11334`

## Dataset
Preuzmite dataset s Kagglea i stavite u `data/` mapu:
https://www.kaggle.com/datasets/naserabdullahalam/phishing-email-dataset

## Struktura projekta

| Mapa | Sadržaj |
|------|---------|
| `src/` | Python kod: analiza i detekcija |
| `data/` | Dataset emailova za testiranje |
| `results/` | Rezultati analize |
| `report/` | Završni tehnički izvještaj |

## Tim
- Marko Mišić
- Ema Mučić
- Nina Obadić
