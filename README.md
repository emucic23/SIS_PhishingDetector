# SIS_PhishingDetector

Alat za detekciju phishing e-poruka razvijen u sklopu kolegija SIS.

## Struktura projekta

| Mapa | Sadržaj |
|------|---------|
| `src/` | Python kod: analiza emailova i detekcija phishinga |
| `data/` | Dataset emailova za testiranje (Kaggle) |
| `results/` | Rezultati analize: score i odluka za svaki email |
| `report/` | Završni tehnički izvještaj |

## Pokretanje

1. Pokrenite Mailpit: `./mailpit.exe`
2. Otvorite web sučelje: `http://localhost:8025`
3. Pokrenite detektor: `python src/analyzer.py
