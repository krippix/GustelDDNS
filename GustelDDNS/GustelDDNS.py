'''
Created on 22.07.2020

@author: Dennis
'''
#System imports
import sys
import logging
import json
#Project-Internal
import domains
import config


#Root location of python program
#projectRoot = Path(__file__).parent.parent


def main():
    logging.debug("GustelDDNS.main()")
    
    #Check if Folder "data" exist, create if not
    config.checkDataFolder()
    
    #Pulls location of domains.json from config.py
    domainsJSON = config.getDomainsJSON()
    
    #Checks if "domains.json" exists, creates if not
    config.checkDomainsJSON()
    
    #Print arguments for testing
    #print(sys.argv)
      
    #Example of Dict: 'example.com': {'A': {'xAuthKey': '123xxx123xxx','email': 'user@example.com', 'zoneID': '123123123'}}
    
    
    #Loading domains.json into domains_dict. If it fails, create empty dict
    try:
        domains_dict = loadDomains(domainsJSON)
    except Exception as e:
        logging.error(str(e))
        domains_dict = {}
        exit()
    
    
    #Check Startup arguments
    #TODO: This is trash make again
 
    try:
        if sys.argv[1] == "-new":
            domains.createNewDomain(domains_dict)


        elif sys.argv[1] == "-update":
            domains.updateDDNSdomains(domains_dict)
    except Exception as e:
        logging.error("Argument missing or not found!")
        logging.debug("Argument missing or not found: "+str(e))

    


                
    #Finishes by writing everything to domains.json
    writeDomains(domainsJSON, domains_dict)
    logging.info("done!")  
    


def loadDomains(domainsJSON):
    logging.debug("GustelDDNS.loadDomains()")
    logging.info("Loading Domains...")
    
    with open(domainsJSON) as json_file:
        data = json.load(json_file)
        return data



def writeDomains(domainsJSON, data):
    #Writes Dict to domains.json
    logging.debug("GustelDDNS.writeDomains()")
    logging.debug("writeDomainsJSON")
    logging.info("Writing Domains...")
    
        
    with open(domainsJSON, 'w') as json_file:
        json.dump(data, json_file, indent=4)


