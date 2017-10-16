"""
This class is used to consume the Confluence API. It has only been tested with Confluence 6.0.3
"""
import requests, json

class Confluence(object):
	def __init__(self, url, username, password):
		self.url = url
		self.api_url = url + '/rest/api'
		self.username = username
		self.password = password

	"""
	Print JSON response to stdout
	"""
	def printResponse(r):
        	print '{} {}\n'.format(json.dumps(r.json(), sort_keys=True, indent=4, separators=(',', ': ')), r)


	"""
	GET /rest/api//space/<space_key>
	"""
	def get_space(self, space_key):
		space_get_url = '{0}/space/{1}'.format(self.api_url, space_key)
		return requests.get(space_get_url, auth=(self.username, self.password))
	
	"""
	POST /rest/api/space
	"""
	def create_space(self, space_key, space_name):
		data = {
			'key': space_key,
			'name': space_name
		}
		create_space_url = '{0}/space'.format(self.api_url)
		return requests.post(create_space_url, data=json.dumps(data), auth=(self.username, self.password), headers=({'Content-Type': 'application/json'}))
	
	"""
	DELETE /rest/api/space/<space_key>
	"""
	def delete_space(self, space_key):
		space_delete_url = '{0}/space/{1}'.format(self.api_url, space_key)
		return requests.delete(space_delete_url, auth=(self.username, self.password))
	
	"""
	POST /rest/api/content
	ancestors e.g [{'id': parentPageId}]
	"""
	def create_page(self, space_key, title, ancestors, content):
		create_page_url = '{0}/content'.format(self.api_url)
		data = {
                '	type': 'page',
                	'title': title,
                	'space': {'key': space_key},
                	'body': {
                        	'storage': {
                                	'value': content,
                                	'representation': 'storage'
                        	}
                	}
        	}
		
		if ancestors != None:
			data['ancestors'] = ancestors
		return requests.post(create_page_url, data=json.dumps(data), auth=(self.username, self.password), headers=({'Content-Type': 'application/json'}))
	
	
	
	"""
	GET /rest/api/content?spaceKey=<space_key>&start=<start>&limit=<limit>
	"""	
	def get_pages(self, space_key, start=0, limit=25):
		pages_get_url = '{0}/content?spaceKey={1}&start={2}&limit={3}'.format(self.api_url, space_key, start, limit)
		return requests.get(pages_get_url, auth=(self.username, self.password))
