#!/usr/bin/env python3
# -*- coding: utf8

# parking2osm
# Converts parkering areas from Statens Vegvesen api feed to osm format for import/update
# Usage: python3 parking2osm.py [output_filename.osm]
# Default output filename: "parkeringsregisteret.osm"


import urllib.request
import html
import csv
import json
import sys
from io import TextIOWrapper


version = "2.0.0"

transform_name = {
	'Alle': 'allé',
	'alle': 'allé',
	'Allé': 'allé',
	'AMFI': 'Amfi',
	'Barnehage': 'barnehage',
	'Boligsameie': 'boligsameie',
	'Brygge': 'brygge',
	'Borettslag': 'borettslag',
	'brl': 'borettslag',
	'Butikksenter': 'butikksenter',
	'COOP': 'Coop',
	'Ekspressparkering': 'ekspressparkering',
	'EUROSPAR': 'Eurospar',
	'Gammel': 'gammel',
	'Gammelt': 'gammelt',
	'Gate': 'gate',
	'Garasje': 'garasje',
	'Gjesteparkering': 'gjesteparkering',
	'Gravplass': 'gravplass',
	'Hagesenter': 'hagesenter',
	'Havn': 'havn',
	'HUS': 'hus',
	'Høgfjellstove': 'høgfjellstove',
	'Idrettshall': 'idrettshall',
	'Idrettspark': 'idrettspark',
	'Inne': 'inne',
	'INNE': 'inne',
	'Innfartsparkering': 'innfartsparkering',
	'Kirke': 'kirke',
	'KIWI': 'Kiwi',
	'Kjøpesenter': 'kjøpesenter',
	'Kundeparkering': 'kundeparkering',
	'Lufthavn': 'lufthavn',
	'Marina': 'marina',
	'Nedre': 'nedre',
	'Nord': 'nord',
	'Nytt': 'nytt',
	'Næringspark': 'næringspark',
	'Nærsenter': 'nærsenter',
	'P-hus': 'p-hus',
	'P-Hus': 'p-hus',
	'P-HUS': 'p-hus',
	'P-område': '',
	'P-plass': '',
	'P-Plass': '',
	'p-plass': '',
	'P-tomt': '',
	'P-sone': 'p-sone',
	'Plan': 'plan',
	'Plass': 'plass',
	'Parkering': '',
	'parkering': '',
	'Parkeringshus': 'p-hus',
	'Parkeringsplass': '',
	'parkeringsplass': '',
	'Parkering': '',
	'Senter': 'senter',
	'Skole': 'skole',
	'Sone': 'sone',
	'Stadion': 'stadion',
	'Stasjon': 'stasjon',
	'Stavkirke': 'stavkirke',
	'Storsenter': 'storsenter',
	'Studentboliger': 'studentboliger',
	'Studentby': 'studentby',
	'Syd': 'syd',
	'Sykehjem': 'sykehjem',
	'Sykehus': 'sykehus',
	'Sør': 'sør',
	'T-bane': 't-bane',
	'Tennisklubb': 'tennisklubb',
	'Terrasse': 'terrasse',
	'Torg': 'torg',
	'Torv': 'torv',
	'Ute': 'ute',
	'Uteområde': 'uteområde',
	'Uteparkering': 'uteparkering',
	'Utfartsparkering': 'utfartsparkering',
	'Ved': 'ved',
	'Veg': 'veg',
	'Vei': 'vei',
	'Vest': 'vest',
	'vgs': 'videregående skole',
	'VGS': 'videregående skole',
	'Vgs': 'videregående skole',
	'Videregående': 'videregående',
	'Øst': 'øst',
	'Øvre': 'øvre',
	'AS': '',
	'HF': ''
}

