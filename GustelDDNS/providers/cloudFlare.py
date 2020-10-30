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
from importlib._bootstrap_external import ExtensionFileLoader

#domainsFilePath = str(projectRoot) + os.sep +'data'+ os.sep +'domains.json'


def createNewDomain(domains_dict, domain, recordType):
    #Create CloudFlare Domain (locally)
    logging.debug("GustelDDNS.providers.cloudFlare.createNewDomain()")
    
    #Ask For xAuthKey and 
    xAuthKey = input("Enter xAuthKey: ")
    email = input("Enter E-Mail: ")        
    
    
    #Retrieve ZoneID for domain
    zoneID = requestZoneID(domain, xAuthKey, email)
    
    #Retrieve RecordID for (sub)domain
    recordID = requestRecordID(domain, xAuthKey, email, zoneID)

    #Write everything into domains_dict
    domains_dict[domain] = {recordType: {'xAuthKey': xAuthKey, 'email': email, 'zoneID': zoneID, 'recordID': recordID, 'DDNS': enable_DDNS}}   

    return domains_dict



def requestZoneID(domain, xAuthKey, email):
    #Get ZoneID from main domain
    logging.debug("GustelDDNS.providers.cloudFlare.requestZoneID()")
    
    #Remove Subdomains
    domain = simpleTools.removeSubDomains(domain)     
          
    
    #Curl request
    headers = {
        'X-Auth-Email': email,
        'X-Auth-Key': xAuthKey,
        'Content-Type': 'application/json',
    }
        
    response = requests.get('https://api.cloudflare.com/client/v4/zones?name='+domain, headers=headers)
    logging.debug(str(response.json))  
    data = response.json()

    
    #Check for Success
    if str(response) == "<Response [200]>":
        logging.info("Succesfully retrieved ZoneID!")
        
        return str(data["result"][0]["id"])
    
    else:
        logging.error("Failed to retrieve ZoneID: "+str(data["result"][0]["id"]))
        exit()
            
            
                
def requestRecordID(domain, xAuthKey, email, zoneID):            
    #Get record ID for domain / subdomain
    logging.debug("GustelDDNS.providers.cloudFlare.requestRecordID()")
    
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
        logging.error("Requesting RecordID failed: "+ str(response))        



def updateIPadress(xAuthKey, email, zoneID, recordID, domain, currentPubIPv4):
    #Updates IP of record
    logging.debug("GustelDDNS.providers.cloudFlare.updateIPadress()")
    
    #Retrieve current IP of record
    headers = {
        'X-Auth-Email': email,
        'X-Auth-Key': xAuthKey,
        'Content-Type': 'application/json',
    }
    
    
    logging.info(domain+" - Retrieving current Record-IP...")
    try:
        response = requests.get('https://api.cloudflare.com/client/v4/zones/'+zoneID+'/dns_records/'+recordID, headers=headers)
        logging.debug(str(response))  
        data = response.json()
    except Exception as e:
        logging.error(domain+" - Failed to retrieve Record-IP: "+e)
    
    
    if str(response) == "<Response [200]>":
        #Check Retrieved IP-Address
        try:
            recordIPv4 = str(data['result']['content'])
            logging.info(domain+" - Current Record IP: "+recordIPv4)
        
        except Exception as e:
            logging.error(domain+"- Failed to retrieve current Record IPv4 address: "+str(e))
            return

    else:
        logging.error(domain+" - Failed to retrieve Record-IP: "+str(response))
        return
    
    

    #Check if record IP matches current Public IP-Address
    if currentPubIPv4 == recordIPv4:
        logging.info(domain+" - IP address remains "+currentPubIPv4)
        return
    
    #Attempt to update DNS-Record
    else:
        try:
            logging.info(domain+" - Updating Record IP...")
            payload = {'type':'A','name': domain,'content': currentPubIPv4}
            
            response = requests.put('https://api.cloudflare.com/client/v4/zones/'+zoneID+'/dns_records/'+recordID, headers=headers, data = json.dumps(payload))
            print(response.text)
            logging.info(str(response))
            
        except Exception as e:
            logging.error(domain+"- Failed to Update DNS-Record: "+str(e))
            return
        
        if str(response) == "<Response [200]>":
            logging.info("Success!")
        else:
            logging.error(domain+" - Updating failed: "+str(response))
    
    
  
            
            
            
            
        
        
            
        
