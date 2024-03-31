# favlinks-backend

## Set up

### 1. Create a Virtual Environment, Activate it

```bash
# Create venv called .venv
python3 -m venv .venv

# Activate venv
# On Windows
.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate

```

## 2. Docker compose

```bash
# Go to app directory
cd favlinks_app

# Run docker compose
docker compose up

# In a separate terminal
docker exec -it favlinksserver_web bash

# Run unit tests in same terminal
python manage.py test

```

## 3. View Admin and API Doc 

### Admin
- Head to localhost:8000/admin
- Login with credentials from init_super_user.py script

### Head to localhost:8000/swagger
- Test and view API viewsets
