"""App/v2/models/party_model.py"""
from app.v2.models import BaseModel


class PetitionModel(BaseModel):
    """The Party Model"""
    table_name = "petitions"
    sub_set_cols = ['id', 'createdBy',
                    'office_id', 'body', 'evidence']

    def __init__(self):
        """Init Model"""
        super(PetitionModel, self).__init__()

    def create(self, createdBy, office_id, body, evidence):
        """[summary]

         Arguments:
             office_id {[int]} -- [office id]
             candidate_id {[int]} -- [candidate id]
             createdby {[int]} -- [user Id (Ther Voter)]
             body =descriFption of the petation
         """
        self.office_id = office_id
        self.createdBy = createdBy
        self.body = body
