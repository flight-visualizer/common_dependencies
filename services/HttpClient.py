import requests
from pydantic import BaseModel

class HttpClient():
    """
    Class for reading and writing from a dynamo table
    """
    
    def __init__(self, endpoint: str, api_key: str, responseModel: BaseModel):
        self.endpoint = endpoint
        self.api_key = api_key
        self.responseModel = responseModel

    def query(self, payload: dict = {}) -> BaseModel:

        try:
            print(f'Attempting to query endpoint: {self.endpoint}...')
            response = requests.get(
                self.endpoint, 
                params={
                    'access_key': self.api_key,
                    **payload
                }
            )
            print(f'Response received... status: {response.status_code}')

            return self.responseModel(**response.json())

        except Exception as e:
            raise Exception(f'Error querying aviation stack: {e}')