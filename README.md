# I1677 - API para Fiesta

Se desarrollara un backend expuesto para gestionar el almacenamiento y acceso a la información de los invitados y premios de la fiesta de la empresa.

```
# Python
Python==3.11.9

# Dependencias (local)
pip install -r requirements.txt

# Web server
Uvicorn

# IP Servers
PRD: 192.25.33.75
QAS: 192.25.33.55

# Ejecución
uvicorn main:app --reload

# Dependencias
requirements.txt

# Base de datos local y auto-contenida
sqlite:///./database/vitaFiesta.db
(Habrá dos BBDD una en QAS y otra en PRD)

# API Docs
api/api.py

# DNS
QAS: https://url-qas.asd.com.ar
PRD: https://url-prd.asd.com.ar

# AUTENTICACION: API KEY
- Variables de entorno
    - API key
    - API key name
- Endpoints parametrizados
    - url/endpoint/<API_KEY_NAME>=<API_KEY>

# ENDPOINTS
QAS:
https://url-prd.asd.com.arconsulta_premios/{telefono_invitado} [RL:25/min]
https://url-prd.asd.com.ar/consulta_invitados/{telefono} [RL:25/min]
https://url-prd.asd.com.ar/consulta_invitados [RL:25/min]
https://url-prd.asd.com.ar/consulta_premios [RL:25/min]
https://url-prd.asd.com.ar/invitados [RL:25/min]
https://url-prd.asd.com.ar/premios [RL:25/min]
https://url-prd.asd.com.ar/carga_masiva [RL:1/min]
https://url-prd.asd.com.ar/reset_db [RL:1/min]

PRD:
https://url-prd.asd.com.ar/consulta_premios/{telefono_invitado} [RL:25/min]
https://url-prd.asd.com.ar/consulta_invitados/{telefono} [RL:25/min]
https://url-prd.asd.com.ar/consulta_invitados [RL:25/min]
https://url-prd.asd.com.ar/consulta_premios [RL:25/min]
https://url-prd.asd.com.ar/invitados [RL:25/min]
https://url-prd.asd.com.ar/premios [RL:25/min]
https://url-prd.asd.com.ar/carga_masiva [RL:1/min]
https://url-prd.asd.com.ar/reset_db [RL:1/min]

```