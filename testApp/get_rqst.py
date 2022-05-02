from pprint import pprint
import requests
payload = {'key': 'Example event2011-07-30'}
r = requests.get('https://ejkqbpgyxj.execute-api.us-east-1.amazonaws.com/dev/get_item_from_dynamo', params=payload)
pprint(r.text)
#print(r.url)