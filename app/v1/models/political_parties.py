"""App/v1/models/political_parties.py"""
from app.v1.models.base_model import BaseModel

partiesList = {}


class PartyModel(BaseModel):
    """The Party Model"""

    def __init__(self, name, hqAddress, logoUrl, id=0):
        self.name = name
        self.hqAddress = hqAddress
        self.logoUrl = logoUrl
        self.id = self.generate_id()
       


    def party_dictionary(self):
        return dict(id=self.id, name=self.name,
                    hqAddress=self.hqAddress, logoUrl=self.logoUrl)

    def name_and_id(self):
        return dict(id=self.id, name=self.name)
    
    def get_details(self):
          return dict(id=self.id, name=self.name, logoUrl=self.logoUrl)

    def update_name(self, name):
        self.name = name
        


    def generate_id(self, id=0):
        if id == 0:
            id = len(partiesList)+1

        if id in partiesList:
            id = id+1
            return self.generate_id(id)
        return id


    def save_party(self):
        partiesList[self.id] = self


    def delete_party(self):
        del partiesList[self.id]

    def check_name_exists(self, name=None):
        if name == None:
            name = self.name
        for i in partiesList:
            if partiesList[i].name == name:
                 return i
        return False
