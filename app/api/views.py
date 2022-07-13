import logging, os, json, redis
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from worker.tasks import get_quote_exe

logger = logging.getLogger(__name__)
redis_client = redis.Redis(host=os.environ.get("REDIS_HOST", "redis"),
            port=int(os.environ.get("REDIS_PORT", "6379")),
            decode_responses=True)

@api_view(['GET'])
def get_quote(request):
    key = os.environ.get('API_KEY')
    #authenticate basic
    if request.META['HTTP_AUTHORIZATION'] == None or key != request.META['HTTP_AUTHORIZATION']:
        return Response('', status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        data = request.data
        if 'ticker' in data:
            get_quote_exe.delay(data['ticker'])

        return Response(data, status=status.HTTP_200_OK)

    return Response('', status=status.HTTP_403_FORBIDDEN)
