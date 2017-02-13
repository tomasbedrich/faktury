#!/usr/bin/env python3

import requests
from xml.etree.ElementTree import parse

namespaces = {'D': 'http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_datatypes/v_1.0.3'}


def firma_info(ic):
    url = 'http://wwwinfo.mfcr.cz/cgi-bin/ares/darv_bas.cgi?ico={}'.format(ic)
    r = requests.get(url, stream=True)
    xml = parse(r.raw)
    r.close()

    # parsovani XML
    jmeno = xml.find('.//D:OF', namespaces).text
    ulice = xml.find('.//D:NU', namespaces).text
    cislo_popisne = xml.find('.//D:CD', namespaces).text
    cislo_orientacni = xml.find('.//D:CO', namespaces).text
    psc = xml.find('.//D:PSC', namespaces).text
    mesto = xml.find('.//D:N', namespaces).text

    dic_element = xml.find('.//D:DIC', namespaces)
    if dic_element is not None:
        dic = dic_element.text
    else:
        dic = None

    # typicky format adresy
    adresa_1 = '{} {}/{}'.format(ulice, cislo_popisne, cislo_orientacni)
    adresa_2 = '{} {}, {}'.format(psc[:3], psc[3:], mesto)

    return {
        'jmeno': jmeno,
        'ulice': ulice,
        'cislo_popisne': cislo_popisne,
        'cislo_orientacni': cislo_orientacni,
        'psc': psc,
        'mesto': mesto,
        'dic': dic,
        'adresa_1': adresa_1,
        'adresa_2': adresa_2
    }

if __name__ == '__main__':
    assert firma_info('67132162')['jmeno'] == 'Ing. Tomáš Bedřich'
    assert firma_info('02513668')['adresa_1'] == 'U Bachmače 1616/36'
    assert firma_info('02513668')['adresa_2'] == '326 00, Plzeň'
    assert firma_info('25648071')['adresa_1'] == 'Milady Horákové 116/109'
    assert firma_info('25648071')['dic'] == 'CZ25648071'
