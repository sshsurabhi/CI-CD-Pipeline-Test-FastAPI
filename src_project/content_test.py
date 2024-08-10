import os
import requests

def content_test():
    api_address = '52.16.214.150'
    api_port = 8000
    sentences = [
        {'sentence': 'life is beautiful', 'expected_v1': 'positive', 'expected_v2': 'positive'},
        {'sentence': 'that sucks', 'expected_v1': 'negative', 'expected_v2': 'negative'}
    ]
    user = {'username': 'alice', 'password': 'wonderland'}

    log_output = []
    for sentence in sentences:
        for version in ['v1', 'v2']:
            r = requests.get(
                url=f'http://{api_address}:{api_port}/{version}/sentiment',
                params={'username': user['username'], 'password': user['password'], 'sentence': sentence['sentence']}
            )
            
            # Debugging output to print the response content
            print(f"Response status code: {r.status_code}")
            print(f"Response content: {r.text}")
            
            if r.status_code == 200:
                response = r.json()
                score = response['score']
                expected = sentence[f'expected_{version}']
                
                # Check if the score matches the expected sign
                if (expected == 'positive' and score > 0) or (expected == 'negative' and score < 0):
                    test_status = 'SUCCESS'
                else:
                    test_status = 'FAILURE'
                
                output = f"""
                ============================
                    Content test
                ============================
                request done at "/{version}/sentiment"
                | sentence="{sentence['sentence']}"
                expected result = {expected} score
                actual result = {score}
                ==> {test_status}
                """
            else:
                # If the request fails, log the error details
                output = f"""
                ============================
                    Content test - ERROR
                ============================
                request done at "/{version}/sentiment"
                | sentence="{sentence['sentence']}"
                Status Code: {r.status_code}
                Response: {r.text}
                ==> FAILURE
                """
            
            log_output.append(output)
            print(output)
            if os.environ.get('LOG') == '1':
                with open('api_test.log', 'a') as file:
                    file.write(output)

if __name__ == "__main__":
    content_test()
