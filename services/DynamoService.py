import os
import boto3
from pydantic import BaseModel
from typing import List, Optional

class DynamoService():
    """
    Class for reading and writing from a dynamo table
    """
    
    def __init__(self, table_name: str, model: BaseModel):
        self.table_name = table_name
        self.region = os.getenv('AWS_REGION')
        dynamodb = boto3.resource('dynamodb', region_name = self.region)
        self.table = dynamodb.Table(self.table_name)
        self.model = model

    def get(self, item: dict) -> Optional[BaseModel]:
        """
        Reads item from dynamo db table with item as dict: {primary_key: value_to_search}

        From Boto3 Documentation: The GetItem operation returns a set of attributes for 
        the item with the given primary key. If there is no matching item, GetItem does 
        not return any data and there will be no Item element in the response.

        Returns item in BaseModel form, or empty dict if item not found
        """
        try:
            print(f"Reading from {self.table_name}...")
            response = self.table.get_item(
                Key=item
            )
            if response.get('Item'):

                print(f'Retrieved data from {self.table_name}')
                return self.model(**response['Item'])
            else:
                print(f'No match found for key(s): {item}')
                return None
            
        except Exception as e:
            raise Exception(f"Failed to read from {self.table_name}. Exception: {e}")
        

    def put(self, item: BaseModel) -> dict:
        """
        Inserts item into dynamo db table
        """

        assert isinstance(item, self.model), (
            f'Can only insert objects of type: {type(self.model)}'
        )

        try:
            return self.table.put_item(Item=item.dict())
        except Exception as e:
            raise Exception(f'Error writing item: {item} to table: {e}')

    def batch_put(self, items: List[BaseModel]) -> dict:
        """
        """

        initial_count = len(items)
        final_count = 0
        assert isinstance(items[0], self.model), (
            f'Can only insert objects of type: {type(self.model)}'
        )

        try:
            print(f"Writing {initial_count} itmes to {self.table_name}...")
            with self.table.batch_writer() as batch:
                for item in items:
                    batch.put_item(
                        Item=item.dict()
                    )
                    final_count +=1
        except Exception as e:
            raise Exception(f'Error writing items: {items} to table: {e}')

        if initial_count != final_count:
            return {'status': f'Failed to write {initial_count-final_count} items'}
        else:
            return {'status': 'Successful batch write'}
