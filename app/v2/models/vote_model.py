"""App/v2/models/party_model.py"""
from app.v2.models import BaseModel


class VoteModel(BaseModel):
    """The Party Model"""
    table_name = "votes"
    sub_set_cols = ['id', 'office_id',
                    'candidate_id', 'createdby', 'createdOn']

    def __init__(self):
        """Init Model"""
        super(VoteModel, self).__init__()

    def create(self, office_id, candidate_id, createdby,):
        """[summary]

         Arguments:
             office_id {[int]} -- [office id]
             candidate_id {[int]} -- [candidate id]
             createdby {[int]} -- [user Id (Ther Voter)]
         """
        self.office_id = office_id
        self.candidate_id = candidate_id
        self.createdby = createdby
