import os

CACHE_TTL = 3600  # 1 hour
API_PORT = int(os.getenv('FASTAPI_PORT', '8000'))
REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
ODA_API_BASE_URL = os.getenv('ODA_API_BASE_URL', 'https://oda.com/api/v1')