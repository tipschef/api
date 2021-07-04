# TipsChef API

## Installation locale
### Installation des prérequis
 - Version de python : 3.8
 - Dépendances python : `pip install -r requirements.txt`

### Variable d'environnement
 - ID du projet GCP: `PROJECT_ID`=`tipschef-ENV`
 - Environnement de lancement: `PROJECT_ENV`=`dev` ou `prod`

### Avoir un secret dans GCP
 - Nom : `secret-api-ENV`
 - format : 
    ```
   {
    "mysql_account": "",
    "mysql_port": ,
    "mysql_password": "",
    "mysql_hostname":"",
    "stripe_api_key": ""
    }
    ```
### Lancement

 - `python -m app/main.py`
## Api urls

- api: http://localhost:8080
- Redoc: http://localhost:8080/redoc
- Swagger: http://localhost:8080/docs
