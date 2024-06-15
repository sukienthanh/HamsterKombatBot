import asyncio
import json
from venv import logger
import aiohttp
from typing import Any

from bot.api.http import handle_error, make_post_request
from bot.utils.scripts import escape_html, get_fingerprint


async def login(self, http_client: aiohttp.ClientSession, json_file_path: str) -> str:
        response_text = ''
        try:
             # Read JSON data from file
            with open("json/"+json_file_path+".json", 'r', encoding="utf8") as file:
                json_data = json.load(file)

            response = await http_client.post(url='https://api.hamsterkombat.io/auth/auth-by-telegram-webapp',
                                             #json={"initDataRaw": json_data, "fingerprint": FINGERPRINT})
                                             json= json_data)
            
            response_text = await response.text()
            response.raise_for_status()

            response_json = await response.json()
            access_token = response_json['authToken']

            return access_token
        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error while getting Access Token: {error} | "
                         f"Response text: {escape_html(response_text)[:128]}...")
            await asyncio.sleep(delay=3)