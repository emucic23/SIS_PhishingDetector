import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from config import BODOVI_SUMNJIVI_URL

SUMNJIVI_TLDOVI = {
  ".ru", ".xyz", ".tk", ".top", ".pw", ".cc", ".ga", ".ml", ".cf",
  ".gq", ".work", ".loan", ".click", ".download", ".zip", ".review",
  ".country", ".kim", ".science", ".party", ".bid", ".trade"
}
 
URL_SHORTENERI = {
  "bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly", "is.gd",
  "buff.ly", "adf.ly", "short.link", "rebrand.ly", "cutt.ly",
  "shorturl.at", "tiny.cc", "cli.re", "shrtco.de"
}

POZNATE_MARKE = [
  "paypal", "google", "microsoft", "apple",
  "amazon", "netflix", "erste", "zaba", "pbz",
  "facebook", "instagram", "linkedin",
  "hep", "hrvatskitelekom", "a1"
]

IP_UZORAK = re.compile(r"https?://(\d{1,3}\.){3}\d{1,3}")
URL_UZORAK = re.compile(r"https?://[^\s\"'<>]+")

def izvuci_domenu(url):
  try:
    domena = urlparse(url).netloc.lower()
    domena = domena.split(":")[0]
    if domena.startswith("www."):
      domena = domena[4:]
    return domena
  except Exception:
    return ""
 
 
def izvuci_linkove_iz_html(html_body):
  soup = BeautifulSoup(html_body, "html.parser")
  linkovi = []
  for tag in soup.find_all("a", href=True):
    href = tag["href"].strip()
    prikaz = tag.get_text(strip=True)
    if href.startswith("http"):
      linkovi.append({"prikaz": prikaz, "href": href})
  return linkovi
 
 
def izvuci_urlove_iz_teksta(tekst):
  return URL_UZORAK.findall(tekst)

def provjeri_sumnjive_tldove(urlovi):
  bodovi = 0
  indikatori = []

  for url in urlovi:
    domena = izvuci_domenu(url)
    for tld in SUMNJIVI_TLDOVI:
      if domena.endswith(tld):
        bodovi += 3
        indikatori.append(f"Sumnjivi TLD u URL-u: '{domena}'")
        break

  return bodovi, indikatori

def provjeri_ip_url(urlovi):
  bodovi = 0
  indikatori = []

  for url in urlovi:
    if IP_UZORAK.match(url):
      bodovi += 3
      indikatori.append(f"URL koristi IP adresu umjesto domene: '{url[:60]}'")

  return bodovi, indikatori

def provjeri_url_shortener(urlovi):
  bodovi = 0
  indikatori = []

  for url in urlovi:
    domena = izvuci_domenu(url)
    if domena in URL_SHORTENERI:
      bodovi += 3
      indikatori.append(f"URL shortener skriva odredište: '{domena}'")

  return bodovi, indikatori

def provjeri_neuskladenost_linka(linkovi):
  bodovi = 0
  indikatori = []

  for link in linkovi:
    prikaz = link["prikaz"]
    href = link["href"]

    pronasao = re.search(r"([\w-]+\.[a-z]{2,})", prikaz.lower())
    if not pronasao:
      continue
      

    domena_prikaz = pronasao.group(1)
    domena_href = izvuci_domenu(href)

    if not domena_href:
      continue

    if domena_prikaz not in domena_href and domena_href not in domena_prikaz:
      bodovi += BODOVI_SUMNJIVI_URL
      indikatori.append(
        f"Neusklađenost linka: prikazano '{domena_prikaz}' vodi na '{domena_href}'"
      )

  return bodovi, indikatori

def provjeri_imitaciju_marke(urlovi):
  bodovi = 0
  indikatori = []

  for url in urlovi:
    domena = izvuci_domenu(url)
    for marka in POZNATE_MARKE:
      marka_clean = marka.lower().replace(" ", "")
      if marka_clean in domena:
        dijelovi = domena.split(".")
        if len(dijelovi) > 2 or (len(dijelovi) == 2 and dijelovi[0] != marka_clean):
          bodovi += BODOVI_SUMNJIVI_URL
          indikatori.append(
            f"Imitacija marke '{marka}' u sumnjivoj domeni: '{domena}'"
          )
          break

  return bodovi, indikatori

def provjeri_urlove(subject, body):
  if "<a " in body.lower() or "<html" in body.lower():
    linkovi = izvuci_linkove_iz_html(body)
    urlovi = [link["href"] for link in linkovi]
    urlovi += izvuci_urlove_iz_teksta(subject)
  else:
    linkovi = []
    urlovi = izvuci_urlove_iz_teksta(body) + izvuci_urlove_iz_teksta(subject)

  urlovi = list(dict.fromkeys(urlovi))

  if not urlovi and not linkovi:
    return {"bodovi": 0, "indikatori": []}

  ukupni_bodovi = 0
  svi_indikatori = []

  provjere = [
    provjeri_neuskladenost_linka(linkovi),
    provjeri_sumnjive_tldove(urlovi),
    provjeri_ip_url(urlovi),
    provjeri_url_shortener(urlovi),
    provjeri_imitaciju_marke(urlovi),
  ]

  for bodovi, indikatori in provjere:
    ukupni_bodovi += bodovi
    svi_indikatori.extend(indikatori)

  return {"bodovi": ukupni_bodovi, "indikatori": svi_indikatori}