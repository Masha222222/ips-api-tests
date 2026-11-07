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