import pandas as pd

nazario  = pd.read_csv("data/Nazario.csv")
nigerian = pd.read_csv("data/Nigerian_Fraud.csv")
ceas     = pd.read_csv("data/CEAS_08.csv")

# Phishing klasa
phishing = pd.concat([nazario, nigerian], ignore_index=True)
phishing["label"] = 1
print(f"Phishing emailova: {len(phishing)}")

# Ham klasa
ham = ceas[ceas["label"] == 0].sample(n=len(phishing), random_state=42)
ham["label"] = 0
print(f"Ham emailova: {len(ham)}")

# Spoji i spremi
df = pd.concat([phishing, ham], ignore_index=True)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

df.to_csv("data/phishing_dataset_novi.csv", index=False)
print(f"Gotovo! Ukupno: {len(df)} emailova")
print(df["label"].value_counts())