import unittest
from fastapi.testclient import TestClient
from app.main import app

class TestUserAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
    
    # 正常情況
    def test_create_user_success(self):
        payload = {"name": "Tesla","age": 50}
        response = self.client.post("/users/", json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["name"], "Tesla")

    # 新增使用者異常情況：user name 為空
    def test_create_empty_name(self):
        payload = {"name": "", "age": 50}
        response = self.client.post("/users/", json=payload)
        self.assertEqual(response.status_code, 422)   # 判斷異常是否有回報 422
        self.assertIn("name", response.text)          # 判斷異常是否有回報 name 字串

    # 新增使用者異常情況：user age 超過 120 (這裏測試 999)
    def test_create_invalid_age(self):
        payload = {"name": "Tesla", "age": 999}
        response = self.client.post("/users/", json=payload)
        self.assertEqual(response.status_code, 422)
        self.assertIn("age", response.text)

if __name__ == "__main__":
    unittest.main()
        