

## Generar SSL
```bash
mkdir ssl 

# Server
openssl genrsa -out ssl/server.key 2048
openssl req -new -x509 -key ssl/server.key -out ssl/server.cert -days 3650 -subj "/C=UY/ST=Montevideo/L=Montevideo/O=OneByt/OU=IT/CN=Server"

# Client
openssl genrsa -out ssl/client.key 
openssl req -new -x509 -key ssl/client.key -out ssl/client.cert -days 365 -subj "/C=UY/ST=Montevideo/L=Montevideo/O=OneByt/OU=IT/CN=Client"
```