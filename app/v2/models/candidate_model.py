"""App/v2/models/party_model.py"""
from app.v2.models import BaseModel


class CandidateModel(BaseModel):
    """The Party Model"""
    table_name = "candidates"
    sub_set_cols = ['id', 'office_id',
                    'party_id', 'user_id']

    def __init__(self):
        """Init Model"""
        super(CandidateModel, self).__init__()

    def create(self, office_id, party_id, user_id,):
        """Create a new candidate

         Arguments:
             office_id {[int]} -- [office id]
             party_id {[int]} -- [party id]
             user_id {[int]} -- [user Id (Ther candidate)]
         """
        self.office_id = office_id
        self.party_id = party_id
        self.user_id = user_id
