import scapy.all as scapy
import optparse

parser = optparse.OptionParser()
parser.add_option("-n","--network",dest = "network",help = "specify the network address with /prefix-length")
options = parser.parse_args()[0]

def scan(ip) : 
    arp_request = scapy.ARP(pdst = ip)

    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request


    # arp_request_broadcast.show()
    #it returns 2 lists
    # answered, unanswered = scapy.srp(arp_request_broadcast,timeout = 1)
    #we are just getting the answered ones
    answered_list = scapy.srp(arp_request_broadcast,timeout = 1)[0]
    scapy.wireshark(answered_list)
    print("IP address :\t\t\t\tMac Address : \n")
    map_IP_MAC = []
    for ans in answered_list :
        entry = {"ip":f"{ans[1].psrc}","mac":f"{ans[1].hwsrc}"}
        ip = entry["ip"]
        mac = entry["mac"]
        print(f"+ {ip}\t\t\t\t{mac}\n ") 
        map_IP_MAC.append(entry)
    return map_IP_MAC

lists = scan(options.network)

print(lists)











