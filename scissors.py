from PIL import Image
import cv2, os

class Scissors:
	def __init__(self):
		self.face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
		self.image_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wanted')

	def run_scissors(self):
		for root, dirs, files in os.walk(self.image_dir):
			for file in files:
				if file.endswith("jpeg") or file.endswith("JPG"):
					path_to_target = os.path.join(root, file)
					self.cut_faces(path_to_target)
					self.cut_picture(path_to_target)
	# def run_scissors(self):
	# 	for root, dirs, files in os.walk(self.image_dir):
	# 		for file in files:
	# 			if file == "name.jpeg":
	# 				path_to_target = os.path.join(root, file)
	# 				self.cut_faces(path_to_target)
	# 				self.cut_picture(path_to_target)				
					
	def cut_faces(self, target_picture: str):
		img = cv2.imread(target_picture)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		face = self.face_cascade.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors = 5)
		for (x, y, w, h) in face:	
			roi_gray = gray [y: y+h, x: x+w]
			roi_color = img [y: y+h, x: x+w]
			cv2.imwrite(target_picture, roi_gray)
	
	def cut_picture(self, target_picture: str):
		img = cv2.imread(target_picture)
		width = int((img.shape)[0]/2.5) 
		height = int((img.shape)[1]/2.5)
		resized_img = cv2.resize(img,(height, width))
		cv2.imwrite(target_picture, resized_img)

Scissors().run_scissors()