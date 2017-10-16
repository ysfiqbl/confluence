"""
This client will/can/should be changed to a CLI eventually
This client class is used to consume confluence.py there by leaving confluence.py
to handle API calls only.

This class may later be converted to a CLI
"""
import sys, json
from confluence import Confluence

class ConfluenceClient(object):

	def __init__(self, url, username, password):
		self.confluence = Confluence(url, username, password)

	"""
	Get a array of all page titles (including children) in a space.	
	"""
	def get_page_names(self, space_key):
		has_next = True	
		page_names = []
		start = 0
		limit = 25
		while has_next is True:
			pages = self.confluence.get_pages(space_key, start, limit).json()
			results = pages['results']
			for page in results:
				page_names.append(page['title'])
			if 'next' in pages['_links']:
				start = pages['start'] + pages['limit']
			else:
				has_next = False
		return page_names
	
	
	"""
	Create an empty page in the give Confluence space
	"""
	def create_empty_page(self, space_key, title, parent_page_id=None):
		if parent_page_id is not None:
			ancestors = [{ 'id': parent_page_id }]
		else:
			ancestors = None		

		return self.confluence.create_page(space_key, title, ancestors, '')


	"""
	Write content to file
	"""
	def write_to_file(filepath, content):
		outfile = open(filepath, 'w')
		outfile.write(content)
		outfile.close()
	
"""
Change this main program to use the API.
"""
if __name__ == '__main__':
	with open(sys.argv[1], 'r') as config:
		conf = json.load(config)	 
		url = conf['url']
		username = conf['username']
		password = conf['password']
		client = ConfluenceClient(url, username, password)
		print(client.confluence.delete_space('SPACEKEY').json())
	
