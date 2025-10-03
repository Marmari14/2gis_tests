import time
import pytest
import requests
import allure

@allure.epic("Создание избранного места")
class TestFavoritesPlace:

	@allure.description("Отправка запроса без токена")
	def test_missing_token(self, base_url, valid_place_data):
		response = requests.post(
			f"{base_url}/v1/favorites",
			data=valid_place_data
		)

		assert response.status_code == 401
		error_message = response.json()["error"]["message"]
		assert "token" in error_message and "обязательным" in error_message

	@allure.description("Отправка запроса с некорректным токеном")
	def test_invalid_token(self, base_url, valid_place_data):
		response = requests.post(
			f"{base_url}/v1/favorites",
			data=valid_place_data,
			cookies={"token": 'token'}
		)

		assert response.status_code == 401
		error_message = response.json()["error"]["message"]
		assert "token" in error_message and "несуществующий" in error_message

	@allure.description("Отправка запроса с 'протухшим' токеном")
	def test_expired_token(self, base_url, auth_token, valid_place_data):
		token = auth_token

		time.sleep(3)

		response = requests.post(
			f"{base_url}/v1/favorites",
			data=valid_place_data,
			cookies={"token": token}
		)

		assert response.status_code == 401
		error_message = response.json()["error"]["message"]
		assert "token" in error_message and "протухший" in error_message

	@allure.description("Успешное создание избранного места с обязательными параметрами")
	def test_create_place_with_required_fields(self, base_url, auth_token, valid_place_data):
		data = {
			"title": valid_place_data["title"],
			"lat": valid_place_data["lat"],
			"lon": valid_place_data["lon"]
		}

		response = requests.post(
			f"{base_url}/v1/favorites",
			data=data,
			cookies={"token": auth_token}
		)

		assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
		response_data = response.json()

		assert "id" in response_data
		assert response_data["title"] == data["title"]
		assert response_data["lat"] == data["lat"]
		assert response_data["lon"] == data["lon"]
		assert response_data["color"] is None
		assert "created_at" in response_data

	@allure.description("Создание места с разными значениями color")
	@pytest.mark.parametrize("color", ["BLUE", "GREEN", "RED", "YELLOW"])
	def test_create_place_with_different_colors(self, base_url, auth_token, valid_place_data, color):
		data = valid_place_data.copy()
		data["color"] = color

		response = requests.post(
			f"{base_url}/v1/favorites",
			data=data,
			cookies={"token": auth_token}
		)

		assert response.status_code == 200
		assert response.json()["color"] == color

	@allure.description("Создание места с некорректным значением color")
	def test_create_place_with_invalid_color(self, base_url, auth_token, valid_place_data):
		data = valid_place_data.copy()
		data["color"] = "color"

		response = requests.post(
			f"{base_url}/v1/favorites",
			data=data,
			cookies={"token": auth_token}
		)

		assert response.status_code == 400
		error_message = response.json()["error"]["message"]
		assert "color" in error_message and "BLUE, GREEN, RED, YELLOW" in error_message

	@allure.description("Создание места с допустимыми значениями title")
	@pytest.mark.parametrize("title", ["кириллица", "lat", "1542", ".?!,:;"],
							 ids=["cyrillic alphabet", "latin alphabet", "numbers", "punctuation marks"])
	def test_different_characters_in_title(self, base_url, auth_token, valid_place_data, title):
		data = valid_place_data.copy()
		data["title"] = title

		response = requests.post(
			f"{base_url}/v1/favorites",
			data=data,
			cookies={"token": auth_token}
		)

		assert response.status_code == 200
		assert response.json()["title"] == title

	@allure.description("Создание места с некорректным значениям lat")
	def test_create_place_with_invalid_lat(self, base_url, auth_token, valid_place_data):
		data = valid_place_data.copy()
		data["lat"] = "lat"

		response = requests.post(
			f"{base_url}/v1/favorites",
			data=data,
			cookies={"token": auth_token}
		)

		assert response.status_code == 400
		error_message = response.json()["error"]["message"]
		assert "lat" in error_message and "'lat' должен быть числом" in error_message

	@allure.description("Создание места с некорректным значениям lon")
	def test_create_place_with_invalid_lon(self, base_url, auth_token, valid_place_data):
		data = valid_place_data.copy()
		data["lon"] = "lon"

		response = requests.post(
			f"{base_url}/v1/favorites",
			data=data,
			cookies={"token": auth_token}
		)

		assert response.status_code == 400
		error_message = response.json()["error"]["message"]
		assert "lon" in error_message and "'lon' должен быть числом" in error_message

	@allure.description("Создание места с некорректным значениям title")
	@pytest.mark.parametrize("title", ["@", "$", "%%%"])
	def test_special_characters_in_title(self, base_url, auth_token, valid_place_data, title):
		data = valid_place_data.copy()
		data["title"] = title

		response = requests.post(
			f"{base_url}/v1/favorites",
			data=data,
			cookies={"token": auth_token}
		)

		assert response.status_code == 400

	@allure.description("Создание места без параметра title")
	def test_missing_title_parameter(self, base_url, auth_token, valid_place_data):
		data = {
			"lat": valid_place_data["lat"],
			"lon": valid_place_data["lon"]
		}

		response = requests.post(
			f"{base_url}/v1/favorites",
			data=data,
			cookies={"token": auth_token}
		)

		assert response.status_code == 400
		error_message = response.json()["error"]["message"]
		assert "title" in error_message and "обзательным" in error_message

		# TODO: После исправления бага заменить на:
		# assert "title" in error_message and "обязательным" in error_message

	@allure.description("Создание места без параметра lat")
	def test_missing_lat_parameter(self, base_url, auth_token, valid_place_data):
		data = {
			"title": valid_place_data["title"],
			"lon": valid_place_data["lon"]
		}

		response = requests.post(
			f"{base_url}/v1/favorites",
			data=data,
			cookies={"token": auth_token}
		)

		assert response.status_code == 400
		error_message = response.json()["error"]["message"]
		assert "lat" in error_message and "обязательным" in error_message

	@allure.description("Создание места без параметра lon")
	def test_missing_lon_parameter(self, base_url, auth_token, valid_place_data):
		data = {
			"title": valid_place_data["title"],
			"lat": valid_place_data["lat"]
		}

		response = requests.post(
			f"{base_url}/v1/favorites",
			data=data,
			cookies={"token": auth_token}
		)

		assert response.status_code == 400
		error_message = response.json()["error"]["message"]
		assert "lon" in error_message and "обязательным" in error_message

	@allure.description("Создание места с граничными значениями параметра title")
	@pytest.mark.parametrize("title, expected_status, expected_error", [
		("", 400, "пустым"),
		("1", 200, ""),
		("2", 200, ""),
		("q" * 998, 200, ""),
		("q"*999, 200, ""),
		("q" * 1000, 400, "999 символов"),
	], ids=["empty", "count symbols: 1", "count symbols: 2", "count symbols: 998", "count symbols: 999", "count symbols: 1000"])
	def test_boundary_values_for_the_title(self, base_url, auth_token, valid_place_data, title, expected_status, expected_error):
		data = valid_place_data.copy()
		data["title"] = title

		response = requests.post(
			f"{base_url}/v1/favorites",
			data=data,
			cookies={"token": auth_token}
		)

		assert response.status_code == expected_status
		if response.status_code == 400:
			error_message = response.json()["error"]["message"]
			assert "title" in error_message and expected_error in error_message

	@allure.description("Создание места с граничными значениями параметра lat")
	@pytest.mark.parametrize("lat, expected_status, expected_error", [
		("", 400, "'lat' должен быть числом"),
		("-91", 400, "не менее -90"),
		("-90", 200, ""),
		("-89", 200, ""),
		("89", 200, ""),
		("90", 200, ""),
		("91", 400, "не более 90"),
	], ids=["empty", "lat: -91", "lat: -90", "lat: -89", "lat: 89", "lat: 90", "lat: 91"])
	def test_boundary_values_for_the_lat(self, base_url, auth_token, valid_place_data, lat, expected_status,
										   expected_error):
		data = valid_place_data.copy()
		data["lat"] = lat

		response = requests.post(
			f"{base_url}/v1/favorites",
			data=data,
			cookies={"token": auth_token}
		)

		assert response.status_code == expected_status
		if response.status_code == 400:
			error_message = response.json()["error"]["message"]
			assert "lat" in error_message and expected_error in error_message

	@allure.description("Создание места с граничными значениями параметра lon")
	@pytest.mark.parametrize("lon, expected_status, expected_error", [
		("", 400, "'lon' должен быть числом"),
		("-181", 400, "не менее -180"),
		("-180", 200, ""),
		("-179", 200, ""),
		("179", 200, ""),
		("180", 200, ""),
		("181", 400, "не более 180"),
	], ids=["empty", "lon: -181", "lon: -180", "lon: -179", "lon: 179", "lon: 180", "lon: 181"])
	def test_boundary_values_for_the_lat(self, base_url, auth_token, valid_place_data, lon, expected_status,
										 expected_error):
		data = valid_place_data.copy()
		data["lon"] = lon

		response = requests.post(
			f"{base_url}/v1/favorites",
			data=data,
			cookies={"token": auth_token}
		)

		assert response.status_code == expected_status
		if response.status_code == 400:
			error_message = response.json()["error"]["message"]
			assert "lon" in error_message and expected_error in error_message