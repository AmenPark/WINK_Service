from rest_framework.test import APIClient, APITestCase , APIRequestFactory
from account.models import User
class TestRoutinePOST(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/Routine/"
        self.data = {
            "title": "problem solving",
            "category": "HOMEWORK",
            "goal": "Increase your problem-solving skills",
            "is_alarm": True,
            "days": ["MON", "WED", "FRI"]
        }
        self.data_alarm_bad = {
            "title": "problem solving",
            "category": "HOMEWORK",
            "goal": "Increase your problem-solving skills",
            "is_alarm": 0,
            "days": ["MON", "WED", "FRI"]
        }
        self.data_category_bad = {
            "title": "problem solving",
            "category": "HW",
            "goal": "Increase your problem-solving skills",
            "is_alarm": False,
            "days": ["MON", "WED", "FRI"]
        }
        self.data_days_bad = {
            "title": "problem solving",
            "category": "HOMEWORK",
            "goal": "Increase your problem-solving skills",
            "is_alarm": False,
            "days": ["M","T"]
        }
    def test_post_without_login(self):
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.data['message']['msg'], 'Need to login')
    def test_post_with_login(self):
        user = User.objects.create(email="test@email.com", password="Strong!Long!PW123")
        self.client.force_authenticate(user=user)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.data["message"]["status"], "ROUTINE_CREATE_OK")
    def test_post_with_login_and_bad_request(self):
        user = User.objects.create(email="test@email.com", password="Strong!Long!PW123")
        self.client.force_authenticate(user=user)
        response = self.client.post(self.url, self.data_alarm_bad)
        self.assertEqual(response.data["message"]["status"], "INVALID_IS_ALARM")
        response = self.client.post(self.url, self.data_category_bad)
        self.assertEqual(response.data["message"]["status"], "INVALID_CATEGORY")
        response = self.client.post(self.url, self.data_days_bad)
        self.assertEqual(response.data["message"]["status"], "BAD_DAYOFTHEWEEK")

class TestRoutineOneData(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/Routine/"
        self.data = {
            "title": "problem solving",
            "category": "HOMEWORK",
            "goal": "Increase your problem-solving skills",
            "is_alarm": True,
            "days": ["MON", "WED", "FRI"]
        }
        self.user = User.objects.create(email="test@email.com", password="Strong!Long!PW123")
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, self.data)
        self.find_id = response.data["data"]["routine_id"]
    def test_post_and_get(self):
        getresponse = self.client.get(self.url+f'{self.find_id}/')
        self.assertEqual(getresponse.data["message"]["status"],"ROUTINE_DETAIL_OK")
    def test_get_without_login(self):
        self.client.force_authenticate(user=None)
        getresponse = self.client.get(self.url + f'{self.find_id}/')
        self.assertEqual(getresponse.data["message"]["status"], "ROUTINE_DETAIL_OK")
    def test_get_cannot_find(self):
        getresponse = self.client.get(self.url + f'{self.find_id+1}/')
        self.assertEqual(getresponse.data["message"]["status"], "ROUTINE_NOT_EXIST")
    def test_delete_cannot_find(self):
        response = self.client.delete(self.url + f'{self.find_id + 1}/')
        self.assertEqual(response.data["message"]["status"], "ROUTINE_NOT_EXIST")
    def test_delete_without_auth(self):
        self.client.force_authenticate(user=None)
        response = self.client.delete(self.url + f'{self.find_id}/')
        self.assertEqual(response.data["message"]["status"], "NOT_ALLOWED")
    def test_delete_well(self):
        response = self.client.delete(self.url + f'{self.find_id}/')
        self.assertEqual(response.data["message"]["status"], "ROUTINE_DELETE_OK")
    def test_delete_twice(self):
        self.client.delete(self.url + f'{self.find_id}/')
        response = self.client.delete(self.url + f'{self.find_id}/')
        self.assertEqual(response.data["message"]["status"], "ROUTINE_NOT_EXIST")
    def test_get_after_delete(self):
        self.client.delete(self.url + f'{self.find_id}/')
        getresponse = self.client.get(self.url + f'{self.find_id}/')
        self.assertEqual(getresponse.data["message"]["status"], "ROUTINE_NOT_EXIST")

class testRoutineDatas(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/Routine/"
        self.datas = [
            {
                "title": "problem solving",
                "category": "HOMEWORK",
                "goal": "Increase your problem-solving skills",
                "is_alarm": True,
                "days": ["MON", "WED", "FRI"]
            },
            {
                "title": "ENG Listening",
                "category": "HOMEWORK",
                "goal": "Learn survive when you go abroad",
                "is_alarm": False,
                "days": ["TUE", "WED", "SAT", "SUN"]
            },
            {
                "title": "Reading Books",
                "category": "HOMEWORK",
                "goal": "Read well-known books",
                "is_alarm": True,
                "days": ["MON", "THU"]
            }
        ]
        self.user = User.objects.create(email="test@email.com", password="Strong!Long!PW123")
        self.client.force_authenticate(user=self.user)
        [self.client.post(self.url, d) for d in self.datas]
        self.user2 = User.objects.create(email="test2@created.com", password="Maye@strong2be")
        self.client.force_authenticate(user=self.user2)
        for data in self.datas:
            data["title"] += "VII"
        [self.client.post(self.url, d) for d in self.datas]
        self.putdata = {
                         "routine_id" : 1,
                         "title" : "New Title",
                         "days" : ["MON","TUE","WED","THU"],
                        }
    def test_get_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(r"/Routine/getlist/", {"today": "2022-02-14"})
        self.assertEqual(len(response.data["data"]), 2)
        response = self.client.post(r"/Routine/getlist/", {"today": "2022-02-15"})
        self.assertEqual(len(response.data["data"]), 1)
        response = self.client.post(r"/Routine/getlist/", {"today": "2022-02-20"})
        self.assertEqual(len(response.data["data"]), 1)
    def test_get_list_without_login(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(r"/Routine/getlist/", {"today": "2022-02-14"})
        self.assertEqual(response.data["message"]["status"], "NEED_LOGIN")
    def test_put_without_auth(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.put(r"/Routine/", self.putdata)
        self.assertEqual(response.data["message"]["status"], "NOT_ALLOWED")
    def test_put(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(r"/Routine/", self.putdata)
        self.assertEqual(response.data["message"]["status"], "ROUTINE_UPDATE_OK")
        getresponse = self.client.get(r'/Routine/1/')
        self.assertEqual(getresponse.data["data"]["title"], "New Title")

class testRoutine

