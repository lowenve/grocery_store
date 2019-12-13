import requests
import time


url = 'http://mzjs.cnki.net/exam/extraction'
for i in range(400000):
    r = requests.get(url)
    print(i)
    time.sleep(0.2)
