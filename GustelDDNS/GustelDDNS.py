'''
Created on 22.07.2020

@author: Dennis
'''
#System imports
import sys
import logging
#Project-Internal
from Cloudflare import domains
import config


#Root location of python program
#projectRoot = Path(__file__).parent.parent


def main():
    #SET logginglevel
        logging.basicConfig(level=logging.DEBUG)

        #Checks if domains.json exists, creates if not
        config.checkDomainsJSON()
        
        
        print(sys.argv)
        
        
        if sys.argv[1] == "-new":
            domains.domains()
        
        
        
        
        
        #TODO: load domains.json into list of domain-objects
    
    







    #TODO: Load existing domains into List of domains
    
    #Create new Domain (arg = -new)
    #if sys.argv[1] == "-new":
    #    newDomain = domain.domain(True)