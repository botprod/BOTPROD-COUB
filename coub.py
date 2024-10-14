import random
import time

from colorama import Fore, Style
from datetime import datetime
import asyncio


def log(status, username, message):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status_colors = {
        "INFO": Fore.GREEN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED
    }
    color = status_colors.get(status, Fore.WHITE)
    print(f"{color}{now} | {status} | {username} | {message}{Style.RESET_ALL}")


class Coub:
    def __init__(self, session_name):
        self.base_url = 'https://coub.com/api/v2'
        self.session_name = session_name  # Сохраняем имя сессии

    async def login(self, session, query, headers, proxy=None, login_url=None):
        delay = random.uniform(0, 600)
        if login_url:
            async with session.get(login_url, headers=headers, proxy=proxy) as response:
                time.sleep(5)
                pass
        log("INFO", self.session_name, f"Waiting for {delay:.2f} seconds before login to simulate user behavior")
        await asyncio.sleep(delay)
        try:
            async with session.get(f"https://coub.com/tg-app/?tgWebAppStartParam={query['start_param']}",
                                   headers=headers, proxy=proxy) as response:
                if response.status == 200:
                    log("INFO", self.session_name, "Login successful")
                    try:
                        async with session.post(f"{self.base_url}/sessions/login_mini_app", headers=headers, data=query,
                                                proxy=proxy) as response:
                            if response.status == 200:
                                log("INFO", self.session_name, "Getting Token")
                                api_token = (await response.json()).get('api_token', "")
                                return await self.get_token(session, api_token, headers, proxy)
                            else:
                                url = f"https://coub.com/api/v2/sessions/signup_mini_app"
                                async with session.post(url, headers=headers, data=query, proxy=proxy) as response:
                                    print(query)
                                    if response.status == 200:
                                        log("INFO", self.session_name, "Getting Token")
                                        api_token = (await response.json()).get('api_token', "")
                                        return await self.get_token(session, api_token, headers, proxy)
                                    else:
                                        log("ERROR", self.session_name,
                                            f"Failed to authenticate user. Status code: {response.status}")
                                        return None
                    except Exception as e:
                        log("ERROR", self.session_name, f"Login error: {str(e)}")
                        return None
                else:
                    log("ERROR", self.session_name, f"Failed to authenticate user. Status code: {response.status}")
                    return False
        except Exception as e:
            log("ERROR", self.session_name, f"Login error: {str(e)}")
            return False

    async def get_token(self, session, api_token, headers, proxy=None):
        # Random delay between requests to simulate user behavior
        delay = random.uniform(5, 20)
        log("INFO", "System", f"Waiting for {delay:.2f} seconds before getting token to simulate user behavior")
        await asyncio.sleep(delay)

        headers['x-auth-token'] = api_token
        url = f"{self.base_url}/torus/token"
        try:
            async with session.post(url, headers=headers, proxy=proxy) as response:
                if response.status == 200:
                    data = await response.json()
                    access_token = data.get('access_token', '')
                    expires_in = data.get('expires_in', '')
                    log("INFO", "System", f"Token Created, Expired in {round(expires_in / 3600)} Hours")
                    return access_token
                else:
                    log("ERROR", "System", f"Failed to get token. Status code: {response.status}")
                    return None
        except Exception as e:
            log("ERROR", "System", f"Token retrieval error: {str(e)}")
            return None

    async def get_rewards(self, session, token, headers, proxy=None):
        # Random delay between requests to simulate user behavior
        delay = random.uniform(5, 20)
        log("INFO", "System", f"Waiting for {delay:.2f} seconds before getting rewards to simulate user behavior")
        await asyncio.sleep(delay)

        headers['authorization'] = f"Bearer {token}"
        url = f"https://rewards.coub.com/api/v2/get_user_rewards"
        try:
            async with session.get(url, headers=headers, proxy=proxy) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    log("ERROR", "System", f"Failed to retrieve user rewards. Status code: {response.status}")
                    return None
        except Exception as e:
            log("ERROR", "System", f"Get rewards error: {str(e)}")
            return None

    async def claim_task(self, session, token, task_id, task_title, headers, proxy=None):
        # Random delay between requests to simulate user behavior
        delay = random.uniform(5, 20)
        log("INFO", "System", f"Waiting for {delay:.2f} seconds before claiming task to simulate user behavior")
        await asyncio.sleep(delay)

        headers['authorization'] = f"Bearer {token}"
        params = {"task_reward_id": task_id}
        url = f"https://rewards.coub.com/api/v2/complete_task"
        try:
            async with session.get(url, headers=headers, params=params, proxy=proxy) as response:
                if response.status == 200:
                    log("INFO", "System", f"ID {task_id} | Task '{task_title}' Done")
                    return await response.json()
                else:
                    log("ERROR", "System",
                        f"ID {task_id} | Task '{task_title}' Failed to claim | error : {response.status}")
                    return None
        except Exception as e:
            log("ERROR", "System", f"Claim task error: {str(e)}")
            return None
