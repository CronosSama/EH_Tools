import optparse
import subprocess
import re 


parser = optparse.OptionParser()
parser.add_option("-i","--interface",help = "the interface id ")
parser.add_option("-a","--address", help = "the adress IP/Length ")

(options,arguments) = parser.parse_args()

