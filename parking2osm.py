#!/usr/bin/env python
# -*- coding: utf8

# parking2osm v1.0.0
# Converts parkering areas from Statens Vegvesen api feed to osm format for import/update
# Usage: python parking2osm.py [output_filename.osm]
# Default output filename: "parkeringsregisteret.osm"


import urllib2
import cgi
import csv
import json
import sys


transform_name = {
	'Alle': u'allé',
	'AMFI': 'Amfi',
	'Barnehage': 'barnehage',
	'Boligsameie': 'boligsameie',
	'Brygge': 'brygge',
	'Borettslag': 'borettslag',
	'brl': 'borettslag',
	'Butikksenter': 'butikksenter',
	'Ekspressparkering': 'ekspressparkering',
	'Gammel': 'gammel',
	'Gammelt': 'gammelt',
	'Gate': 'gate',
	'Garasje': 'garasje',
	'Gjesteparkering': 'gjesteparkering',
	'Gravplass': 'gravplass',
	'Hagesenter': 'hagesenter',
	'Havn': 'havn',
	'HUS': 'hus',
	u'Høgfjellstove': u'høgfjellstove',
	'Idrettshall': 'idrettshall',
	'Idrettspark': 'idrettspark',
	'Inne': 'inne',
	'INNE': 'inne',
	'Innfartsparkering': 'innfartsparkering',
	'Kirke': 'kirke',
	u'Kjøpesenter': u'kjøpesenter',
	'Kundeparkering': 'kundeparkering',
	'Lufthavn': 'lufthavn',
	'Marina': 'marina',
	'Nedre': 'nedre',
	'Nord': 'nord',
	'Nytt': 'nytt',
	u'Næringspark': u'næringspark',
	u'Nærsenter': u'nærsenter',
	'P-hus': 'p-hus',
	'P-Hus': 'p-hus',
	'P-HUS': 'p-hus',
	'P-plass': 'p-plass',
	'P-Plass': 'p-plass',
	'P-sone': 'p-sone',
	'Plan': 'plan',
	'Plass': 'plass',
	'Parkeringshus': 'parkeringshus',
	'Parkeringsplass': 'parkeringsplass',
	'Parkering': 'parkering',
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
	u'Sør': u'sør',
	'T-bane': 't-bane',
	'Tennisklubb': 'tennisklubb',
	'Terrasse': 'terrasse',
	'Torg': 'torg',
	'Torv': 'torv',
	'Ute': 'ute',
	u'Uteområde': u'uteområde',
	'Uteparkering': 'uteparkering',
	'Utfartsparkering': 'utfartsparkering',
	'Ved': 'ved',
	'Veg': 'veg',
	'Vei': 'vei',
	'Vest': 'vest',
	'vgs': u'videregående skole',
	'VGS': u'videregående skole',
	u'Videregående': u'videregående',
	u'Øst': u'øst',
	u'Øvre': u'øvre',
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
	u'øst': u'Øst',
	u'sør': u'Sør',
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
		encoded_key = cgi.escape(key.encode('utf-8'),True)
		encoded_value = cgi.escape(value.encode('utf-8'),True)
		file.write ('    <tag k="%s" v="%s" />\n' % (encoded_key, encoded_value))


# Output message

def message (line):

	sys.stdout.write (line)
	sys.stdout.flush()


# Main program

if __name__ == '__main__':

	# Load parking data from Statens Vegvesen

	message ("Reading data ...")

	filename = "https://www.vegvesen.no/ws/no/vegvesen/veg/parkeringsomraade/parkeringsregisteret/v1/parkeringsomraade?datafelter=alle"
	file = urllib2.urlopen(filename)
	parking_data = json.load(file)
	file.close()

	# Read postal code to municipality code translation table used to determine county (first two digits of municipality code)

	county_name = [None] * 51
	county_name[1] = u'Østfold'
	county_name[2] = 'Akershus'
	county_name[3] = 'Oslo'
	county_name[4] = 'Hedmark'
	county_name[5] = 'Oppland'
	county_name[6] = 'Buskerud'
	county_name[7] = 'Vestfold'
	county_name[8] = 'Telemark'
	county_name[9] = 'Aust-Agder'
	county_name[10] = 'Vest-Agder'
	county_name[11] = 'Rogaland'
	county_name[12] = 'Hordaland'
	county_name[14] = 'Sogn og Fjordane'
	county_name[15] = u'Møre og Romsdal'
	county_name[50] = u'Trøndelag'
	county_name[18] = 'Nordland'
	county_name[19] = 'Troms'
	county_name[20] = 'Finnmark'
	county_name[21] = 'Svalbard'
	county_name[22] = 'Jan Mayen'

	postal_file = urllib2.urlopen('https://www.bring.no/postnummerregister-ansi.txt')
	postal_codes = csv.DictReader(postal_file, fieldnames=['zip','post_city','municipality_ref','municipality','type'], delimiter="\t")
	municipality_id = [None] * 10000
	for row in postal_codes:
		municipality_id[int(row['zip'])] = row['municipality_ref']
	postal_file.close()

	# Get output filename

	filename = 'parkeringsregisteret.osm'
	
	if len(sys.argv) > 1:
		filename = sys.argv[1]

	file = open (filename, "w")

	# Produce OSM file header

	message ("\nConverting to file %s ..." % filename)

	file.write ('<?xml version="1.0" encoding="UTF-8"?>\n')
	file.write ('<osm version="0.6" generator="parking2osm v1.0.0" upload="false">\n')

	node_id = -1000
	number = 0
	no_county = 0

	# Loop all parking areas and produce OSM file

	for parking in parking_data:

		pdata = parking['aktivVersjon']

		if pdata['typeParkeringsomrade'] != "LANGS_KJOREBANE":

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
			name = name_split[0]
			for word in name_split[1:]:  # Skip first word
				if word[-1] == ",":
					word_without_comma = word[:-1]
				else:
					word_without_comma = word
				if word_without_comma in transform_name:
					if transform_name[word_without_comma]:
						name += " " + transform_name[word_without_comma]
						if word[-1] == ",":
							name += ","
				else:
					name += " " + word

			name = name.replace("  ", " ").strip()

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

			make_osm_line ("amenity", "parking")
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

			if pdata['typeParkeringsomrade'] == "PARKERINGSHUS":  # Mostly underground (some are multi-storey)
				make_osm_line ("parking", "underground")
			elif pdata['typeParkeringsomrade'] == "AVGRENSET_OMRADE":
				make_osm_line ("parking", "surface")
			elif pdata['typeParkeringsomrade'] == "LANGS_KJOREBANE":
				make_osm_line ("parking", "street")
			else:
				make_osm_line ("parking", pdata['typeParkeringsomrade'])

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

			county = county_name[ int(municipality_id[ int(pdata['postnummer']) ][0:2])]
			if county:
				make_osm_line ("FYLKE", county)
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
