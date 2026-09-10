```markdown
# Ranking Coefficient Analyzer

Agent pro analýzu rankingových koeficientů orientačního běhu.

## Popis

Tento projekt obsahuje agenta, který automaticky:
1. Stáhne data z ORIS (startovka a ranking)
2. Vypočítá rankingový koeficient pro každou kvalifikační skupinu
3. Vygeneruje profesionální PDF report s výsledky

## Funkcionality

- **Automatické stahování dat** z ORIS webových stránek
- **Výpočet koeficientů** - průměr koeficientu 4 nejlépe umístěných běžců
- **Generování PDF reportu** s přehledným formátováním
- **Podpora více kategorií** - H21 (Muži 21) a D21 (Ženy 21)

## Requirements

```bash
pip install -r requirements.txt
```

### Závislosti
- requests - HTTP knihovna
- beautifulsoup4 - HTML parsing
- pandas - Data análýza
- reportlab - PDF generování

## Konfigurace

Upravte `config.py` podle vašich potřeb:

```python
# ORIS URLs
RANKING_URL = "https://oris.ceskyorientak.cz/Ranking?sport=1&ranktype=2"
STARTOVKA_URL = "https://oris.ceskyorientak.cz/Startovka?id=8950"

# Cílové kategorie
TARGET_CATEGORIES = ["H21", "D21"]

# Počet běžců pro výpočet koeficientu
TOP_RUNNERS_COUNT = 4

# Výstupní adresář
OUTPUT_DIR = "reports"
PDF_FILENAME = "ranking_coefficient_report.pdf"
```

## Spuštění

### Běžné spuštění
```bash
python agent.py
```

Skript pak:
1. Stáhne data z ORIS
2. Zpracuje je pro obě kategorie (H21, D21)
3. Vygeneruje PDF report do adresáře `reports/`

## Struktura projektu

```
rank_analazer/
├── agent.py              # Hlavní orchestrační modul
├── config.py            # Konfigurace
├── scraper.py           # Stahování dat z ORIS
├── analyzer.py          # Analýza dat a výpočty
├── report_generator.py  # Generování PDF reportu
├── requirements.txt     # Balíčky
├── reports/             # Výstupní adresář pro PDF
└── README.md           # Tento soubor
```

## Výpočet koeficientu

Koeficient se vypočítá takto:
1. Filtrují se všichni běžci pro danou kategorii
2. Vyberou se 4 běžci s nejvyšším koeficientem z rankingu
3. Spočítá se průměr jejich koeficientů
4. Výsledek se zaokrouhlí na 4 desetinná místa

## Příklad výstupu

PDF report obsahuje:
- Nadpis s datem
- Pro každou kategorii (H21, D21):
  - Vypočítaný koeficient
  - Jména a koeficienty 4 nejlépe umístěných běžců
- Souhrnnout tabulku se všemi výsledky

## Logování

Agent generuje detailní logy během běhu:
```
2026-09-10 12:30:45 - agent - INFO - Ranking Coefficient Agent initialized
2026-09-10 12:30:45 - agent - INFO - Starting Ranking Coefficient Analysis
2026-09-10 12:30:46 - scraper - INFO - Fetching ranking data from https://...
...
```

## Chyby a řešení

### Stránka se nenačte
- Zkontrolujte internetové připojení
- Ověřte, že URL v `config.py` je správná
- ORIS server může být přetížený, zkuste později

### Žádná data pro kategorii
- Kategorie nemusí existovat na daném MČR
- Zkontrolujte správné ID závodů v URL

### PDF se negeneruje
- Zkontrolujte práva k zápisu do `reports/` adresáře
- Ujistěte se, že reportlab je správně nainstalován

## Autor

Vytěženo pro účely analýzy rankingů orientačního běhu.

## Licence

MIT
```