transform_operator = {
	'Q-park': 'Q-Park',
	'P-norge': 'P-Norge',
	'Apcoa': 'APCOA',
	'p-drift': 'P-drift',
	'norway': 'Norway',
	'norge': 'Norge',
	'nordic': 'Nordic',
	'arendal': 'Arendal',
	'Gc': 'GC',
	'rieber': 'Rieber',
	'halden': 'Halden',
	'bergen': 'Bergen',
	'jan': 'Jan',
	'jacobsen': 'Jacobsen',
	'jangaard': 'Jangaard',
	'griegsvei': 'Griegs vei',
	'øst': 'Øst',
	'sør': 'Sør',
	'vest': 'Vest',
	'nord': 'Nord',
	'd': 'D',
	'p': 'P',
	'hovedkontor': '',
	'avd': '',
	'as': '',
	'hf': '',
	'kf': '',
	'a/s': ''
}


# Produce a tag for OSM file

def make_osm_line (key,value):

	if value:
		encoded_key = html.escape(key).strip()
		encoded_value = html.escape(value).strip()
		file.write ('    <tag k="%s" v="%s" />\n' % (encoded_key, encoded_value))


# Output message

def message (line):

	sys.stdout.write (line)
	sys.stdout.flush()


# Main program

if __name__ == '__main__':

	# Load parking data from Statens Vegvesen

	message ("Loading data ...")

