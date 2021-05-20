from pandas import DataFrame

class Attendance:
	def __init__(self, names_list: list, time_list: list):
		self.names_list = names_list
		self.time_list = time_list

	def take_attendance(self):
		sdnt_tm = DataFrame({'Name': self.names_list, 'time': self.time_list})
		sdnt_tm.to_excel('./Attendance.xlsx', index = None)