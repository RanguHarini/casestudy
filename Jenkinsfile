
pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    triggers {
        pollSCM('H/1 * * * *')
    }

    environment {
        DOCKERHUB_REPO = 'ranguharini/study-notes-organizer'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t "%DOCKERHUB_REPO%:latest" .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKERHUB_USER',
                        passwordVariable: 'DOCKERHUB_TOKEN'
                    )
                ]) {
                    bat 'echo %DOCKERHUB_TOKEN%| docker login --username "%DOCKERHUB_USER%" --password-stdin'
                    bat 'docker push "%DOCKERHUB_REPO%:latest"'
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([
                    file(
                        credentialsId: 'kubeconfig-file',
                        variable: 'KUBECONFIG'
                    )
                ]) {
                    bat 'kubectl apply -f k8s\\pvc.yaml'
                    bat 'kubectl apply -f k8s\\deployment.yaml'
                    bat 'kubectl apply -f k8s\\service.yaml'
                    bat 'kubectl get pods'
                    bat 'kubectl get services'
                }
            }
        }
    }

    post {
        success {
            echo 'Study Notes Organizer deployed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check the Console Output for the error.'
        }
        always {
            echo 'CI/CD pipeline execution completed.'
        }
    }
}
