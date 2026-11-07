import allure
import pytest
from pydantic import TypeAdapter

from api_tests.models.pumps import AlertResponse


@allure.title("Получение списка предупреждений помпы")
def test_get_pump_alerts(pumps_client):
    response = pumps_client.get_alerts("pump-1")

    assert response.status_code == 200, (
        f"Ожидался код 200, получен {response.status_code}. "
        f"Ответ: {response.text}"
    )

    TypeAdapter(list[AlertResponse]).validate_json(response.text, strict=True)


@allure.title("Удаление предупреждения с некорректными данными")
@pytest.mark.parametrize(
    "payload",
    [
        pytest.param(None, id="missing-body"),
        pytest.param({"level": "unknown"}, id="invalid-level"),
        pytest.param(
            {"level": "warning", "timestamp": "not-a-date"},
            id="invalid-timestamp",
        ),
    ],
)
def test_delete_alert_rejects_invalid_payload(
    pumps_client, test_pump_id, payload
):
    response = pumps_client.delete_alert(test_pump_id, payload)

    assert response.status_code == 422, (
        f"Для тела {payload!r} ожидался код 422, "
        f"получен {response.status_code}. Ответ: {response.text}"
    )

@allure.title("Удаление одного предупреждения помпы")
def test_delete_alert(pumps_client, test_pump_id, pump_alerts):
    alert = pump_alerts[0]

    response = pumps_client.delete_alert(test_pump_id, alert)

    assert response.status_code == 200, (
        f"Ожидался код 200 при удалении, получен {response.status_code}. "
        f"Ответ: {response.text}"
    )
    TypeAdapter(list[AlertResponse]).validate_json(response.text, strict=True)

    response = pumps_client.get_alerts(test_pump_id)
    assert response.status_code == 200, (
        f"Не удалось проверить список после удаления: {response.status_code}"
    )
    assert response.json() == pump_alerts[1:], (
        f"Должно исчезнуть только выбранное предупреждение. Осталось: {response.text}"
    )


@allure.title("Удаление всех предупреждений помпы")
def test_delete_all_alerts(pumps_client, test_pump_id, pump_alerts):
    response = pumps_client.delete_all_alerts(test_pump_id)

    assert response.status_code == 200, (
        f"Ожидался код 200 при удалении всех предупреждений, "
        f"получен {response.status_code}. Ответ: {response.text}"
    )
    TypeAdapter(list[AlertResponse]).validate_json(response.text, strict=True)

    response = pumps_client.get_alerts(test_pump_id)
    assert response.status_code == 200, (
        f"Не удалось проверить список после удаления: {response.status_code}"
    )
    assert response.json() == [], (
        f"После удаления всех предупреждений ожидался пустой список: {response.text}"
    )

@allure.title("Стенд отклоняет POST /alerts/all")
def test_post_all_alerts_is_not_allowed(pumps_client, test_pump_id):
    response = pumps_client.post_all_alerts(test_pump_id)

    assert response.status_code == 405, (
        f"На стенде для POST /alerts/all ожидался код 405, "
        f"получен {response.status_code}. Ответ: {response.text}"
    )