from typing import Dict, List
import requests
from datetime import datetime
from app.core.config import settings

class GigaAPI:
    def __init__(self):
        self.cert = settings.GIGA_CERT_PATH
        self.authorization_token = settings.GIGA_AUTH_TOKEN
        self.access_token = {"token": "XXX", "expires": datetime(1900, 1, 1, 0, 0)}

    async def obtain_access_token(self) -> bool:
        try:
            url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
            payload = {'scope': 'GIGACHAT_API_CORP'}
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json',
                'Authorization': f'Basic {self.authorization_token}'
            }
            
            async with requests.Session() as session:
                response = await session.post(url, headers=headers, data=payload, verify=self.cert)
                if response.status_code == 200:
                    data = response.json()
                    self.access_token["token"] = data["access_token"]
                    self.access_token["expires"] = datetime.fromtimestamp(data['expires_at'])
                    return True
            return False
        except Exception as e:
            print(f"Error obtaining token: {e}")
            return False

    async def get_completion(self, messages: List[Dict]) -> Dict:
        if datetime.now() > self.access_token['expires']:
            await self.obtain_access_token()

        url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
        payload = {
            "model": "GigaChat-Pro",
            "messages": messages,
            "stream": False,
            "repetition_penalty": 1
        }
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.access_token["token"]}'
        }

        async with requests.Session() as session:
            response = await session.post(url, headers=headers, json=payload, verify=self.cert)
            return response.json()