import requests
# Definir la URL del servidor GraphQL
url = 'http://localhost:8000/graphql'

print("listar las plantas")
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
            nombre
            especie
            edad
            altura
            frutos
            
        }
    }
"""
# Solicitud POST al servidor GraphQL
response = requests.post(url, json={'query': query})
print(response.text)
print("-----planta x altura-----------")
# Definir la consulta GraphQL por  Buscar las plantas que tienen frutos
query = """
    {
        plantaPorAltura(altura:20){
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
response = requests.post(url, json={'query': query})
print(response.text)

print("-----planta x altura-----------")
# Definir la consulta GraphQL por  Buscar las plantas que tienen frutos
query = """
    {
        plantaPorFruto(frutos:True){
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
response = requests.post(url, json={'query': query})
print(response.text)




# Definir la consulta GraphQL para crear nuevo estudiante


query_actulizar = """
mutation {
        actulizarPlanta(id:1,edad:20,altura:100) {
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

response_mutation = requests.post(url, json={'query': query_actulizar})
print(response_mutation.text)

# Lista de todos los estudiantes
response = requests.post(url, json={'query': query_lista})
print(response.text)



print("MUTATION")
# Definir la consulta GraphQL para crear nuevo estudiante
query_crear = """
mutation {
        crearPlanta(nombre="Alfalfa", especie="Armeria", edad=30, altura=40,frutos=True) {
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

# Definir la consulta GraphQL para eliminar un 
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