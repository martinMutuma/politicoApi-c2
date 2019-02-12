"""App/v1/models/political_parties.py"""
from app.v1.models.base_model import BaseModel

partiesList = {}


class PartyModel(BaseModel):
    """The Party Model"""

    def __init__(self, name, hqAddress, logoUrl, id=0):
        """Party create
        Arguments:
            name {[string]} 
            hqAddress {[string]} 
            logoUrl {[string]} 
        
        """
        self.name = name
        self.hqAddress = hqAddress
        self.logoUrl = logoUrl
        self.id = self.generate_id(partiesList)
       


    def party_dictionary(self):
        """coverts the object attribute to a dict
        
        Returns:
            [dict] -- [of the desired object attribs]
        """

        return dict(id=self.id, name=self.name,
                    hqAddress=self.hqAddress, logoUrl=self.logoUrl)

    def name_and_id(self):
        """ Creates a subset dict of object atribs
        
        Returns:
            [dict] 
        """

        return dict(id=self.id, name=self.name)
    
    def get_details(self):
        """get all attris of the object
        
        Returns:
            [dict] -- [of the desired object attribs]
        """
        return dict(id=self.id, name=self.name, logoUrl=self.logoUrl)

    def update_name(self, name):
        """a setter to updatate the name attrib of the object
        
        Arguments:
            name {[type]} -- [description]
        """

        self.name = name


    def save_party(self):
        """
        Insert the object into the list of parties 
        """

        partiesList[self.id] = self


    def delete_party(self):
        """remove the object from the list of parties
        
        Returns:
            [dict] -- [updated list of parties]
        """

        del partiesList[self.id]
        return partiesList

