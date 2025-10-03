import pytest
import requests

BASE_URL = "https://regions-test.2gis.com"

@pytest.fixture
def base_url():
    return BASE_URL

@pytest.fixture
def post(base_url):
    def _post(path, data=None, token=None):
        cookies = {"token": token} if token else None
        return requests.post(f"{base_url}{path}", data=data, cookies=cookies)
    return _post

@pytest.fixture
def auth_token(base_url):
    """Фикстура для получения свежего токена перед каждым тестом"""
    response = requests.post(f"{base_url}/v1/auth/tokens")
    token = response.cookies.get('token')
    assert token is not None, "Не удалось получить токен"
    return token

@pytest.fixture
def valid_place_data():
    """Валидные данные для создания места"""
    return {
        "title": "Тестовое место",
        "lat": 55.7558,
        "lon": 37.6173,
        "color": "BLUE"
    }