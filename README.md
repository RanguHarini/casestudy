# Study Notes Organizer — DevOps Case Study

A Flask web app for adding, viewing, searching and deleting study notes. Includes Docker, Kubernetes and Jenkins starter configuration.

## Pages
- `/` Home dashboard
- `/add` Add a note
- `/notes` View and delete notes
- `/search` Search notes
- `/health` Health check

## Run locally (Windows PowerShell)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```
Open http://localhost:5001. If activation is blocked, run pip install and python app.py without activating.

## Docker
```powershell
docker build -t study-notes-organizer:local .
docker run -d --name study-notes-test -p 5001:5001 study-notes-organizer:local
```
Open http://localhost:5001. Clean up with `docker stop study-notes-test` and `docker rm study-notes-test`.

## Kubernetes
Ensure Docker Desktop and Minikube are running. Replace `YOUR_DOCKERHUB_USERNAME` in the deployment and Jenkinsfile after creating your Docker Hub repository.
```powershell
minikube start --driver=docker
kubectl apply -f k8s/pvc.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl get pods
kubectl port-forward service/study-notes-service 8080:5001
```
Open http://localhost:8080. The image must exist in Docker Hub before applying the deployment.

## GitHub
Create an empty GitHub repository, then:
```powershell
git init
git add .
git commit -m "Initial Study Notes Organizer application"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/study-notes-organizer.git
git push -u origin main
```

## Jenkins setup
Create a Pipeline job configured as **Pipeline script from SCM**, Git, repository URL, branch `*/main`, script path `Jenkinsfile`.
Create credentials:
- `dockerhub-creds`: username with password; use Docker Hub access token as password.
- `kubeconfig-file`: secret file containing a kubeconfig that works from the Jenkins agent.

The Jenkins agent must be able to run Docker and kubectl and access the cluster. Local Minikube access from a Windows Jenkins service can require extra service-account and kubeconfig setup. The Jenkinsfile uses SCM polling roughly every minute. GitHub webhooks require a secure, externally reachable Jenkins URL; `localhost` is not reachable by GitHub.

## Notes
- Replace all `YOUR_DOCKERHUB_USERNAME` placeholders.
- Do not commit credentials, access tokens, virtual environments, or local database files.
- One replica is configured because sharing a SQLite database across multiple pods is not a robust production setup. Use PostgreSQL or another database service for production.
