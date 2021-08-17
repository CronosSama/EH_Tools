import subprocess
import optparse
import re


def mac_changer(interface,mac):           
        acts = ["down",f"hw ether {mac} ","up"]

        for act in acts : 
            subprocess.run(f"ifconfig {interface} {act} ",shell=True)
        checker(interface,mac)
   


def checker(interface,new_mac=False):
    # actual_mac = subprocess.run(f"ifconfig {interface} | grep ether | cut -d' ' -f10",shell=True,capture_output=True)
    # actual_mac = actual_mac.stdout.decode().strip()

    actual_mac = subprocess.run(f"ifconfig {interface} | grep ether",shell=True,capture_output=True)
    actual_mac = actual_mac.stdout.decode().strip()
    actual_mac = re.search("\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",actual_mac)
    
    if actual_mac :
        if str(actual_mac.group(0)) == str(new_mac) :
            print(f" {actual_mac.group(0)} ")
            print(f" {new_mac} ")
            print("the address was successfully changed !!! ")
        else : 
            print(f" {actual_mac.group(0)} ")
            print(f" {new_mac} ")
            print("the address wasn't succesfully changed !!! ")
    else : 
        print(" [-] we didn't find any mac address for this interface !! ")




def get_arguments() :
    parser = optparse.OptionParser()
    parser.add_option("-i","--interface",dest="interface",help="write the interface you want to change .")
    parser.add_option("-m","--mac",dest="mac",help="the new mac address . the first octet must be 00 .")
    #it will return a tuble , the first iterable is an object that have options as  keys and arguments as values
    # ig : { interface : "eth0" , mac : "00:11:22:33:44:55"} 
    (options,arguments) = parser.parse_args()
    if not options.interface : 
        parser.error("you forgot to put an interface id !!!")
    if not options.mac :
        parser.error("you forgot to put the new mac address !!! ")    
    else :
        
        return options
        
    






options = get_arguments()

mac_changer(options.interface,options.mac)















