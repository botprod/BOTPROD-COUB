import json
import os
import random
from colorama import Fore, Style
from datetime import datetime
from fake_useragent import UserAgent

ua = UserAgent()


class SessionManager:
    def __init__(self, session_file_path, proxy_file_path):
        self.session_file_path = session_file_path
        self.proxy_file_path = proxy_file_path
        self.sessions = self.load_sessions()
        self.proxies = self.load_proxies()

    def load_sessions(self):
        if not os.path.exists(self.session_file_path):
            return {}
        try:
            with open(self.session_file_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            self.log("ERROR", "System", f"Failed to load sessions: {str(e)}")
            return {}

    def save_sessions(self):
        try:
            with open(self.session_file_path, 'w') as f:
                json.dump(self.sessions, f, indent=4)
        except Exception as e:
            self.log("ERROR", "System", f"Failed to save sessions: {str(e)}")

    def load_proxies(self):
        try:
            with open(self.proxy_file_path, 'r') as f:
                return [line.strip() for line in f.readlines() if line.strip()]
        except FileNotFoundError:
            self.log("WARNING", "System", "Proxy file not found.")
            return []
        except Exception as e:
            self.log("ERROR", "System", f"Failed to load proxies: {str(e)}")
            return []

    def compare_and_update_sessions(self, queries):
        for username, query in queries.items():
            if username not in self.sessions:
                self.sessions[username] = {
                    "Name": username,
                    "URL": query,
                    "Proxy": self.assign_proxy(),
                    "Headers": self.generate_headers(username)
                }
        self.save_sessions()

    def get_session(self, username):
        return self.sessions.get(username)

    def generate_headers(self, name):
        android_version = random.randint(24, 33)
        webview_version = random.randint(70, 125)

        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://coub.com",
            'Referer': 'https://coub.com/',
            "User-Agent": self.get_mobile_user_agent(),
            "Sec-Ch-Ua": (
                f'"Android WebView";v="{webview_version}", '
                f'"Chromium";v="{webview_version}", '
                f'"Not?A_Brand";v="{android_version}"'
            ),
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
        }

        if not self.sessions.get(name):
            self.sessions[name] = {"proxy": "", "headers": headers}
        else:
            self.sessions[name]["headers"] = headers

        self.save_sessions()
        return headers

    def get_mobile_user_agent(self):
        user_agent = ua.random
        if 'wv' not in user_agent:
            parts = user_agent.split(')')
            parts[0] += '; wv'
            user_agent = ')'.join(parts)
        return user_agent

    def assign_proxy(self):
        if not self.proxies:
            return {"http": "", "https": ""}
        proxy = random.choice(self.proxies)
        return {"http": proxy, "https": proxy}

    async def verify_proxy(self, session, proxy):
        if not proxy or proxy == "":
            return False
        try:
            async with session.get('https://api.ipify.org?format=json', proxy=proxy, timeout=10) as response:
                if response.status == 200:
                    ip = (await response.json()).get('ip')
                    self.log("INFO", "System", f"Proxy is working. Public IP: {ip}")
                    return True
                else:
                    self.log("ERROR", "System", f"Failed to verify proxy. Status code: {response.status}")
                    return False
        except Exception as e:
            self.log("ERROR", "System", f"Proxy verification error: {str(e)}")
            return False

    def log(self, status, username, message):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status_colors = {
            "INFO": Fore.GREEN,
            "WARNING": Fore.YELLOW,
            "ERROR": Fore.RED
        }
        color = status_colors.get(status, Fore.WHITE)
        print(f"{color}{now} | {status} | {username} | {message}{Style.RESET_ALL}")
