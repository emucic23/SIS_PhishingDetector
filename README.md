# Phishing Detector

Alat za detekciju phishing e-poruka razvijen u sklopu kolegija Sigurnost informacijskih sustava.

## O projektu

Program analizira e-poruke i detektira phishing kombinirajući više indikatora:
- Analiza sumnjivih URL-ova
- Detekcija lažnog pošiljatelja
- Provjera neusklađenosti Reply-To zaglavlja
- Detekcija anomalija jezika i fraud fraza

Svaki indikator donosi bodove, a ukupni score odlučuje o klasifikaciji:
- 0-3 → Legitimno
- 4 → Phishing
- 2-3 → Sumnjivo

## Tehnologije

- Python 3.11
- Docker (Mailpit + Rspamd + analyzer)
- [Kaggle Phishing Email Dataset](https://www.kaggle.com/datasets/naserabdullahalam/phishing-email-dataset)

## Dataset

### 1. Preuzimanje

Preuzmi dataset s Kagglea:
**[Phishing Email Dataset](https://www.kaggle.com/datasets/naserabdullahalam/phishing-email-dataset)**

Nakon preuzimanja raspakiraj ZIP i iz njega u `data/` folder projekta kopiraj:
- `Nazario.csv`
- `Nigerian_Fraud.csv`
- `CEAS_08.csv`

### 2. Struktura foldera
```
SIS_PHISHINGDETECTOR/
  data/
    Nazario.csv
    Nigerian_Fraud.csv
    CEAS_08.csv
    phishing_dataset_novi.csv  ← kreira se automatski
```
### 3. Kreiranje balansiranog dataseta

Pokreni jednom:

```bash
python prepare_dataset.py
```

Skripta kreira `data/phishing_dataset_novi.csv`:
- 4.897 phishing emailova (Nazario + Nigerian_Fraud)
- 4.897 ham emailova (CEAS_08 ham dio)
- Ukupno: 9.794 emailova, 50/50 split

## Pokretanje

```bash
# Instaliraj dependencies
pip install -r requirements.txt

# Pokreni Docker okruženje
docker-compose up -d

# Pokreni analyzer (prima emailove iz Mailpit-a)
python src/analyzer.py
```

## Evaluacija

```bash
# Vlastiti alat — evaluacija na cijelom datasetu
python src/dataset_evaluator.py

# Rspamd evaluacija
python src/rspamd_evaluator.py
```

Rezultati se spremaju u `results/` folder:
- `results/evaluacija.csv` - rezultati vlastitog alata
- `results/rspamd_evaluacija.csv` - rezultati Rspamd evaluacije

## Testiranje

Pošalji testne emailove kroz Mailpit:

```bash
python src/test_mailpit.py
```

Mailpit web sučelje: `http://localhost:8025`  
Rspamd web sučelje: `http://localhost:11334`

## Struktura projekta

| Mapa | Sadržaj |
|---|---|
| `src/` | Python kod: analiza i detekcija |
| `data/` | Dataset emailova za testiranje |
| `results/` | Rezultati analize |
| `report/` | Završni tehnički izvještaj |


## Tim
- Marko Mišić
- Ema Mučić
- Nina Obadić
