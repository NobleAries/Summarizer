class Crawler(object):
	def __init__(self, url):
		self.url = url
		
	def get_content(self):
		f = open(self.url, "r")
		content = f.read()
		f.close()
		return content
