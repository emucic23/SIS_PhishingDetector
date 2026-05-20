import re
from urrlib.parse import urlparse
from bs4 import BeautifulSoup

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