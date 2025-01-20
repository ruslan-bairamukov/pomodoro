import redis

from config import settings


class CacheHelper:
    def __init__(
        self,
        host: str,
        port: int,
        db: int,
        username: str,
        password: str,
    ) -> None:
        self.host = host
        self.port = port
        self.db = db
        self.username = username
        self.password = password

    def get_redis(self) -> redis.Redis:
        return redis.Redis(
            host=self.host,
            port=self.port,
            db=self.db,
            username=self.username,
            password=self.password,
        )

    def set_pomo(self) -> int:
        redis = self.get_redis()
        redis.set(
            name="task:pomodoro_count",
            value=1,
            ex=300,
        )
        return redis.get("task:pomodoro_count")

    def test_connection(self) -> None:
        try:
            r = self.get_redis()
            # r = redis.Redis(host='192.168.1.84', port=36379)
            # r = redis.Redis(host='localhost', port=16379, db=0, username='redis', password='superSECRETpassword')
            # r = redis.Redis.from_url("redis://127.0.0.1:36379/0")
            # url="redis://default:@0.0.0.0:16379/0"
            info = r.info()
            print(info["redis_version"])
            response = r.ping()
            if response:
                print("Подключение успешно!")
            else:
                print("Не удалось подключиться к Redis.")
        except redis.exceptions.RedisError as e:
            print(f"Ошибка: {e}")


cache_helper = CacheHelper(
    host=settings.REDIS.HOST,
    port=settings.REDIS.PORT,
    db=settings.REDIS.DB,
    username=settings.REDIS.USERNAME,
    password=settings.REDIS.PASSWORD,
)
