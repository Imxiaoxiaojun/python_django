# -*- coding: utf-8 -*-
class News():
	def __init__(self,title,url): 
		self.title = title
		self.url = url
		self.picurl = ''
		self.description = ''

	@property
	def description(self):
		return self.description

	@property
	def picurl(self):
		return self.picurl
	
	@property
	def title(self):
		return self.title
		
	@property
	def url(self):
		return self.url

	@description.setter	
	def description(self,description):
		self.description = description

	@picurl.setter
	def picurl(self,picurl):
		self.picurl = picurl
	
	def class_to_dict(obj):
		is_list = obj.__class__ == [].__class__
		is_set = obj.__class__ == set().__class__
		if is_list or is_set:
			obj_arr = []
			for o in obj:
				dict = {}
				dict.update(o.__dict__)
				obj_arr.append(dict)
			return obj_arr
		else:
			dict = {}
			dict.update(obj.__dict__)
			return dict

