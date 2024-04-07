import requests

url = "http://localhost:8000/pacientes"
headers = {'Content-type': 'application/json'}

print("--- Pacientes actuales ---")
get_response = requests.get(url)
print(get_response.text)

print("--- ---")
nuevo_paciente = {
    "ci": 456789,
    "nombre": "Marta",
    "apellido": "Zamora",
    "edad": 20,
    "genero": "Femenino",
    "diagnostico": "Diabetes",
    "doctor": "Doctora Gabriela Flores",
}
response = requests.post(url, json=nuevo_paciente, headers=headers)
print(response.text)

print("--- LISTAR A LOS PACIENTES ---")
response = requests.get(url)
print(response.text)

print("--- Pacientes con ci ---")
ci = 456789
response_ci = requests.get(f"{url}/{ci}")
print(response_ci.text)

print("--- Pacientes con diabetes ---")
diagnostico = "Diabetes"
response2 = requests.get(f"{url}/?diagnostico={diagnostico}")
print(response2.text)
print("--- Pacientes con el doctor ---")

doctor = "Doctor Pedro Perez"
response2 = requests.get(f"{url}/?doctor={doctor}")
print(response2.text)

print("--- PUT paciente con CI---")
ci = 456789
actualizacion_paciente = {
    "edad": 60,
    "doctor": "Doctor Pedro Perez",
}
response = requests.put(f"{url}/{ci}", json=actualizacion_paciente)
print(response.text)

print("--- DELETE pacinte ---")
ci = 8464559
response = requests.delete(f"{url}/{ci}")
print(response.text)

print("--- Pacientes Actuales ---")
response = requests.get(url)
print(response.text)