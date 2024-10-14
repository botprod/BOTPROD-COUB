import asyncio
from utils.file_loader import load_json_file
from utils.parser import parse_query
from utils.session_manager import SessionManager
from coub import Coub
import aiohttp
from datetime import datetime
from colorama import Fore, Style


def log(status, username, message):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status_colors = {
        "INFO": Fore.GREEN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED
    }
    color = status_colors.get(status, Fore.WHITE)
    print(f"{color}{now} | {status} | {username} | {message}{Style.RESET_ALL}")


# main.py
async def main():
    session_manager = SessionManager('data/sessions.json', 'data/proxy.txt')
    queries = load_json_file('data/coub_query.json')
    tasks = load_json_file('data/task.json', default=[])
    total_queries = len(queries)

    log("INFO", "System", f"Starting task for {total_queries} accounts.")

    # Check for new queries and add to sessions if missing
    session_manager.compare_and_update_sessions(queries)

    async with aiohttp.ClientSession() as session:
        tasks_to_run = [
            process_account(session, session_manager, username, query, tasks, total_queries, index)
            for index, (username, query) in enumerate(queries.items(), start=1)
        ]
        await asyncio.gather(*tasks_to_run)


async def process_account(session, session_manager, username, query, tasks, total_queries, index):
    session_data= session_manager.get_session(username)
    if not session_data:
        log("WARNING", username, "No session found. Skipping...")
        return

    headers = session_data['Headers']
    proxy = session_data['Proxy'].get('http')
    # Ping to verify proxy is working
    if not await session_manager.verify_proxy(session, proxy):
        log("WARNING", username, "Proxy is not working. Skipping session.")
        return

    parsed_data, x_tg_auth, query = parse_query(query)
    headers['x-tg-authorization'] = x_tg_auth
    log("INFO", username, f"Processing account {index}/{total_queries}")

    coub = Coub(username)  # Передаем имя сессии в Coub
    token = await coub.login(session, parsed_data, headers, proxy, query)
    if not token:
        log("ERROR", username, "Failed to authenticate user.")
        return

    data_reward = await coub.get_rewards(session, token, headers, proxy)
    if not data_reward:
        await coub.claim_task(session, token, 1, "Welcome Task", headers, proxy)
        data_reward = await coub.get_rewards(session, token, headers, proxy)
        if not data_reward:
            log("ERROR", username, "Failed to retrieve rewards.")
            return

    list_id = [data.get('id', 0) for data in data_reward if data.get('id', 0) not in [2, 12, 13, 15, 16, 19]]

    for task in tasks:
        task_id = task.get('id')
        if task_id in list_id:
            log("INFO", username, f"Task '{task.get('title')}' already completed.")
        else:
            await asyncio.sleep(2)
            log("INFO", username, f"Starting task '{task.get('title')}'.")
            await coub.claim_task(session, token, task.get('id'), task.get('title'), headers, proxy)


if __name__ == "__main__":
    asyncio.run(main())
