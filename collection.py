import boto3
from pic_requests import get_image
from typing import List

class Collection:
	def __init__(self):
		self.client = boto3.client('rekognition')

	def get_all_collections(self) -> List[str]:
	    response = self.client.list_collections()
	    result = []
	    while True:
	        collections = response['CollectionIds']
	        result.extend(collections)
	        if 'NextToken' in response:
	            next_token = response['NextToken']
	            response = self.client.list_collections(NextToken = next_token)
	            print(response)
	        else:
	            break
	    return result

	def get_exists_collection(self, collection_name: str) -> bool:
	    return collection_name in self.get_all_collections()

	def create_new_collection(self, collection_name: str):
	    if not self.get_exists_collection(collection_name):
	        response = self.client.create_collection(CollectionId = collection_name)
	        if response['StatusCode'] != 200:
	            raise 'Could not create collection, ' + collection_name \
	            + ', status code: ' + str(response['StatusCode'])

	def destroy_collection(self, collection_name: str):
	    from botocore.exceptions import ClientError
	    try:
	        self.client.delete_collection(CollectionId = collection_name)
	    except ClientError as e:
	        raise e.response['Error']['Code']

	def get_faces_from_collection(self, collection_name: str) -> List[dict]:
	    response = self.client.list_faces(CollectionId = collection_name)
	    tokens = True
	    result = []
	    while tokens:
	        faces = response['Faces']
	        result.extend(faces)
	        if 'NextToken' in response:
	            next_token = response['NextToken']
	            response = self.client.list_faces(CollectionId = collection_name, NextToken = next_token)
	        else:
	            tokens = False
	    return result

	def add_new_face(self, collection_name: str, image: str):

	    def extract_file_name(fname_or_url: str) -> str:
	        import re
	        return re.split('[\\\/]', fname_or_url)[-1]
	   
	    rekresp = self.client.index_faces(CollectionId = collection_name, 
	    	Image = {'Bytes': get_image(image)}, ExternalImageId = extract_file_name(image))
	    
	    if rekresp['FaceRecords'] == []:
	        raise Exception('No face found in the image')