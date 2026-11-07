import requests


class PumpsClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_status(self, pump_id):
        url = f"{self.base_url}/api/v1/pumps/{pump_id}/status"
        return requests.get(url, timeout=10)

    def get_alerts(self, pump_id):
        url = f"{self.base_url}/api/v1/pumps/{pump_id}/alerts"
        return requests.get(url, timeout=10)

    def delete_alert(self, pump_id, alert):
        url = f"{self.base_url}/api/v1/pumps/{pump_id}/alerts"
        return requests.delete(url, json=alert, timeout=10)

    def delete_all_alerts(self, pump_id):
        url = f"{self.base_url}/api/v1/pumps/{pump_id}/alerts/all"
        return requests.delete(url, timeout=10)

    def send_telemetry(self, pump_id, payload):
        url = f"{self.base_url}/api/v1/pumps/{pump_id}/telemetry"
        return requests.post(url, json=payload, timeout=10)
    def reset_block(self, pump_id):
        url = f"{self.base_url}/api/v1/pumps/{pump_id}/block/reset"
        return requests.post(url, timeout=10)
    def post_all_alerts(self, pump_id):
        url = f"{self.base_url}/api/v1/pumps/{pump_id}/alerts/all"
        return requests.post(url, timeout=10)