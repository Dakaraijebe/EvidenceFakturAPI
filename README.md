# Firemní evidence faktur – REST API

Tento projekt je ukázkové REST API pro správu vydaných a přijatých faktur.  
Umožňuje vystavení, evidenci, filtrování a generování přehledů.  
Součástí je i Swagger dokumentace dostupná na `/api`.

---

## 🚀 Funkce API

| Metoda | Endpoint | Popis |
|---------|-----------|--------|
| **GET** | `/invoices` | Vrátí seznam všech faktur (volitelné filtry: `?paid=true`, `?customer=ABC`) |
| **POST** | `/invoices` | Vytvoří novou fakturu |
| **GET** | `/invoices/<id>` | Vrátí detail konkrétní faktury |
| **DELETE** | `/invoices/<id>` | Smaže fakturu |
| **GET** | `/reports/unpaid` | Vrátí všechny nezaplacené faktury |
| **GET** | `/reports/debtors` | Vrátí seznam dlužníků podle výše dluhu |
| **GET** | `/reports/statistics` | Vrátí přehledné statistiky (počet, součty, průměrná doba úhrady) |
| **GET** | `/api` | Swagger dokumentace (vizuální přehled endpointů) |

---

## 🧰 Požadavky na software

Pro lokální spuštění je potřeba:

- [Python 3.10+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/)
- Webový prohlížeč (pro Swagger UI)

Volitelně:
- [Postman](https://www.postman.com/) nebo `curl` pro testování endpointů

---

## 🧱 Instalace a spuštění lokálně

1. Naklonuj repozitář:
   ```bash
   git clone https://github.com/<TVŮJ_UŽIVATEL>/fakturace-api.git
   cd fakturace-api

2. Nainstaluj požadované balíčky:

pip install flask flask-swagger-ui pyyaml

3.Spusť aplikaci:

python app.py

4.Otevři v prohlížeči:

API endpointy: http://127.0.0.1:5000/invoices

Swagger dokumentace: http://127.0.0.1:5000/api
