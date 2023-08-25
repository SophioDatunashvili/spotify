from rest_framework.views import APIView
from rest_framework.response import Response
import json
import redis


class GetNewReleases(APIView):
    def get(self, request):
        redis_host = 'redis'
        redis_port = 6379
        redis_db = 0
        redis_connection = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

        cached_data = redis_connection.get('new_releases')
        if cached_data is not None:
            cached_data = json.loads(cached_data)
            return Response(cached_data)
        else:
            return Response({"message": "Data not available."}, status=404)



    
