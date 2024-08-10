import os
import requests
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger()

def auth_test():
    api_address = '52.16.214.150'
    api_port = 8000
    users = [
        {'username': 'alice', 'password': 'wonderland', 'expected_status': 200},
        {'username': 'bob', 'password': 'builder', 'expected_status': 200},
        {'username': 'clementine', 'password': 'mandarine', 'expected_status': 403}
    ]
    
    # Create a session object for reusing connections
    session = requests.Session()
    
    for user in users:
        try:
            r = session.get(
                url=f'http://{api_address}:{api_port}/permissions',
                params={'username': user['username'], 'password': user['password']}
            )
            status_code = r.status_code
            test_status = 'SUCCESS' if status_code == user['expected_status'] else 'FAILURE'
            output = f"""
            ============================
                Authentication test
            ============================
            request done at "/permissions"
            | username="{user['username']}"
            | password="{user['password']}"
            expected result = {user['expected_status']}
            actual result = {status_code}
            ==> {test_status}
            """
            # Log to console
            logger.info(output)
            # Log to file if LOG environment variable is set
            if os.environ.get('LOG') == '1':
                with open('api_test.log', 'a') as file:
                    file.write(output + '\n')
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")

if __name__ == "__main__":
    auth_test()
