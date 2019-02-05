from app.v1.models.base_model import BaseModel

officeList = {}
officeTypes = ['federal', 'legislative', 'state', 'local government']


class OfficeModel(BaseModel):
    '''Represents an office, with a name.'''

    def __init__(self, name, type, id=0):
        self.id = self.generate_id()
        self.type = type  # federal, legislative, state, or local government
        self.name = name

    def generate_id(self, id=0):
        if id == 0:
            id = len(officeList)+1

        if id in officeList:
            id = id+1
            return self.generate_id(id)
        return id

    def get_details(self):
        return dict(id=self.id, name = self.name, type = self.type)

    def save_office(self):
        officeList[self.id] = self

    def delete_party(self):
        del officeList[self.id]

    def check_name_exists(self, name=None):
        if name == None:
            name = self.name
        for i in officeList:
            if officeList[i].name == name:
                return i
        return False
