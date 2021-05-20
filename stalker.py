from pathlib import Path 
from glob import glob
from aws import Aws
from datetime import datetime as dt
from time import strftime as st
from collection import Collection
from attendance import Attendance

class Stalker:
	
	def run_stalker(self, collection_name: str, target_name: str):
		if len(Collection().get_all_collections()) == 0 or collection_name not in Collection().get_all_collections():
			Collection().create_new_collection(collection_name)
		else:  
			if len(Collection().get_faces_from_collection(collection_name)) < 3:
			    list_faces_name = glob('wanted/*.jpeg')
			    for victim in list_faces_name:
			        Collection().add_new_face(collection_name ,victim)
			img_victim = str(Path('devils_eye') / target_name)
			faces_info = Aws().face_rekognition(collection_name, img_victim)
			student_name = ''.join([face_info['Face']['ExternalImageId'] for face_info in faces_info])
			
			return student_name[:student_name.find('.')]