import requests


def consume_API():
    #TODO cambiar el URL
    url = 'http://api.example.com/books' 
    r = requests.get(url)
    results = r.json()
    plates_list = {'plates':results['results']}
    return plates_list