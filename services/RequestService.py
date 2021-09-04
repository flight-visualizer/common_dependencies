import requests
from pydantic import BaseModel

class RequestService():
    """
    Class for reading and writing from a dynamo table
    """
    
    def __init__(self, endpoint: str, params: dict, responseModel: BaseModel):
        self.endpoint = endpoint
        self.params = params
        self.responseModel = responseModel

    def query(self) -> BaseModel:

        try:
            print(f'Attempting to query data...')
            response = requests.get(
                self.endpoint, 
                params=self.params
            )
            print(f'Response received... status: {response.status_code}')

            return self.responseModel(**response.json())

        except:
            print('Error querying aviation stack...')
            raise