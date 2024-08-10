import os
import requests

def content_test():
    api_address = '52.212.242.207'
    api_port = 8000
    sentences = [
        {'sentence': 'life is beautiful', 'expected_v1': 1, 'expected_v2': 1},
        {'sentence': 'that sucks', 'expected_v1': -1, 'expected_v2': -1}
    ]
    user = {'username': 'alice', 'password': 'wonderland'}

    log_output = []
    for sentence in sentences:
        for version in ['v1', 'v2']:
            r = requests.get(
                url=f'http://{api_address}:{api_port}/{version}/sentiment',
                json={'username': user['username'], 'password': user['password'], 'sentence': sentence['sentence']}
            )
            response = r.json()
            print('jsen response', response)
            expected = sentence[f'expected_{version}']
            test_status = 'SUCCESS' if response['score'] == expected else 'FAILURE'
            output = f"""
            ============================
                Content test
            ============================
            request done at "/{version}/sentiment"
            | sentence="{sentence['sentence']}"
            expected result = {expected}
            actual result = {response['score']}
            ==> {test_status}
            """
            log_output.append(output)
            print(output)
            if os.environ.get('LOG') == '1':
                with open('api_test.log', 'a') as file:
                    file.write(output)

if __name__ == "__main__":
    content_test()
