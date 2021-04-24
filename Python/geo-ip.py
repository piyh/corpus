import geoip2.database
import csv

GeoIPReader = geoip2.database.Reader('GeoLite2-City.mmdb')

extract = []

with open('ip-with-occur-count.txt') as iplist:
	ipCSV = csv.reader(iplist, delimiter=',', quotechar='"')
	for count, line in enumerate(ipCSV):
		try:
			ipinfo = GeoIPReader.city(line[0].rstrip())
			extract.append((line[0].rstrip(), str(ipinfo.city.name), \
				str(ipinfo.subdivisions.most_specific.name),  \
				str(ipinfo.country.name), str(ipinfo.location.latitude), \
				str(ipinfo.location.longitude), line[1]))
		except Exception, e: extract.append((line[0].rstrip(), 'Error', 'Error', 'Error', 'Error', 'Error', 'Error'))

#begin piecing together json
print "var citymap = {"
for row in extract:
	print "\t\"" + row[0] + "\": {"
	print "\t\tcenter: { lat: " + row[4] + ", lng: " + row[5] + "},"
	print "\t\trequests: " + row[6] + "},"
print "};"

