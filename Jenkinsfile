pipeline {
    agent any

    environment {
        IMAGE_NAME = 'roommate-recommender:latest'
    }

    stages {
        stage('Build Docker Image') {
            steps {
                bat '''
                call minikube docker-env --shell=cmd > minikube_env.bat
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
                    kubectl apply -f deployment.yaml
                    kubectl apply -f service.yaml
                    '''
                }
            }
        }

        stage('Get App URL') {
            steps {
                bat 'minikube service roommate-recommender-service --url'
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
