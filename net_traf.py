import pygeoip
import dpkt 
import socket
import os

kml_header = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2"><Document>
    <Style id="yellowLineGreenPoly">
        <LineStyle>
            <color>7f00ffff</color>
            <width>4</width>
        </LineStyle>
        <PolyStyle>
            <color>7f00ff00</color>
        </PolyStyle>
    </Style>"""
kml_footer = "</Document></kml>\n"

geo_ip_file = os.path.join(os.path.dirname(__file__),"GeoLiteCity.dat")

gi = pygeoip.GeoIP(geo_ip_file)

def plotPcap(pcap):
    KMLpts = ''
    for (ts,buf) in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            srcKML = pointKMLcreate(src)
            dst = socket.inet_ntoa(ip.dst)
            dstKML = pointKMLcreate(dst)
            lineKML = lineKMLcreate(src,dst)
            KMLpts = KMLpts + srcKML + dstKML + lineKML
            # print("Source: {}\t-->\tDestination:{}".format(ipToLocation(src),ipToLocation(dst)))
        except:
            pass
    return KMLpts

def printRecord(tgt):
    rec = gi.record_by_name(tgt)
    # print(str(rec))
    city = rec['city']
    region = rec['region_code']
    country = rec['country_name']
    lng = rec['longitude']
    lat = rec['latitude']
    print("Target: {}\n{},{},{}\nLat:{}\tLong:{}".format(tgt, str(city), str(region), str(country), str(lat), str(lng)))

def ipToLocation(ip):
    try:
        rec = gi.record_by_name(ip)
        city = rec['city']
        region = rec['region_code']
        country = rec['country_code3']
        if city != '':
            loc = city + ',' + region + ',' + country
        else:
            loc = country
    except:
        loc = ip
    return loc

def lineKMLcreate(src,dst):
    src_rec = gi.record_by_name(src)
    dst_rec = gi.record_by_name(dst)
    try:
        src_longitude = src_rec['longitude']
        src_latitude = src_rec['latitude']
        dst_longitude = dst_rec['longitude']
        dst_latitude = dst_rec['latitude']

        kml = """\t<Placemark>
        <styleUrl>#yellowLineGreenPoly</styleUrl>
        <LineString>
            <extrude>1</extrude>
            <altitudeMode>relative</altitudeMode>
            <coordinates>%6f,%6f,10000
                %6f,%6f,10000
            </coordinates>
        </LineString>
    </Placemark>"""%(src_longitude,src_latitude,dst_longitude,dst_latitude)
    except Exception as e:
        # print(e)
        return ''
    return kml

def pointKMLcreate(ip):
    src_rec = gi.record_by_name(ip)
    try:
        longitude = src_rec['longitude']
        latitude = src_rec['latitude']
        kml = """
    <Placemark>
        <name>%s</name>
        <Point>
            <coordinates>%6f,%6f</coordinates>
        </Point>
    </Placemark>"""%(ip,longitude,latitude)
    except:
        return ''
    return kml

if __name__ == "__main__":
#     kml_string = ''
#     with open(os.path.join(os.path.dirname(__file__),"test.pcap")) as pcap_file:
#         print(pcap_file)
#         pcap = dpkt.pcap.Reader(pcap_file)
#         kml_string = plotPcap(pcap)
#     with open(os.path.join(os.path.dirname(__file__),"capture.kml"), 'w') as kml_file:
#         kml_file.write(kml_header + kml_string + kml_footer)
#         # printPcap(pcap)

    src = '128.128.111.151'
    dst = '128.198.111.150'
    with open(os.path.join(os.path.dirname(__file__),"capture.kml"), 'w') as kml_file:
        kml_file.write(kml_header+pointKMLcreate(src)+pointKMLcreate(dst)+lineKMLcreate(src,dst)+kml_footer)
