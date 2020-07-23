'''
Created on 22.07.2020

@author: Dennis
'''

import json

#domainsFilePath = str(projectRoot) + os.sep +'data'+ os.sep +'domains.json'

class domain:
    #newDomain: Create or Load, domainNo in case newDomain is true
    
    def __init__(self,newDomain,domainNo=None):
        
        if newDomain:
            self.createNewDomain()
            
        elif not newDomain and domainNo is not None:
            self.importDomain(domainNo)

        
    def createNewDomain(self):    
        
        self.domain = input("Enter Domain: ")
        self.xAuthKey = input("Enter xAuthKey: ")
        self.email = input("Enter E-Mail: ")
        
        domainsFile = open(DomainsFilePath, "a")
    
    
    
    
    def importDomain(self,domainNo):
        self.domain = ""
        self.xAuthKey = ""
        self.email = ""