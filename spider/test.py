from urllib.request import urlopen
url = 'http://www.bing.com'

responce = urlopen(url)

print(responce.closed)

print(type(responce))
print(responce.status)
print(responce._method)
print(responce.info())