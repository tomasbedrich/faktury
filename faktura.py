#!/usr/bin/env python3

import datetime
from click import prompt
from jinja2 import Template
from mena import mena_kc
from ares import firma_info

parameter_sablony = dict()
today = datetime.date.today()

print("Odběratel", "=" * 80)
parameter_sablony["odberatel"] = firma_info(prompt("IČ"))

print("Faktura", "=" * 80)
cislo_faktury = prompt("Číslo faktury", type=int)
parameter_sablony["cislo_faktury"] = "{:%Y%m}{:0>2}".format(today, cislo_faktury)
parameter_sablony["cislo_objednavky"] = prompt("Číslo objednávky", default="–")
parameter_sablony["datum_vystaveni"] = "{:%d. %m. %Y}".format(today)
dni = prompt("Délka splatnosti - dny", default=14)
datum_splatnosti = today + datetime.timedelta(days=dni)
parameter_sablony["datum_splatnosti"] = "{:%d. %m. %Y}".format(datum_splatnosti)

polozky = []
parameter_sablony["polozky"] = polozky
cena_celkem_k_uhrade = 0
print("Položky", "=" * 80)

while True:
    polozka = dict()
    pocet_mnozstvi = prompt("Množství (pro ukončení zadej 0)", default=1)
    if pocet_mnozstvi == 0:
        break
    polozka["pocet_mnozstvi"] = str(pocet_mnozstvi)
    polozka["m_j"] = prompt("Měrná jednotka", default="ks.")
    polozka["oznaceni_dodavky"] = prompt("Označení dodávky")
    cena_za_m_j = prompt("Cena za měrnou jednotku", type=float)
    polozka["cena_za_m_j"] = mena_kc(cena_za_m_j)
    cena_celkem = pocet_mnozstvi * cena_za_m_j
    polozka["cena_celkem"] = mena_kc(cena_celkem)
    cena_celkem_k_uhrade += cena_celkem
    polozky.append(polozka)
    print("-" * 80)

parameter_sablony["cena_celkem_k_uhrade"] = mena_kc(cena_celkem_k_uhrade)

# pre spravne zobrazovanie ceskych znakov musim napisat do paramentru metody encoding="utf-8"

with open("template.html", "r", encoding="utf-8") as index:
    sablona = Template(index.read())
    nova_faktura_str = sablona.render(**parameter_sablony)
    with open("{}.html".format(parameter_sablony["cislo_faktury"]), "w", encoding="utf-8") as nova_faktura_html:
        nova_faktura_html.write(nova_faktura_str)

print("Vsechno probehlo v poradku. Mas to pripravene :)")
