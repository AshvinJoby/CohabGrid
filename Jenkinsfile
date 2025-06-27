pipeline {
    agent any

    environment {
        IMAGE_NAME = 'roommate-recommender:latest'
        MINIKUBE_EXE = 'C:\\Program Files\\Minikube\\minikube.exe'
    }

    stages {
        stage('Start Minikube') {
            steps {
                bat '''
                echo Starting Minikube if not already running...
                "%MINIKUBE_EXE%" status || "%MINIKUBE_EXE%" start --driver=docker
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                bat '''
                call "%MINIKUBE_EXE%" docker-env --shell=cmd > minikube_env.bat
                call minikube_env.bat
                docker build -t %IMAGE_NAME% .
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                    bat '''
                    echo Deploying to Kubernetes using Jenkins kubeconfig credential...
                    kubectl apply -f deployment.yaml --validate=false
                    kubectl apply -f service.yaml --validate=false
                    '''
                }
            }
        }

        stage('Get App URL') {
            steps {
                bat '"%MINIKUBE_EXE%" service roommate-recommender-service --url'
            }
        }
    }

    post {
        success {
            echo '✅ Deployment complete'
        }
        failure {
            echo '❌ Deployment failed'
        }
    }
}
