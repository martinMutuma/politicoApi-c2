from tests.v2 import BaseTest
from app.v2.models.user_model import UserModel
from app.v2.models.party_model import PartyModel
from app.v2.models.candidate_model import CandidateModel
from app.v2.models.office_model import OfficeModel
from app.v2.models.vote_model import VoteModel
from app.v2.models.petition_model import PetitionModel


class TestModels(BaseTest):

    def test_user_model(self):
        user_data = self.generate_user()
        user = UserModel()
        user.create_user(user_data)
        self.assertEqual(user.email, user_data['email'])
        user.insert(user_data)
        self.assertEqual(type(user.id), int)

    def test_office_model(self):
        office_data = self.generate_random_office()
        office = OfficeModel()
        office.create_office(office_data['name'], office_data['type'])
        self.assertEqual(office.name, office_data['name'])
        office.insert(office_data)
        self.assertEqual(type(office.id), int)

    def test_party_model(self):
        party_data = self.gen_party()
        party = PartyModel()
        party.create(party_data['name'],
                     party_data['hqAddress'], party_data['logoUrl'])
        self.assertEqual(party.name, party_data['name'])
        party.insert(party_data)
        self.assertEqual(type(party.id), int)

    def test_candidate_model(self):
        candidate = CandidateModel()
        candidate.create(1, 1, 1)
        self.assertEqual(candidate.office_id, 1)
        self.assertIsInstance(candidate, CandidateModel)

    def test_vote_model(self):
        vote = VoteModel()
        vote.create(1, 3, 4)
        self.assertEqual(vote.office_id, 1)
        self.assertIsInstance(vote, VoteModel)

    def test_petition(self):
        petition = PetitionModel()
        petition.create(1, 1, "Body", 'Evidence')
        self.assertEqual(petition.office_id, 1)
        self.assertIsInstance(petition, PetitionModel)
