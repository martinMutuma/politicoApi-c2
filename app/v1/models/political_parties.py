"""App/v1/models/political_parties.py"""
from app.v1.models.base_model import BaseModel

partiesList = []

class Party(BaseModel):

    def __init__(self, name, hqAddress, logoUrl, id=0):
        self.name = name
        self.hqAddress = hqAddress
        self.logoUrl = logoUrl
        self.id = id
    
    def party_dictionary(self):
        return dict(id=self.id, name=self.name,
                    hqAddress=self.hqAddress, logoUrl=self.logoUrl)
    def update_name(self, name):
        self.name = name