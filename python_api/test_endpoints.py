import requests


def test_alerts():
    try:
        r = requests.get('http://localhost:3000/alerts', timeout=10)
        print('ALERTS', r.status_code)
        print(r.text[:2000])
    except Exception as e:
        print('ALERTS ERROR', e)


def test_predict():
    try:
        with open('../README.md', 'rb') as f:
            files = {'image': ('README.md', f, 'text/plain')}
            r = requests.post('http://127.0.0.1:5000/predict', files=files, timeout=20)
            print('PREDICT', r.status_code)
            print(r.text)
    except Exception as e:
        print('PREDICT ERROR', e)


if __name__ == '__main__':
    test_alerts()
    test_predict()
