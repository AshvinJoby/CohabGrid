pipeline {
    agent any

    environment {
        KUBECONFIG = "${WORKSPACE}\\.kube\\config"
        PATH = "${env.PATH};C:\\Program Files\\Docker;C:\\Program Files\\Minikube;C:\\Program Files\\Kubernetes"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Start Minikube') {
            steps {
                bat '''
                    echo 🧱 Checking Minikube status...
                    minikube status >nul 2>&1
                    IF ERRORLEVEL 1 (
                        echo ▶ Starting Minikube in background...
                        start /B "" minikube start --driver=docker --embed-certs=true
                        timeout /t 30
                    ) ELSE (
                        echo ✅ Minikube already running.
                    )
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                bat '''
                    echo 🛠️ Building Docker image...
                    docker build -t cohabgrid-app .
                '''
            }
        }

        stage('Load Image into Minikube') {
            steps {
                bat '''
                    echo 📦 Loading image into Minikube...
                    minikube image load cohabgrid-app
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat '''
                    echo 🚀 Deploying Kubernetes resources...
                    kubectl apply -f k8s/
                    kubectl rollout restart deployment cohabgrid-deployment
                '''
            }
        }

        stage('Wait for Pod to be Ready') {
            steps {
                bat '''
                    echo ⏳ Waiting for pod to be ready...
                    FOR /F "delims=" %%i IN ('kubectl get pods -l app=cohabgrid --field-selector status.phase=Running --sort-by=.metadata.creationTimestamp -o "jsonpath={.items[-1].metadata.name}"') DO (
                        echo 🔍 Waiting on pod: %%i
                        kubectl wait --for=condition=ready pod %%i --timeout=90s
                        IF ERRORLEVEL 1 (
                            echo ❌ Pod did not become ready in time.
                            exit /b 1
                        )
                    )
                '''
            }
        }

        stage('Get App URL') {
            steps {
                bat '''
                    echo 🌐 Getting app URL from service...
                    FOR /F %%i IN ('kubectl get svc cohabgrid-service -o jsonpath^="{.spec.ports[0].nodePort}"') DO (
                        echo ✅ App is available at: http://127.0.0.1:%%i
                    )
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
