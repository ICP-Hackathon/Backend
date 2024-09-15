import requests

def send_data(data: str):
  publisher = "https://publisher-devnet.walrus.space"
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
  }
  url = '{0}/v1/store'.format(publisher)
  response = requests.put(url, headers=headers, data=data)
  print(response.json())
  return response.json()


def read_blob(blob_id: str):
  aggregator = "https://aggregator-devnet.walrus.space"
  response = requests.get('{0}/v1/{1}'.format(aggregator, blob_id))
  print(response.text)
  return response.text

