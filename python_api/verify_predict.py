import requests
import os

# Test prediction endpoint with class_names.json as a dummy file
try:
    test_file_path = 'class_names.json'
    with open(test_file_path, 'rb') as f:
        files = {'image': (test_file_path, f, 'application/json')}
        r = requests.post('http://127.0.0.1:5000/predict', files=files, timeout=20)
        print('STATUS:', r.status_code)
        print('RESPONSE:', r.json() if r.headers.get('content-type') == 'application/json' else r.text)
except Exception as e:
    print('ERROR:', e)
