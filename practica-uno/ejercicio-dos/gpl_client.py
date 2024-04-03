import requests
# Definir la URL del servidor GraphQL
url = 'http://localhost:8000/graphql'

# Definir la consulta GraphQL simple
query_lista = """
{
        plantas{
            id
            nombre
            especie
            edad
            altura
            frutos
        }
    }
"""
# Solicitud POST al servidor GraphQL
response = requests.post(url, json={'query': query_lista})
print(response.text)


print("---------plantaPorEspecie--------------")
# Definir la consulta GraphQL con parametros po especie 
query = """
    {
        plantaPorEspecie(especie:"Tulbalghia"){
            id
            
        }
    }
"""

# Solicitud POST al servidor GraphQL
response1 = requests.post(url, json={'query': query})
print(response1.text)


print("-----plantaPorFrutos-----------")
# Definir la consulta GraphQL por  Buscar las plantas que tienen frutos
query2 = """
    {
        plantaSiTieneFrutos(frutos:True){
           nombre
        }
    }
"""

# Solicitud POST al servidor GraphQL
response2 = requests.post(url, json={'query': query2})
print(response2.text)


# Definir la consulta GraphQL para crear nuevo estudiante
query_crear = """
mutation {
        crearPlanta( nombre="Alfalfa", especie="Armeria", edad=30, altura=40,frutos=false) {
            planta {
                id
                nombre
                especie
                edad
                altura
                frutos
            }
        }
    }
"""

response_mutation = requests.post(url, json={'query': query_crear})
print(response_mutation.text)

# Lista de todos los estudiantes
response = requests.post(url, json={'query': query_lista})
print(response.text)

# Definir la consulta GraphQL para eliminar un estudiante
query_eliminar = """
mutation {
        deletePlanta(id: 2) {
            planta {
                nombre
                especie
                edad
                altura
                frutos
            }
        }
    }
"""

response_mutation = requests.post(url, json={'query': query_eliminar})
print(response_mutation.text)

# Lista de todos los estudiantes
response = requests.post(url, json={'query': query_lista})
print(response.text)