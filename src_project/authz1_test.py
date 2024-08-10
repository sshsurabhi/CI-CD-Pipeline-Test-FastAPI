import os
import requests
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger()

def authz_test():
    api_address = '52.212.242.207'
    api_port = 8000
    test_cases = [
        {'username': 'bob', 'password': 'builder', 'endpoint': 'v1', 'expected_status': 200},
        {'username': 'bob', 'password': 'builder', 'endpoint': 'v2', 'expected_status': 403},
        {'username': 'alice', 'password': 'wonderland', 'endpoint': 'v1', 'expected_status': 200},
        {'username': 'alice', 'password': 'wonderland', 'endpoint': 'v2', 'expected_status': 200},
    ]

    log_output = []
    for case in test_cases:
        r = requests.get(
            url=f'http://{api_address}:{api_port}/{case["endpoint"]}/sentiment',
            json={'username': case['username'], 'password': case['password'], 'sentence': 'test'}
        )
        status_code = r.status_code
        test_status = 'SUCCESS' if status_code == case['expected_status'] else 'FAILURE'
        output = f"""
        ============================
            Authorization test
        ============================
        request done at "/{case['endpoint']}/sentiment"
        | username="{case['username']}"
        | password="{case['password']}"
        expected result = {case['expected_status']}
        actual result = {status_code}
        ==> {test_status}
        """
        log_output.append(output)
        print(output)
        if os.environ.get('LOG') == '1':
            with open('api_test.log', 'a') as file:
                file.write(output)

if __name__ == "__main__":
    authz_test()
