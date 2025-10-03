import time
import pytest
import allure

@allure.epic("Негативные сценарии создания избранного места")
class TestFavoritesPlaceNegative:

	@allure.description("Отправка запроса без токена")
	def test_missing_token(self, post, base_url, valid_place_data):
		response = post("/v1/favorites", data=valid_place_data)

		assert response.status_code == 401
		error_message = response.json()["error"]["message"]
		assert "token" in error_message and "обязательным" in error_message

	@allure.description("Отправка запроса с некорректным токеном")
	def test_invalid_token(self, post, base_url, valid_place_data):
		response = post("/v1/favorites", data=valid_place_data, token="token")

		assert response.status_code == 401
		error_message = response.json()["error"]["message"]
		assert "token" in error_message and "несуществующий" in error_message

	@allure.description("Отправка запроса с 'протухшим' токеном")
	def test_expired_token(self, post, base_url, auth_token, valid_place_data):
		token = auth_token

		time.sleep(3)

		response = post("/v1/favorites", data=valid_place_data, token=token)

		assert response.status_code == 401
		error_message = response.json()["error"]["message"]
		assert "token" in error_message and "протухший" in error_message

	@allure.description("Создание места с некорректным значением color")
	def test_create_place_with_invalid_color(self, post, auth_token, valid_place_data):
		data = valid_place_data.copy()
		data["color"] = "color"

		response = post("/v1/favorites", data=data, token=auth_token)

		assert response.status_code == 400
		error_message = response.json()["error"]["message"]
		assert "color" in error_message and "BLUE, GREEN, RED, YELLOW" in error_message

	@allure.description("Создание места с некорректным значениям lat")
	def test_create_place_with_invalid_lat(self, post, auth_token, valid_place_data):
		data = valid_place_data.copy()
		data["lat"] = "lat"

		response = post("/v1/favorites", data=data, token=auth_token)

		assert response.status_code == 400
		error_message = response.json()["error"]["message"]
		assert "lat" in error_message and "'lat' должен быть числом" in error_message

	@allure.description("Создание места с некорректным значениям lon")
	def test_create_place_with_invalid_lon(self, post, auth_token, valid_place_data):
		data = valid_place_data.copy()
		data["lon"] = "lon"

		response = post("/v1/favorites", data=data, token=auth_token)

		assert response.status_code == 400
		error_message = response.json()["error"]["message"]
		assert "lon" in error_message and "'lon' должен быть числом" in error_message

	@allure.description("Создание места с некорректным значениям title")
	@pytest.mark.parametrize("title", ["@", "$", "%%%"])
	def test_special_characters_in_title(self, post, auth_token, valid_place_data, title):
		data = valid_place_data.copy()
		data["title"] = title

		response = post("/v1/favorites", data=data, token=auth_token)

		assert response.status_code == 400

	@allure.description("Создание места без параметра title")
	@pytest.mark.xfail(reason="опечатка 'обзательным' вместо 'обязательным'")
	def test_missing_title_parameter(self, post, auth_token, valid_place_data):
		data = {
			"lat": valid_place_data["lat"],
			"lon": valid_place_data["lon"]
		}

		response = post("/v1/favorites", data=data, token=auth_token)

		assert response.status_code == 400
		error_message = response.json()["error"]["message"]
		assert "title" in error_message and "обязательным" in error_message

	@allure.description("Создание места без параметра lat")
	def test_missing_lat_parameter(self, post, auth_token, valid_place_data):
		data = {
			"title": valid_place_data["title"],
			"lon": valid_place_data["lon"]
		}

		response = post("/v1/favorites", data=data, token=auth_token)

		assert response.status_code == 400
		error_message = response.json()["error"]["message"]
		assert "lat" in error_message and "обязательным" in error_message

	@allure.description("Создание места без параметра lon")
	def test_missing_lon_parameter(self, post, auth_token, valid_place_data):
		data = {
			"title": valid_place_data["title"],
			"lat": valid_place_data["lat"]
		}

		response = post("/v1/favorites", data=data, token=auth_token)

		assert response.status_code == 400
		error_message = response.json()["error"]["message"]
		assert "lon" in error_message and "обязательным" in error_message

