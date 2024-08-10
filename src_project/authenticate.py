import os
import requests

def auth_test():
    api_address = '52.212.242.207'
    api_port = 8000
    users = [
        {'username': 'alice', 'password': 'wonderland', 'expected_status': 200},
        {'username': 'bob', 'password': 'builder', 'expected_status': 200},
        {'username': 'clementine', 'password': 'mandarine', 'expected_status': 403}
    ]

    log_output = []
    for user in users:
        r = requests.get(
            url=f'http://{api_address}:{api_port}/permissions',
            params={'username': user['username'], 'password': user['password']}
        )
        status_code = r.status_code
        test_status = 'SUCCESS' if status_code == user['expected_status'] else 'FAILURE'
        output = f"""
	  Results  After Run
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
        log_output.append(output)
#        print(output)
        if os.environ.get('LOG') == '1':
            with open('api_test.log', 'a') as file:
                file.write(output)

if __name__ == "__main__":
    auth_test()
