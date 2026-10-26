# CI/CD Pipeline with GitHub Actions and Docker

Every push to `main` automatically **tests** a Flask application, **builds** a Docker image and **pushes** it to Docker Hub. The image is then deployed locally with Docker Compose.

Built as part of the 2-week DevOps internship at **Elevate Labs**.

## Pipeline

```
git push ──▶ GitHub Actions
                 │
                 ├─ Job 1: test              (pytest)
                 │        │ passes?
                 │        ▼
                 └─ Job 2: build-and-push    (docker build, push to Docker Hub)
                                │
                                ▼
                       Docker Hub: <user>/flask-cicd-demo:latest and :<commit-sha>
                                │
                                ▼
                  docker compose pull && up   (local deployment)
```

If the tests fail, Job 2 never runs, so a broken build is never published. Pull requests run the tests only.

## Project structure

```
.
├── app.py                         Flask app (/, /health, /api/add)
├── tests/test_app.py              pytest tests
├── requirements.txt               runtime dependencies
├── requirements-dev.txt           adds pytest
├── pytest.ini
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
├── .github/workflows/ci-cd.yml    the pipeline
└── docs/                          report and screenshots
```

## Endpoints

| Endpoint | Response |
|---|---|
| `GET /` | message, version and short commit SHA of the running build |
| `GET /health` | `{"status": "ok"}` |
| `GET /api/add?a=2&b=3` | `{"result": 5.0}` (400 on missing or non-numeric input) |

## Setup

### 1. Accounts
- **GitHub** account: https://github.com
- **Docker Hub** account: https://hub.docker.com (remember your *username*, not your email)

### 2. Create a Docker Hub access token
Docker Hub → Account settings → **Personal access tokens** → *Generate new token*. Name it `github-actions`, give it **Read & Write** access, and copy the token (it is shown only once).

### 3. Create the GitHub repository
Create an empty repository named `flask-cicd-demo` (no README, since this folder already has one).

### 4. Add the secrets
Repository → **Settings → Secrets and variables → Actions → New repository secret**

| Name | Value |
|---|---|
| `DOCKERHUB_USERNAME` | your Docker Hub username |
| `DOCKERHUB_TOKEN` | the access token from step 2 |

### 5. Push the code
```bash
git init -b main
git add .
git commit -m "Initial commit: Flask app with CI/CD pipeline"
git remote add origin https://github.com/<your-username>/flask-cicd-demo.git
git push -u origin main
```
GitHub no longer accepts account passwords for `git push`. Use `gh auth login` (GitHub CLI) or a personal access token.

Open the **Actions** tab and watch the pipeline run. Both jobs should turn green.

## Run the tests locally
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -v
```

## Deploy locally with Docker Compose

Pull and run the image the pipeline pushed:
```bash
export DOCKERHUB_USERNAME=<your-dockerhub-username>
docker compose pull
docker compose up -d
curl localhost:5000/health
curl localhost:5000/
```

Or build locally without Docker Hub: `docker compose up --build -d`

## Demo: change code, push, watch

1. Edit the message in `app.py` (for example `Hello from the CI/CD pipeline! v2`).
2. `git commit -am "Update greeting" && git push`
3. Watch the run in the Actions tab.
4. Redeploy and confirm the commit SHA changed:
   ```bash
   docker compose pull && docker compose up -d
   curl localhost:5000/
   ```

## Cleanup
```bash
docker compose down
```

## Tools used
GitHub Actions, Docker, Docker Hub, Docker Compose, Python (Flask, pytest, gunicorn), Git, WSL2 Ubuntu
