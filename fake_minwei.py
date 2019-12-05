import requests

url = 'http://mzjs.cnki.net/exam/extraction'
fout = open('result.txt', 'w')
for i in range(100000):
    r=requests.get(url)
    fout.write(str(i+1)+' ： OK with status_code: '+str(r.text)+'\n')
    print(str(i+1)+' ： OK with status_code: '+str(r.text)+'\n')
fout.close()