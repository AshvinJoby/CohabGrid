pipeline {
    agent any

    environment {
        IMAGE_NAME = 'roommate-recommender:latest'
        MINIKUBE_PATH = '"C:\\Program Files\\Minikube\\minikube.exe"'
    }

    stages {
        stage('Check Minikube') {
            steps {
                bat '''
                echo Starting Minikube if not running...
                %MINIKUBE_PATH% status || %MINIKUBE_PATH% start --driver=docker
                '''
            }
        }

        stage('Build Docker Image (Docker Desktop)') {
            steps {
                bat '''
                echo Building Docker image using Docker Desktop...
                docker build -t %IMAGE_NAME% .
                '''
            }
        }

        stage('Load Image into Minikube') {
            steps {
                bat '''
                echo Loading image into Minikube...
                %MINIKUBE_PATH% image load %IMAGE_NAME%
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                    bat '''
                    echo Applying Kubernetes manifests...
                    kubectl apply -f deployment.yaml
                    kubectl apply -f service.yaml
                    '''
                }
            }
        }

        stage('Get App URL') {
            steps {
                bat '''
                echo Getting Minikube service URL...
                %MINIKUBE_PATH% service roommate-recommender-service --url
                '''
            }
        }
    }

    post {
        success {
            echo 'Deployment complete'
        }
        failure {
            echo 'Deployment failed'
        }
    }
}
