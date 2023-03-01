import requests
import re

def retrieve_credentials(domain, timeout=5):
    payload={}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }

    response = None
    try:
        response = requests.request("GET", domain, headers=headers, data=payload, timeout=timeout)
    except:
        return { "ScanSuccessful": False }

    if response.status_code >= 400:
        return { "ScanSuccessful": False }
    
    def merge_cookies(request_headers, response_cookies):
        cookies = {}
        if 'Cookie' in request_headers:
            for cookie in request_headers['Cookie'].split('; '):
                cookies[cookie.split('=')[0]] = '='.join(cookie.split('=')[1:])
        
        for cookie in response_cookies:
            cookies[cookie] = response_cookies[cookie]

        return cookies if len(cookies) > 0 else None
    
    pattern = r"var g_ck = '(.*)';"
    try:
        return {
            "ScanSuccessful": True,
            "Credentials": {
                'Token': re.search(pattern, response.text).group(1) if re.search(pattern, response.text) != None else None,
                'Cookies': merge_cookies(response.request.headers, response.cookies.get_dict())
            }
        }
    except Exception as e:
        print(domain, e)
        return {
            "ScanSuccessful": False
        }
    

