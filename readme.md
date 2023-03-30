**Receipt generator** — API for "Zhrachka top"

# Installation

```sh
git clone https://github.com/ye11ow-banana/receipt_generator.git
```

Install dependencies to your virtual environment
```sh
pip install -r requirements.txt
```

Run celery
```sh
celery -A config worker -l info
```

Run Django
```sh
python3 manage.py migrate
```
```sh
python3 manage.py runserver
```

Set environment variables to .env file
```sh
SECRET_KEY=

POSTGRES_NAME=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=localhost
POSTGRES_PORT=5001

REDIS_HOST=localhost
REDIS_PORT=6000
```

Run docker

```sh
docker-compose up
```

---

## Here we go...