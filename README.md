# backend-whatsapp-ai

## General

Este es un proyecto para levantar un endpoint para automatizar un bot de whatsapp usando LLM, especificamente, con Groq.

## Pre Requisitos

Para usar este repositorio, se debe tener los siguientes pre-requisitos:

- Api Key en Groq. Esto se puede obtener desde https://groq.com/ de manera gratuita.
- Base de datos de Cosmo DB en Azure, generando una BBDD y contenedor llamada chat_message y History respectivamente.
- Tener instalado Docker en el computador.

## Ajustar .env

Luego de las configuraciones, se debe añadir las contraseñas en el archivo .env, tanto para Groq y CosmoDB Azure. El archivo es el siguiente:

```bash
TOKEN_VERIFICACION=AR5VeJoKXytJkqAuYuvpourVRWUFEAjVzZE4yHRJe49mz3HDUjpb6B26fOX4GHDo
COSMOS_DB_URL=
COSMOS_DB_KEY=
COSMOS_DB_NAME=chat_message
COSMOS_DB_CONTAINER_CHAT_HISTORY=History
API_KEY_GROQ=
PERMANENT_TOKEN_FACEBOOK=
```

## DockerFile

Para levantar el dockerfile, se debe utilizar el siguiente comando:

```bash
docker build -t backend-whatsapp-ai .
```

Despues de tener la image construida, se puede ejecutar con el siguiente comando:

```bash
docker run --name backend-whatsapp-ai -p 8000:8000 -d backend-whatsapp-ai
```