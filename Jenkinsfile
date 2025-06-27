pipeline {
    agent any

    environment {
        IMAGE_NAME = 'roommate-recommender:latest'
    }

    stages {
        stage('Build Docker Image inside Minikube') {
            steps {
                bat '''
                echo Setting Minikube Docker environment...
                call minikube docker-env --shell=cmd > minikube_env.bat
                call minikube_env.bat

                echo Building Docker image inside Minikube...
                docker build -t %IMAGE_NAME% .
                '''
            }
        }

        stage('Deploy to Minikube') {
            steps {
                bat '''
                echo Deploying to Kubernetes...
                kubectl apply -f deployment.yaml
                kubectl apply -f service.yaml
                '''
            }
        }

        stage('Get App URL') {
            steps {
                bat '''
                echo Fetching Service URL...
                minikube service roommate-recommender-service --url > url.txt
                type url.txt
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
