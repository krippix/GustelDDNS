'''
Created on 22.07.2020

@author: Dennis
'''
#System imports
import sys
#Project-Internal
from DDNS.Cloudflare import domain



#print(sys.argv) returns list of arguments

#TODO: Load existing domains into List of domains

#Create new Domain (arg = -new)
if sys.argv[1] == "-new":
    newDomain = domain.domain(True)
    
