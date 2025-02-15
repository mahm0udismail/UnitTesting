import json

class APIClient:

    def __init__(self, test_client):
        self.client = test_client

    def post(self, endpoint, data):
        return self.client.post(endpoint, data=json.dumps(data), content_type="application/json")

    def put(self, endpoint, data):
        return self.client.put(endpoint, data=json.dumps(data), content_type="application/json")

    def delete(self, endpoint):
        return self.client.delete(endpoint)

    def get(self, endpoint):
        return self.client.get(endpoint)
