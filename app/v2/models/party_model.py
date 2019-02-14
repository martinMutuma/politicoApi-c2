"""App/v2/models/party_model.py"""
from app.v2.models import BaseModel




class PartyModel(BaseModel):
    """The Party Model"""
    table_name = "parties"
    sub_set_cols = ['id','name', 'hqAddress', 'logoUrl']
    def __init__(self):
        """Party create
        Arguments:
            name {[string]}
            hqAddress {[string]}
            logoUrl {[string]}

        """
        super(PartyModel, self).__init__()

    def create(self, name, hqAddress, logoUrl):
        """[summary]

         Arguments:
             name {[str]} -- [name od party]
             hqAddress {[str]} -- [party address]
             logoUrl {[type]} -- [logo url for the party]
         """
        self.name = name
        self.hqAddress = hqAddress
        self.logoUrl = logoUrl
       


    

