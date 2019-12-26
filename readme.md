# docker+django+vue+nginx

## Getting Started

### env
```
pyenv global 3.7.2 
virtualenv env 
pip install -r requirements.txt 
``` 

### prod 
```
docker-compose -f docker-compose.prod.yml up -d --build
``` 


http://localhost:1337/ 

### dev 

```
docker-compose -f docker-compose.yml up -d --build
``` 


http://localhost:8000/

