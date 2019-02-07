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
        return dict(id=self.id, name=self.name, type=self.type)

    @staticmethod
    def search_office_by_id(id):
        if id in officeList:
            return officeList[id]
        return False

    def save_office(self):
        officeList[self.id] = self

    def delete(self):
        del officeList[self.id]

    def check_name_exists(self, name=None):
        if name == None:
            name = self.name
        for i in officeList:
            if officeList[i].name == name:
                return i
        return False

    def update(self, name, type=False):
        self.name = name
        if type:
            self.type = type


   