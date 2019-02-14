from app.v2.models import BaseModel


class UserModel(BaseModel):
    """User management 

    Arguments:
        BaseModel --- Base class 
    """
    table_name = "users"
    def __init__(self):
        super(UserModel, self).__init__()

    def create_user(self, user_dict={}):
        """Creates a user 

        Arguments:
            firstname {[type]} -- [description]
            lastname {[type]} -- [description]
            othername {[type]} -- [description]
            email {[type]} -- [description]
            phonenumber {[type]} -- [description]
            passporturlstring {[type]} -- [description]

        Keyword Arguments:
            isadmin {bool} -- [description] (default: {False})
        """
        clean_user_dict = self.clean_insert_dict(user_dict)
        self.firstname = clean_user_dict['firstname']
        self.lastname = clean_user_dict['lastname']
        self.othername = clean_user_dict['othername']
        self.email = clean_user_dict['email']
        self.phonenumber = clean_user_dict['phonenumber']
        self.passporturlstring = clean_user_dict['passporturlstring']
        self.isadmin = False
