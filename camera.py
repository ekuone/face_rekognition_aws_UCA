from time import strftime as st, gmtime as gt
import cv2, os

from attendance import Attendance
from stalker import * 
class Camera:
	def __init__(self):
		self.names_list = []
		self.time_list = []
	
	def take_pic(self, collection_name: str):
		capture = cv2.VideoCapture(0)
		face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
		image_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'devils_eye') 
		while True:
			ret, image = capture.read()
			gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors = 5)
			for (x, y, w, h) in faces:	
				roi_gray = gray [y: y+h, x: x+w]
				roi_color = image [y: y+h, x: x+w]
				cv2.imwrite(os.path.join(image_dir, 'target.jpeg'), roi_color)
				cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
				name = Stalker().run_stalker(collection_name, 'target.jpeg')
				print(name)
				if name in self.names_list:
					pass
				else:
					self.names_list.append(name)
					self.time_list.append(st('%H:%M:%S', gt()))
			cv2.imshow('look_at_me', image)
			if cv2.waitKey(20) & 0xFF == ord('q'):
				break
		cv2.destroyAllWindows()
		Attendance(self.names_list, self.time_list).take_attendance()
	

