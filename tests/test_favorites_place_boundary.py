import pytest
import allure

@allure.epic("Сценарии использования граничных значений при создании избранного места")
class TestFavoritesPlaceBoundary:
	@allure.description("Создание места с граничными значениями параметра title")
	@pytest.mark.parametrize("title, expected_status, expected_error", [
		("", 400, "пустым"),
		("1", 200, ""),
		("2", 200, ""),
		("q" * 998, 200, ""),
		("q"*999, 200, ""),
		("q" * 1000, 400, "999 символов"),
	], ids=["empty", "count symbols: 1", "count symbols: 2", "count symbols: 998", "count symbols: 999", "count symbols: 1000"])
	def test_boundary_values_for_the_title(self, post, auth_token, valid_place_data, title, expected_status, expected_error):
		data = valid_place_data.copy()
		data["title"] = title

		response = post("/v1/favorites", data=data, token=auth_token)

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
	def test_boundary_values_for_the_lat(self, post, auth_token, valid_place_data, lat, expected_status,
										   expected_error):
		data = valid_place_data.copy()
		data["lat"] = lat

		response = post("/v1/favorites", data=data, token=auth_token)

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
	def test_boundary_values_for_the_lat(self, post, auth_token, valid_place_data, lon, expected_status,
										 expected_error):
		data = valid_place_data.copy()
		data["lon"] = lon

		response = post("/v1/favorites", data=data, token=auth_token)

		assert response.status_code == expected_status
		if response.status_code == 400:
			error_message = response.json()["error"]["message"]
			assert "lon" in error_message and expected_error in error_message