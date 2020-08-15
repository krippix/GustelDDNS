'''
Created on 22.07.2020

@author: Dennis
'''
#System imports
import json
import logging
import sys

#Part of Project
import config
import simpleTools

#External Imports
import requests

#domainsFilePath = str(projectRoot) + os.sep +'data'+ os.sep +'domains.json'


class domains:
    #newDomain: Create or Load, domainNo in case newDomain is true
    
    
    def __init__(self):
        logging.debug("domain __init__")
        
        #Variables
        self.domain = ""
        self.recordType = ""
        self.xAuthKey = ""
        self.email = ""
        self.zoneID = ""
        self.recordID = ""
        
        #Pulls location of domains.json from config.py
        self.domainsJSON = config.getDomainsJSON()
        #Example of Dict: 'example.com': {'A': {'xAuthKey': '123xxx123xxx','email': 'user@example.com', 'zoneID': '123123123'}}
        
        #Loading domains.json into domains_dict
        try:
            self.domains_dict = self.loadDomains()
        except Exception as e:
            logging.error(str(e))
            self.domains_dict = {}
        
        if sys.argv[1] == "-new":
            self.createNewDomain()
        
        
        
        
        
        
        
        
            
        
        #Finishes by writing everything to domains.json
        self.writeDomains(self.domains_dict)   
        
        logging.debug("class domains: done!")
    
    
    def loadDomains(self):
        logging.info("Loading Domains...")
        
        with open(self.domainsJSON) as json_file:
            data = json.load(json_file)
            return data
    
    def writeDomains(self, data):
        logging.debug("writeDomainsJSON")
        logging.info("Writing Domains...")
        #Writes Dict to domains.json
        
        with open(self.domainsJSON, 'w') as json_file:
            json.dump(data, json_file, indent=4)
            
    def createNewDomain(self):    
        
        self.domain = input("Enter Domain: ")
        self.recordType = input("Enter record Type: ")
                
        #Check if domain and RecordType already exists
        try: 
            if self.domain in self.domains_dict and self.recordType in self.domains_dict[self.domain]:
    
                #Check if you want to override existing entry
                if not simpleTools.query_yes_no("{}{}{}{}{}".format("Record type: ",self.recordType, " already Exists for '",self.domain,"', do you want to override it?")):
                    print("Domain creation cancelled.")
                    exit()
        except Exception as e:
            logging.error(str(e))
        
        #Continue with domain creation
        self.xAuthKey = input("Enter xAuthKey: ")
        self.email = input("Enter E-Mail: ")        
        
        
        #Retrieve ZoneID for domain
        self.zoneID = requestZoneID(self.domain, self.xAuthKey, self.email)
        
        #Retrieve RecordID for (sub)domain
        self.recordID = requestRecordID(self.domain, self.xAuthKey, self.email, self.zoneID)
        
        
        #Write everything into domains_dict
        self.domains_dict[self.domain]= {self.recordType: {'xAuthKey': self.xAuthKey, 'email': self.email, 'zoneID': self.zoneID, 'recordID': self.recordID}}      
                
                

def requestZoneID(domain, xAuthKey, email):
    #Get ZoneID from main domain
    
    #Remove Subdomains
    domain = simpleTools.removeSubDomains(domain)     
          
    
    
    headers = {
        'X-Auth-Email': email,
        'X-Auth-Key': xAuthKey,
        'Content-Type': 'application/json',
    }
        
    response = requests.get('https://api.cloudflare.com/client/v4/zones?name='+domain, headers=headers)
    logging.debug(str(response.json))  
    data = response.json()

    
    #Sucess!
    if str(response) == "<Response [200]>":
        logging.info("Succesfully retrieved ZoneID!")
        
        return str(data["result"][0]["id"])
    
    else:
        print("rip in peace")
            
                
def requestRecordID(domain, xAuthKey, email, zoneID):            
    #Get record ID for domain / subdomain
    
    headers = {
        'X-Auth-Email': email,
        'X-Auth-Key': xAuthKey,
        'Content-Type': 'application/json',
    }
        
    response = requests.get('https://api.cloudflare.com/client/v4/zones/'+zoneID+'/dns_records?name='+domain, headers=headers)
    logging.debug(str(response.json))  
    data = response.json()

    
    #Sucess!
    if str(response) == "<Response [200]>":
        logging.info("Succesfully retrieved ZoneID!")
        
        return str(data["result"][0]["id"])
    
    else:
        print("rip in peace")        
            
        
        
        
        
        
        
        
            
        
