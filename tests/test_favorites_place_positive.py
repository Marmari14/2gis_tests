import pytest
import allure

@allure.epic("Позитивные сценарии создания избранного места")
class TestFavoritesPlacePositive:
	@allure.description("Успешное создание избранного места с обязательными параметрами")
	def test_create_place_with_required_fields(self, post, auth_token, valid_place_data):
		data = {
			"title": valid_place_data["title"],
			"lat": valid_place_data["lat"],
			"lon": valid_place_data["lon"]
		}

		response = post("/v1/favorites", data=data, token=auth_token)

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
	def test_create_place_with_different_colors(self, post, auth_token, valid_place_data, color):
		data = valid_place_data.copy()
		data["color"] = color

		response = post("/v1/favorites", data=data, token=auth_token)

		assert response.status_code == 200
		assert response.json()["color"] == color

	@allure.description("Создание места с допустимыми значениями title")
	@pytest.mark.parametrize("title", ["кириллица", "lat", "1542", ".?!,:;"],
							 ids=["cyrillic alphabet", "latin alphabet", "numbers", "punctuation marks"])
	def test_different_characters_in_title(self, post, auth_token, valid_place_data, title):
		data = valid_place_data.copy()
		data["title"] = title

		response = post("/v1/favorites", data=data, token=auth_token)

		assert response.status_code == 200
		assert response.json()["title"] == title
