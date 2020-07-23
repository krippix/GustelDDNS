'''
Created on 22.07.2020

@author: Dennis
'''
#System imports
import os
import sys
import logging
from pathlib import Path
#Project-Internal
from DDNS.Cloudflare import domain
from DDNS import config


#Root location of python program
#projectRoot = Path(__file__).parent.parent



class DDNS:    
    '''
    print(sys.argv) returns list of arguments
    '''
    
    def __init__(self):
        #SET logginglevel
        logging.basicConfig(level=logging.DEBUG)
    
        #Parse config.ini
        
    
        #Check for domains.json
        #domainsFilePath = str(projectRoot) + os.sep +'data'+ os.sep +'domains.json'
        domainsFilePath = config.readinifile("domains", "domaindata")
        print(domainsFilePath)
        
        
        #Checks if domains.json exists, creates if not
        if Path(domainsFilePath).exists():
            logging.info("domains.json found!")
        else:
            logging.warning("domains.json not found!")
            logging.info("Creating new domains.json")
            
            try:
                domainsFile = open(domainsFilePath, "x")
                logging.info("domains.json created!")
            except Exception as e:
                logging.error("Failed to create domains.json: "+str(e))
                exit()
            
        
        logging.info("Checking for domains.json")
        
        
        #TODO: load domains.json into list of domain-objects
    
    







    #TODO: Load existing domains into List of domains
    
    #Create new Domain (arg = -new)
    #if sys.argv[1] == "-new":
    #    newDomain = domain.domain(True)
        
