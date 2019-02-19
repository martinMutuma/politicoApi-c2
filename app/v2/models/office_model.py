from app.v2.models import BaseModel
import os
officeTypes = ['federal', 'legislative', 'state', 'local government']


class OfficeModel(BaseModel):
    '''Represents an office, with a name.'''
    sub_set_cols = ['id', 'name', 'type']
    table_name = "offices"

    def __init__(self):
        super(OfficeModel, self).__init__()
        print(os.getenv('FLASK_ENV'))

    def create_office(self, name, type):
        """Create new office

        Returns:
            [dict]
        """
        self.type = type  # federal, legislative, state, or local government
        self.name = name
