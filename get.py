import requests

x = requests.get("http://localhost:8080/api/produto")
print(x.status_code)
data = x.json()

print(data)
PARAMS = ({"id":10},{"produto":"cadeira"},{"qtd":1},{"preco":120},{"idMP":1},{"loja":"loja"})
x = requests.get(url ="http://localhost:8080/api/cadastro", params= PARAMS)

data = x.json()
print(data)