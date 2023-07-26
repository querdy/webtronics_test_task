from redis.asyncio import Redis

from app.settings import settings

redis = Redis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0")
