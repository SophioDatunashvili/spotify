import requests
import base64


class SpotifyClient:
	def __init__(self):
		self.client_id = "9cb859667fcd4487b2cbd3af514106bc"
		self.client_secret = "79b5d7c5a8574e7288a3ce171041793d"
		
		auth_string = f"{self.client_id}:{self.client_secret}"
		auth_header = {
			"Authorization": f"Basic {base64.b64encode(auth_string.encode()).decode()}",
			"Content-Type": "application/x-www-form-urlencoded"
		}
		# Prepare token request data
		token_url = 'https://accounts.spotify.com/api/token'
		token_params = {
			'grant_type': 'client_credentials',
		}
		
		# Request token from Spotify
		token_response = requests.post(token_url, data=token_params, headers=auth_header)
		self.token = token_response.json()
		self.access_token = self.token['access_token']