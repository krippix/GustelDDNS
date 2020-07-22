'''
Created on 22.07.2020

@author: Dennis
'''

class domain:
    def __init__(self,create):
        
        if create == True:
            self.createDomain()
            
        elif create == False:
            importDomain()
        
        
   
        
    def createDomain(self):    
        
        self.domain = input("Enter Domain: ")
        self.xAuthKey = input("Enter xAuthKey: ")
        self.email = input("Enter E-Mail: ")
    