import os
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger()

def authz_test():
    api_address = '52.16.214.150'
    api_port = 8000
    test_cases = [
        {'username': 'bob', 'password': 'builder', 'endpoint': 'v1', 'expected_status': 200},
        {'username': 'bob', 'password': 'builder', 'endpoint': 'v2', 'expected_status': 403},
        {'username': 'alice', 'password': 'wonderland', 'endpoint': 'v1', 'expected_status': 200},
        {'username': 'alice', 'password': 'wonderland', 'endpoint': 'v2', 'expected_status': 200},
    ]

    for case in test_cases:
        try:
            response = requests.get(
                url=f'http://{api_address}:{api_port}/{case["endpoint"]}/sentiment',
                params={'username': case['username'], 'password': case['password'], 'sentence': 'test'}
            )
            status_code = response.status_code
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
            logger.info(output)
            if os.environ.get('LOG') == '1':
                with open('api_test.log', 'a') as file:
                    file.write(output + '\n')

        except requests.RequestException as e:
            error_output = f"Request failed: {e}"
            logger.error(error_output)
            if os.environ.get('LOG') == '1':
                with open('api_test.log', 'a') as file:
                    file.write(error_output + '\n')

if __name__ == "__main__":
    authz_test()
