# JWTAuth-FastAPI


- Generating Private and Public key 

```bash

ssh-keygen -t rsa -b 4096 -m PEM -f jwtRS256.key
# Don't add passphrase
openssl rsa -in jwtRS256.key -pubout -outform PEM -out jwtRS256.key.pub

#or

openssl rand -hex 32

```
