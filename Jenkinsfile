pipeline {
    agent any

    environment {
        IMAGE_NAME = 'roommate-recommender:latest'
    }

    stages {
        stage('Build Image in Minikube') {
            steps {
                sh '''
                eval $(minikube docker-env)
                docker build -t $IMAGE_NAME .
                '''
            }
        }

        stage('Deploy to Minikube') {
            steps {
                sh '''
                kubectl apply -f deployment.yaml
                kubectl apply -f service.yaml
                '''
            }
        }
    }

    post {
        success {
            sh "minikube service roommate-recommender-service --url"
        }
    }
}
