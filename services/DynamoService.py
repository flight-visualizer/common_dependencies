import os
import boto3
from pydantic import BaseModel
from typing import List

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

    def get(self, item: dict) -> dict:
        """
        Reads item from dynamo db table with item as dict: {primary_key: value_to_search}
        """
        try:
            print(f"Reading from {self.table_name}...")
            response = self.table.get_item(
                Key=item.dict()
            )
            return response['Item']
        except:
            raise Exception(f"Failed to read from {self.table_name}")
        

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