#	filename = "https://www.vegvesen.no/ws/no/vegvesen/veg/parkeringsomraade/parkeringsregisteret/v1/parkeringsomraade?datafelter=alle"
	filename = "https://parkreg-open.atlas.vegvesen.no/ws/no/vegvesen/veg/parkeringsomraade/parkeringsregisteret/v1/parkeringsomraade?datafelter=alle"
	file = urllib.request.urlopen(filename)
	parking_data = json.load(file)
	file.close()

	# Load county names from Kartverket/GeoNorge

	filename = "https://register.geonorge.no/api/sosi-kodelister/fylkesnummer.json?"
	file = urllib.request.urlopen(filename)
	county_data = json.load(file)
	file.close()

	county_name = {}
	for county in county_data['containeditems']:
		if county['status'] == "Gyldig":
			county_name[county['codevalue']] = county['label'].strip()

	# Load postal code to municipality code translation table from Posten/Bring, used to determine county (first two digits of municipality code)

	filename = "https://www.bring.no/postnummerregister-ansi.txt"
	file = urllib.request.urlopen(filename)
	postal_codes = csv.DictReader(TextIOWrapper(file, "cp1252"), fieldnames=['zip','post_city','municipality_ref','municipality','type'], delimiter="\t")

	municipality_id = [None] * 10000
	municipality_name = {}
	for row in postal_codes:
		municipality_id[int(row['zip'])] = row['municipality_ref']
		municipality_name[row['municipality_ref']] = row['municipality']  # .decode('cp1252')  # Windows ANSI coding

	file.close()

	# Get output filename

	filename = 'parkeringsregisteret.osm'
	
	if len(sys.argv) > 1:
		filename = sys.argv[1]

	file = open (filename, "w")

	# Produce OSM file header

	message ("\nConverting to file %s ..." % filename)

	file.write ('<?xml version="1.0" encoding="UTF-8"?>\n')
	file.write ('<osm version="0.6" generator="parking2osm v%s" upload="false">\n' % version)

	node_id = -1000
	number = 0
	no_municipality = 0
	no_county = 0

	# Loop all parking areas and produce OSM file

	for parking in parking_data:

		pdata = parking['aktivVersjon']

		if not(parking['deaktivert']) and (pdata['typeParkeringsomrade'] != "LANGS_KJOREBANE"):

			node_id -= 1
			number += 1

			fee_parking = 0
			free_parking = 0
			disabled_parking = 0
			charging = 0

			if pdata['antallAvgiftsbelagtePlasser']:
				fee_parking = pdata['antallAvgiftsbelagtePlasser']
			if pdata['antallAvgiftsfriePlasser']:
				free_parking = pdata['antallAvgiftsfriePlasser']
			if pdata['antallForflytningshemmede']:
				disabled_parking = pdata['antallForflytningshemmede']
			if pdata['antallLadeplasser']:
				charging = pdata['antallLadeplasser']

			# Fix parking name

			name = pdata['navn']
			if name == name.upper():
				name = name.title()

			name_split = name.split()
			name = ""
			for word in name_split:
				if word[-1] == ",":
					word_without_comma = word[:-1]
				else:
					word_without_comma = word
				if word_without_comma in transform_name:
					if transform_name[word_without_comma]:
						name += transform_name[word_without_comma] + " "
						if word[-1] == ",":
							name += ","
				else:
					name += word + " "

			name = name[0].upper() + name[1:].replace("  ", " ").replace("- -", "-").strip()

			# Fix operator name

			operator = parking['parkeringstilbyderNavn'].strip()
			operator = operator[0] + operator[1:].lower()

			operator_split = operator.split()
			operator = ""
			for word in operator_split:
				if word in transform_operator:
					operator += " " + transform_operator[word]
				else:
					operator += " " + word

			if operator.find("Avinor") >= 0:
				operator = "Avinor"

			operator = operator.replace("  ", " ").strip()

			# Generate tags

			file.write ('  <node id="%i" lat="%s" lon="%s">\n' % (node_id, parking['breddegrad'], parking['lengdegrad']))

			make_osm_line ("ref:pregister", str(parking['id']))
			make_osm_line ("operator", operator)
			make_osm_line ("name", name)
			make_osm_line ("capacity", str(fee_parking + free_parking))

			if disabled_parking > 0:
				make_osm_line ("capacity:disabled", str(disabled_parking))
			if charging > 0:
				make_osm_line ("capacity:charging", str(charging))

			if fee_parking > 0:
				make_osm_line ("fee", "yes")
			else:
				make_osm_line ("fee", "no")

			if pdata['innfartsparkering'] == "JA":
				make_osm_line ("park_ride", "yes")

			if name.find("utfartsparkering") >= 0:
				make_osm_line ("hiking", "yes")

			amenity = "parking"
			if pdata['typeParkeringsomrade'] == "PARKERINGSHUS":  # Mostly underground (some are multi-storey)
				make_osm_line ("parking", "underground")
				amenity = "parking_entrance"
			elif pdata['typeParkeringsomrade'] == "AVGRENSET_OMRADE":
				make_osm_line ("parking", "surface")
			elif pdata['typeParkeringsomrade'] == "LANGS_KJOREBANE":
				make_osm_line ("parking", "street")
			else:
				make_osm_line ("parking", pdata['typeParkeringsomrade'])

			make_osm_line ("amenity", amenity)

			# Generate extra tags for help during import

			make_osm_line ("AKTIVERINGSDATO", pdata['aktiveringstidspunkt'][0:10])
			make_osm_line ("OPPDATERTINGSDATO", pdata['sistEndret'][0:10])
			make_osm_line ("REFERANSE", pdata['referanse'])

			if free_parking >0:
				make_osm_line ("GRATISPLASSER", str(free_parking))
			if fee_parking >0:
				make_osm_line ("AVGIFTSPLASSER", str(fee_parking))

			if pdata['adresse']:
				make_osm_line ("ADRESSE", pdata['adresse'] + ", " + pdata['postnummer'] + " " + pdata['poststed'])
			else:
				make_osm_line ("ADRESSE", pdata['postnummer'] + " " + pdata['poststed'])

			if pdata['handhever']:
				operator = pdata['handhever']['navn'].strip()
				operator = operator[0] + operator[1:].lower()
				make_osm_line (u"HÅNDHEVER", operator)

			municipality = municipality_id[ int(pdata['postnummer']) ]
			if municipality in municipality_name:
				make_osm_line("KOMMUNE", municipality_name[municipality])
			else:
				no_municipality += 0
			if municipality[0:2] in county_name:
				make_osm_line ("FYLKE", county_name[ municipality[0:2] ])
			else:
				no_county += 0

			# Done with OSM node

			file.write ('  </node>\n')

	# Produce OSM file footer

	file.write ('</osm>\n')
	file.close()

	message ("\nParking areas: %i\n" % number)
	if no_county > 0:
		message ("Without county: %i\n" % no_county)
	if no_municipality > 0:
		message ("Without municipality: %i\n" % no_municipality)
