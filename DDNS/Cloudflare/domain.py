'''
Created on 22.07.2020

@author: Dennis
'''

import json
import logging
from pathlib import Path


from DDNS import config
from DDNS import simpleTools

#domainsFilePath = str(projectRoot) + os.sep +'data'+ os.sep +'domains.json'



class domain:
    #newDomain: Create or Load, domainNo in case newDomain is true
    
    
    def __init__(self,newDomain):
        logging.debug("domain __init__")
        
        #Pulls location of domains.json from config.py
        self.domainsJSON = config.getDomainsJSON()
        
        #TODO: Check if domains.json exists
        
        #Example of Dict: 'example.com': {'A': {'xAuthKey': '123xxx123xxx','email': 'user@example.com'}}
        
        #Loading domains.json into domains_dict
        self.domains_dict = self.loadDomains()
        
        #Creates new Domain in case Parameter has been passed
        if newDomain:
            self.createNewDomain()
        
        #Finishes by writing everything to domains.json
        self.writeDomainsJSON(self.domains_dict)   
        
        logging.debug("class domains: done!")
    
    def createDomainsJSON(self):
        logging.debug("createDomainsJSON")
        print("lel")    

    
    def loadDomains(self):
        logging.debug("loadDomains")
        logging.info("Loading Domains...")
        
        with open(self.domainsJSON) as json_file:
            data = json.load(json_file)
            return data
    
    def writeDomainsJSON(self, data):
        logging.debug("writeDomainsJSON")
        logging.info("Writing Domains...")
        #Writes Dict to domains.json
        
        with open(self.domainsJSON, 'w') as json_file:
            json.dump(data, json_file, indent=4)
    
    def createNewDomain(self):    
        
        domain = input("Enter Domain: ")
        #Cancel Creation if domain shouldnt be overwritten
        if domain in self.domains_dict:
            if not simpleTools.query_yes_no("{}{}".format(domain, "already Exists, do you want to override it?")):
                print("Domain creation cancelled.")
                exit()
            
        
        
        recordType = input("Enter record Type: ")
        xAuthKey = input("Enter xAuthKey: ")
        email = input("Enter E-Mail: ")
        
        
        
        self.domains_dict[domain]= {recordType: {'xAuthKey': xAuthKey, 'email': email}}
        
            
        
