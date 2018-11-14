from scapy.all import sniff
import net_traf
import time
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

def realtime_print(packet):
    try:
        socket.inet_aton(packet[0][1].src)
        socket.inet_aton(packet[0][1].dst)
    except:
        return
    src = packet[0][1].src
    dst = packet[0][1].dst
    realtime_KMLwrite(src,dst)
    return "Source: {}\t-->\tDestination:{}".format(net_traf.ipToLocation(src),net_traf.ipToLocation(dst))

def realtime_KMLwrite(src,dst):
    kml_string = ''
    kml_string += net_traf.pointKMLcreate(src)
    kml_string += net_traf.pointKMLcreate(dst)
    kml_string += net_traf.lineKMLcreate(src,dst)
    with open(os.path.join(os.path.dirname(__file__),"capture.kml"), 'a') as kml_file:
        kml_file.write(kml_string)

with open(os.path.join(os.path.dirname(__file__),"capture.kml"), 'w') as kml_file:
    kml_file.write(kml_header)

sniff(count=100,prn=realtime_print)

with open(os.path.join(os.path.dirname(__file__),"capture.kml"), 'a') as kml_file:
    kml_file.write(kml_footer)