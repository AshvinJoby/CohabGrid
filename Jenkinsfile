pipeline {
    agent any

    environment {
        KUBECONFIG = 'C:\\WINDOWS\\system32\\config\\systemprofile\\.kube\\config'
    }

    stages {
        stage('Start Minikube') {
            steps {
                bat '''
                    echo ✅ Starting Minikube...
                    "C:\\Program Files\\Minikube\\minikube.exe" status || (
                        "C:\\Program Files\\Minikube\\minikube.exe" delete &&
                        "C:\\Program Files\\Minikube\\minikube.exe" start --driver=docker
                    )
                '''
            }
        }

        stage('Wait for API Server') {
            steps {
                bat '''
                    echo 🕒 Waiting for Kubernetes API server...
                    for /l %%x in (1, 1, 15) do (
                        kubectl get nodes && goto ready
                        echo Waiting 10 seconds...
                        timeout /t 10 > nul
                    )
                    echo ❌ Kubernetes API server did not start in time.
                    exit /b 1

                    :ready
                    echo ✅ API server is ready.
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                bat '''
                    echo 🐳 Building Docker image...
                    docker build -t roommate-recommender:latest .
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat '''
                    echo 📦 Applying Kubernetes manifests...
                    kubectl config use-context minikube
                    kubectl apply -f deployment.yaml --validate=false
                    kubectl apply -f service.yaml --validate=false
                '''
            }
        }

        stage('Get App URL') {
            steps {
                bat '''
                    echo 🌐 Getting service URL...
                    "C:\\Program Files\\Minikube\\minikube.exe" service roommate-recommender-service --url
                '''
            }
        }
    }

    post {
        failure {
            echo '❌ Deployment failed'
        }
        success {
            echo '✅ Deployment successful'
        }
    }
}
