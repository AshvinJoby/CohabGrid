pipeline {
    agent any

    environment {
        // ✅ Point directly to Minikube's real kubeconfig
        KUBECONFIG = "C:\\Users\\ashvin\\.kube\\config"
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
                    echo 📦 Checking Minikube status...
                    minikube status
                    IF %ERRORLEVEL% NEQ 0 (
                        echo 🚀 Starting Minikube...
                        minikube start --driver=docker --embed-certs=true
                    ) ELSE (
                        echo ✅ Minikube already running
                    )
                '''
            }
        }

        stage('Debug Cluster Access') {
            steps {
                bat '''
                    echo 🔍 Verifying Minikube and kubectl access...
                    minikube status
                    kubectl config current-context
                    kubectl get nodes
                '''
            }
        }

        stage('Wait for Kubernetes API Server') {
            steps {
                bat '''
                    echo ⏳ Waiting for Kubernetes API server...

                    set COUNT=0
                    :loop
                    kubectl get nodes >nul 2>&1
                    if %ERRORLEVEL% EQU 0 (
                        echo ✅ Kubernetes API server is ready!
                        goto done
                    )
                    if %COUNT% GEQ 15 (
                        echo ❌ Kubernetes API server did not start in time.
                        exit /b 1
                    )
                    echo ⏳ Still waiting... (%COUNT%/15)
                    set /a COUNT+=1
                    timeout /t 5 >nul
                    goto loop
                    :done
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                bat '''
                    echo 🛠️ Building Docker image...
                    docker build -t cohabgrid-app .
                    echo ♻️ Loading Docker image into Minikube...
                    minikube image load cohabgrid-app
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat '''
                    echo 📦 Deploying to Kubernetes...
                    kubectl apply -f k8s/
                '''
            }
        }

        stage('Wait for Pod to Run') {
            steps {
                bat '''
                    echo ⏳ Waiting for pod to be ready...
                    FOR /F "delims=" %%i IN ('kubectl get pods -l app^=cohabgrid --field-selector=status.phase^=Running --sort-by=.metadata.creationTimestamp -o "jsonpath={.items[-1].metadata.name}"') DO (
                        echo 🔍 Waiting on pod: %%i
                        kubectl wait --for=condition=ready pod %%i --timeout=90s
                        if ERRORLEVEL 1 (
                            echo ❌ Pod did not start in time.
                            exit /b 1
                        )
                    )
                    
                '''
            }
        }

        stage('Get App URL') {
            steps {
                bat '''
                    echo 🌐 Getting app URL...
                    minikube service cohabgrid-service --url
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