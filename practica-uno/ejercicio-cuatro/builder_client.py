import requests

url = "http://localhost:8000/pacientes"
headers = {'Content-type': 'application/json'}

# GET /pizzas
response = requests.get(url)
print(response.json())

# POST /pizzas 
mi_paciente= {
    "nombre": "David",
    "apellido": "Mamani",
    "edad": 20,
    "genero": "Masculino",
    "diagnostico": "diabetes",
    "doctor": "Pedro Perez",
}
response = requests.post(url, json=mi_paciente, headers=headers)
print(response.json())

# GET /pizzas
response = requests.get(url)
print(response.json())

# DELETE /pizzas/1
response = requests.delete(url + "/1")
print(response.json())

# GET /pizzas
response = requests.get(url)
print(response.json())
