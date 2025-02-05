## Clone project
 Все команды выполняются внутри каталога hr-sheets

## Up project with bash command
```bash
bash main.sh
```

## Create /hr-sheets/.env based on .env.test
```bash
nano .env
```

## Create /hr-sheets/credentials.json based on credential.test.json
```bash
nano credentials.json
```

## Check Python and pip
```bash 
$ python3 --version # Python 3.12.3
$ pip --version # pip 24.0
```

## Create virtual environment
```bash
$ python3 -m venv .venv
```

## Activate virtual environment
```bash
$ source .venv/bin/active
```

## Install requirements
```bash
$ pip install -r requirements.txt
```

## Collect static files
```bash
$ python3 manage.py collectstatic
```

## Migration
```bash
$ python3 manage.py migrate
```

## Run app
```bash
$ python3 manage.py runserver # default 8000
```

## Run app different port
```bash
$ python3 manage.py runserver 8081 # different port
```

### TIP
 - После настройки nginx, staticfiles и media могут быть запрещены, а скрипты/стили/фото могут работать некорректно. в этом случае вам нужно будет предоставить разрешения для папок

### Nginx 

 ```
 server {
    listen 80;
    server_name example.com;

    location /static/ {
        alias /home/user/project/staticfiles/;
    }

    location /media/ {
        alias /home/user/project/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;  # Proxy to Django (Gunicorn/Uvicorn)
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
``` 



