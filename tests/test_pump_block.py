from datetime import datetime, timezone
import allure
from api_tests.models.pumps import (
    PumpStateResponse,
    ResetBlockResponse,
    TelemetryRequest,
)


@allure.title("Сброс отклонён, если причина блокировки сохраняется")
def test_reset_block_rejects_low_glucose(pumps_client, test_pump_id, pump_alerts):
    before = pumps_client.get_status(test_pump_id)
    assert before.status_code == 200, f"Не удалось получить статус: {before.text}"

    state_before = PumpStateResponse.model_validate(before.json(), strict=True)
    assert state_before.bolus_status == "blocked", (
        f"Перед сбросом ожидалась блокировка: {before.text}"
    )

    response = pumps_client.reset_block(test_pump_id)
    assert response.status_code == 403, (
        f"При отказе в сбросе ожидался HTTP-код 403, "
        f"получен {response.status_code}. Ответ: {response.text}"
    )

    result = ResetBlockResponse.model_validate(response.json(), strict=True)
    assert result.status == "FAILED", (
        f"Ожидался отказ в сбросе, получено {result.status!r}: {result.message}"
    )

    after = pumps_client.get_status(test_pump_id)
    assert after.status_code == 200, f"Не удалось получить статус: {after.text}"

    state_after = PumpStateResponse.model_validate(after.json(), strict=True)
    assert state_after.bolus_status == "blocked", (
        f"После отказа блокировка должна сохраниться: {after.text}"
    )


@allure.title("Успешный сброс снимает требование ручного действия")
def test_reset_block_clears_manual_action(pumps_client, test_pump_id, pump_alerts):
    telemetry = TelemetryRequest(
        glucose_value=6.0,
        glucose_unit="mmol/L",
        timestamp=datetime.now(timezone.utc),
    )
    sent = pumps_client.send_telemetry(
        test_pump_id, telemetry.model_dump(mode="json")
    )
    assert sent.status_code == 200, f"Не удалось отправить измерение: {sent.text}"

    before = pumps_client.get_status(test_pump_id)
    assert before.status_code == 200, f"Не удалось получить статус: {before.text}"

    state_before = PumpStateResponse.model_validate(before.json(), strict=True)
    assert state_before.glucose_level == "normal", (
        f"Перед сбросом ожидался уровень normal: {before.text}"
    )
    assert state_before.manual_action_required is True, (
        f"До сброса ожидалось требование ручного действия: {before.text}"
    )

    response = pumps_client.reset_block(test_pump_id)
    assert response.status_code == 200, (
        f"Ожидался HTTP-код 200, получен {response.status_code}. "
        f"Ответ: {response.text}"
    )

    result = ResetBlockResponse.model_validate(response.json(), strict=True)
    assert result.status == "OK", (
        f"Ожидался успешный сброс, получено {result.status!r}: {result.message}"
    )

    after = pumps_client.get_status(test_pump_id)
    assert after.status_code == 200, f"Не удалось получить статус: {after.text}"

    state_after = PumpStateResponse.model_validate(after.json(), strict=True)
    assert state_after.manual_action_required is False, (
        f"После сброса ручное действие не должно требоваться: {after.text}"
    )