import requests

url = 'http://127.0.0.1:5000/api/category'
url2 = 'http://127.0.0.1:5000/api/login'

def post_category(name, url, token):
    r= requests.post(url, json={'name': '{}'.format(name)}, headers={"Authorization": "Bearer {}".format(token)});
    print(r.json())
    return r.json()

def login(url, email, password):
    r= requests.post(url, json={'email': '{}'.format(email), 'password': '{}'.format(password)});
    return {'access_token': r.json()['access_token'], 'refresh_token': r.json()['refresh_token']}

def get_category(url):
    r= requests.get(url);
    test = r.json()['data']
    print("\n".join(["id: {} -- name: {}".format(x['id'], x['name']) for x in test]))
    return r.json()

def delete_category(url, id, token):
    r= requests.delete(url, json={'id': '{}'.format(id), 'name':'r'}, headers={"Authorization": "Bearer {}".format(token)});
    return r.json()

tokens = login(url2, "tor@test.com", "test")
print("Hentet access token. \ntoken: {}".format(tokens['access_token']))
# req = post_category("Tullekategori", url, tokens['access_token'])

listeMedTing = ["Jada", "Jeadi", "Heida", "Tullball"]

for i in listeMedTing:
    req = post_category(i, url, tokens['access_token'])

get_category(url)
print(delete_category(url, 3, tokens['access_token']))
