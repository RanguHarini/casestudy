pipeline {
    agent any
    triggers {
        // Polls SCM approximately every minute; a GitHub webhook is another option.
        pollSCM('H/1 * * * *')
    }
    environment {
        DOCKERHUB_REPO = 'ranguharini/study-notes-organizer'
        K8S_DIR = 'k8s'
    }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Build and Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DH_USER', passwordVariable: 'DH_TOKEN')]) {
                    powershell '''
                        $ErrorActionPreference = "Stop"
                        $env:DH_TOKEN | docker login -u $env:DH_USER --password-stdin
                        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
                    '''
                    bat '''
                        docker build -t %DOCKERHUB_REPO%:%BUILD_NUMBER% .
                        if errorlevel 1 exit /b 1
                        docker push %DOCKERHUB_REPO%:%BUILD_NUMBER%
                        if errorlevel 1 exit /b 1
                    '''
                }
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig-file', variable: 'KUBECONFIG')]) {
                    bat '''
                        kubectl apply -f %K8S_DIR%\pvc.yaml
                        if errorlevel 1 exit /b 1
                        kubectl apply -f %K8S_DIR%\deployment.yaml
                        if errorlevel 1 exit /b 1
                        kubectl apply -f %K8S_DIR%\service.yaml
                        if errorlevel 1 exit /b 1
                        kubectl set image deployment/study-notes-organizer study-notes-organizer=%DOCKERHUB_REPO%:%BUILD_NUMBER%
                        if errorlevel 1 exit /b 1
                        kubectl rollout status deployment/study-notes-organizer --timeout=180s
                    '''
                }
            }
        }
    }
    post {
        success { echo 'Study Notes Organizer deployed successfully!' }
        failure { echo 'Pipeline failed. Check the Jenkins console output.' }
    }
}
