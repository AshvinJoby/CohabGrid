pipeline {
    agent any

    environment {
        MINIKUBE_PATH = '"C:\\Program Files\\Minikube\\minikube.exe"'
        KUBECTL_PATH = '"C:\\Program Files\\Kubernetes\\kubectl.exe"'
    }

    stages {
        stage('Start Minikube') {
            steps {
                bat '''
                    echo ✅ Checking Minikube status...
                    %MINIKUBE_PATH% status
                    if errorlevel 1 (
                        echo 🔄 Restarting Minikube...
                        %MINIKUBE_PATH% delete
                        %MINIKUBE_PATH% start --driver=docker
                    ) else (
                        echo 🚀 Minikube already running.
                    )
                '''
            }
        }

        stage('Wait for Kubernetes API Server') {
            steps {
                powershell '''
                    Write-Host "🕒 Waiting for Kubernetes API server..."
                    $maxRetries = 15
                    $count = 0
                    while ($count -lt $maxRetries) {
                        kubectl get nodes > $null 2>&1
                        if ($LASTEXITCODE -eq 0) {
                            Write-Host "✅ Kubernetes API server is ready!"
                            exit 0
                        } else {
                            Write-Host "⏳ Still waiting... ($count/$maxRetries)"
                            Start-Sleep -Seconds 10
                            $count++
                        }
                    }
                    Write-Host "❌ Kubernetes API server did not start in time."
                    exit 1
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                bat '''
                    echo 🐳 Building Docker image...
                    docker build -t myapp-image .
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat '''
                    echo 🚀 Deploying to Kubernetes...
                    %KUBECTL_PATH% apply -f k8s/deployment.yaml
                    %KUBECTL_PATH% apply -f k8s/service.yaml
                '''
            }
        }

        stage('Get App URL') {
            steps {
                bat '''
                    echo 🌐 Getting service URL...
                    %MINIKUBE_PATH% service myapp-service --url
                '''
            }
        }
    }

    post {
        failure {
            echo '❌ Deployment failed'
        }
    }
}
