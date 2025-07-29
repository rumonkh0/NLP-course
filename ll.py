import requests
import time
from datetime import datetime

url = "http://app5.nu.edu.bd/nu-web/pinRetrievalForm"

headers = {
    "Accept": "text/plain, */*; q=0.01",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Referer": "http://app5.nu.edu.bd/nu-web/pinRetrievalForm",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

data = {
    "hscRoll": "5282881",
    "hscPassingYear": "2024",
    "hscBoardId": "12",  # Rajshahi board as number
    "birthDate": "18-12-2005",
    "degreeName": "Honours"
}

start_time = datetime.now()
attempt = 0

while True:
    attempt += 1
    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)

        elapsed = datetime.now() - start_time
        print(f"[{attempt}] Status: {response.status_code}, Time Elapsed: {elapsed}")

        if response.status_code == 200 and response.text.strip():
            print("\n✅ Success!")
            print("🕓 Total Time Elapsed:", elapsed)
            print("📄 Response:\n", response.text.strip())
            break

    except requests.RequestException as e:
        print(f"[{attempt}] ❌ Request failed: {e}")

    time.sleep(2)  # Delay between retries
import requests
import time
from datetime import datetime

url = "http://app55.nu.edu.bd/nu-web/applicantLogin.action?degreeName=Honours"

headers = {
    "Accept": "text/plain, */*; q=0.01",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Referer": "http://app5.nu.edu.bd/nu-web/pinRetrievalForm",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}

data = {
    "hscRoll": "5282881",
    "hscPassingYear": "2024",
    "hscBoardId": "12",  # Rajshahi board as number
    "birthDate": "18-12-2005",
    "degreeName": "Honours"
}

start_time = datetime.now()
attempt = 0

while True:
    attempt += 1
    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)

        elapsed = datetime.now() - start_time
        print(f"[{attempt}] Status: {response.status_code}, Time Elapsed: {elapsed}")

        if response.status_code == 200 and response.text.strip():
            print("\n✅ Success!")
            print("🕓 Total Time Elapsed:", elapsed)
            print("📄 Response:\n", response.text.strip())
            break

    except requests.RequestException as e:
        print(f"[{attempt}] ❌ Request failed: {e}")

    time.sleep(2)  # Delay between retries
