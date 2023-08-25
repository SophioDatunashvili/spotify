
from celery import shared_task
from .client import SpotifyClient
import requests
import redis

@shared_task
def fetch_and_store_new_releases():
    client = SpotifyClient()

    api_url = 'https://api.spotify.com/v1/browse/new-releases?limit=50'
    header = {'Authorization': f'Bearer {client.access_token}'}

    response = requests.get(api_url, headers=header)
    data = response.json()

    new_releases = {}
    items = data.get("albums", {}).get("items", [])
    for item in items:
        if item["album_type"] == "single":
            single_name = item["name"]
            artist = item["artists"][0]["name"]
            new_releases[single_name] = artist

    # Connect to the Redis server
    redis_host = 'redis'
    redis_port = 6379
    redis_db = 0
    redis_connection = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

    # Serialize the data as JSON and store it in Redis
    import json
    serialized_data = json.dumps(new_releases)
    redis_connection.set('new_releases', serialized_data, ex=3600 * 24)  # Cache for 24 hours


