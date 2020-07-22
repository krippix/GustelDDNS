'''
Created on 22.07.2020

@author: Dennis
'''
#System imports
import sys
#Project-Internal
from DDNS import Cloudflare
from DDNS.Cloudflare import createDomain



#print(sys.argv) returns list of arguments



#Create new Domain
'''
Required Data to get all Domain Information:

- Domain
- xAuthKey
- E-Mail
'''

print(createDomain.setDomain())