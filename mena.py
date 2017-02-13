#!/usr/bin/env python3

def mena_kc(cislo):
	cislo = float(cislo)
	cislo = "{:,.2f}".format(cislo)
	cela, desatinna = cislo.split(".")
	cela = cela.replace(",", " ")
	cislo = "{},{} Kč".format(cela, desatinna)
	return cislo

if __name__ == '__main__':
	assert mena_kc("5000") == "5 000,00 Kč"
	assert mena_kc("50000") == "50 000,00 Kč"
	assert mena_kc("5089000") == "5 089 000,00 Kč"
	assert mena_kc("5000.50") == "5 000,50 Kč"

# test sa spusti len pri spusteni cez ctrl+B, nie pri importe metody
