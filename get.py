import requests

x = requests.get("http://localhost:5000/api/produto")
print(x.status_code)
data = x.json()

print(data)

x = requests.get(url ="http://localhost:5000/api/produto", params={"id":1})
data = x.json()
print(data)