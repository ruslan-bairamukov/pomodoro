import httpx

from app.config import Settings
from app.users.auth.schemas import YandexUserData


class YandexClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.async_client = httpx.AsyncClient

    async def get_user_info(
        self, code: str
    ) -> YandexUserData:
        yandex_access_token = (
            await self._get_user_access_token(code=code)
        )
        async with self.async_client() as client:
            user_info = await client.get(
                "https://login.yandex.ru/info?format=json",
                headers={
                    "Authorization": f"OAuth {yandex_access_token}"
                },
            )
        return YandexUserData(
            **user_info.json(),
            yandex_access_token=yandex_access_token,
        )

    async def _get_user_access_token(
        self, code: str
    ) -> str:
        async with self.async_client() as client:
            response = await client.post(
                self.settings.YANDEX_OIDC.YANDEX_TOKEN_URL,
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "client_id": self.settings.YANDEX_OIDC.YANDEX_CLIENT_ID,
                    "client_secret": self.settings.YANDEX_OIDC.YANDEX_CLIENT_SECRET,
                },
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            )
        return response.json()["access_token"]
