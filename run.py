import json
import os
import time
import urllib
from multiprocessing import Process, Queue

import requests

num_process = 15
folder_to_save = './downloaded_images'


def download(q):
    while True:
        try:
            item = q.get()
            file = folder_to_save + '/' + str(item['id']) + '.png'
            if os.path.isfile(file):
                print('File is already exist')
                continue
            urllib.request.urlretrieve(item['transparent']['thumb_url'], file)
        except Exception as e:
            print('Error: ' + e)


if __name__ == '__main__':
    is_exist = os.path.exists(folder_to_save)
    if not is_exist:
        # Create a new directory because it does not exist
        os.makedirs(folder_to_save)

    queue = Queue()

    producers = []
    for i in range(num_process):
        p = Process(target=download, args=(queue,))
        p.daemon = True
        producers.append(p)

    for p in producers:
        p.start()

    """for p in producers:
        p.join()"""

    api_url = 'https://api.generated.photos/api/frontend/v1/images'

    headers = {
        'Authorization': 'API-Key Cph30qkLrdJDkjW-THCeyA',  # Token autorization
        'Content-Type': 'application/json',
        # 'date': 'Sun, 13 Feb 2022 10:43:52 GMT',
        # 'content-encoding': 'gzip',
        # 'strict-transport-security': 'max-age=15724800; includeSubDomains',
        # 'vary': 'Accept-Encoding, Origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
    }
    params = {'order_by': 'latest',
              'page': '1',
              'per_page': '50',
              'age': 'young-adult',
              'ethnicity': 'white',
              'gender': 'female',
              'emotion': 'neutral',
              # 'headpose': 'center'
              }

    page = 1
    while True:
        print('Parsing page №: ' + str(page))

        params['page'] = str(page)
        res = requests.get(api_url, headers=headers, params=params)
        data = json.loads(res.content)
        if len(data['images']) == 0:
            break
        for item in data['images']:
            queue.put(item)
        page = page + 1
        time.sleep(1)

    while queue.qsize():
        time.sleep(2)

    print('Exiting...')
