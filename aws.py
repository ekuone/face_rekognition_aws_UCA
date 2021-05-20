import boto3
from pic_requests import get_image
from typing import List

class Aws:
       
    def face_rekognition(self, collection_name: str, victim: str) -> List[dict]:
        client = boto3.client('rekognition')
        rekresp = client.search_faces_by_image(CollectionId = collection_name, Image={'Bytes': get_image(victim)})
        return rekresp['FaceMatches']