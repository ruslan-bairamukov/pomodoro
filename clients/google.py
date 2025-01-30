import requests

from config import Settings
from schemas import GoogleUserData


class GoogleClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def get_user_info(self, code: str) -> GoogleUserData:
        google_access_token = self._get_user_access_token(
            code=code
        )
        user_info = requests.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={
                "Authorization": f"Bearer {google_access_token}"
            },
        )
        return GoogleUserData(
            **user_info.json(),
            google_access_token=google_access_token,
        )

    def _get_user_access_token(self, code: str) -> str:
        data = {
            "code": code,
            "client_id": self.settings.GOOGLE_OIDC.GOOGLE_CLIENT_ID,
            "client_secret": self.settings.GOOGLE_OIDC.GOOGLE_CLIENT_SECRET,
            "redirect_uri": self.settings.GOOGLE_OIDC.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        response = requests.post(
            url=self.settings.GOOGLE_OIDC.GOOGLE_TOKEN_URL,
            data=data,
        )
        return response.json()["access_token"]
