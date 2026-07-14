import secrets
import string
import random

res = ""
with open("docker-compose.exemple.yaml", 'r') as f:
    res = f.read()

res = res.replace("{{postgress_password}}", secrets.token_urlsafe(32))
res = res.replace("{{JWT_TOKEN}}", secrets.token_urlsafe(32))


with open("./docker-compose.yaml", 'w') as f:
    f.write(res)