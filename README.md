## Clone project
### All command runned inside hr-sheets directory

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

## install requirements
```bash
$ pip install -r requirements.txt
```

## collect static files
```bash
$ python3 manage.py collectstatic
```

## Migration
```bash
$ python3 manage.py migrate
```

## run app
```bash
$ python3 manage.py runserver # default 8000
```

## run app different port
```bash
$ python3 manage.py runserver 8081 # different port
```


