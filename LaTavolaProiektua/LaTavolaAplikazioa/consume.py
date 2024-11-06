import requests


def consume_API():
    url = 'http://api.example.com/books' 
    r = requests.get(url)
    results = r.json()
    plates_list = {'plates':results['results']}
    return plates_list