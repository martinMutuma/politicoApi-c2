from app.v1.models.base_model import BaseModel

officeList = {}
officeTypes = ['federal', 'legislative', 'state', 'local government']


class OfficeModel(BaseModel):
    '''Represents an office, with a name.'''

    def __init__(self, name, type, id=0):
        self.id = self.generate_id(officeList)
        self.type = type  # federal, legislative, state, or local government
        self.name = name

    def get_details(self):
        """Get all attributes of the object
        
        Returns:
            [dict] 
        """

        return dict(id=self.id, name=self.name, type=self.type)

    @staticmethod
    def search_office_by_id(id):
        """search for a certain id in the officelist
        
        Arguments:
            id {[int]} -- id to search for
        
        Returns:
            [object office] -- [if found an the office object is returned]
            [bool false] --- if the office id not found
        """

        if id in officeList:
            return officeList[id]
        return False

    def save_office(self):
        """
        Insert the object into the list of parties
        """

        officeList[self.id] = self

    def delete(self):
        del officeList[self.id]


    def update(self, name, type=False):
        self.name = name
        if type:
            self.type = type


   