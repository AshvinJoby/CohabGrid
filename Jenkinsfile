pipeline {
    agent any

    environment {
        KUBECONFIG = "${WORKSPACE}/.kube/config"
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
                    minikube status
                    IF errorlevel 1 (
                        echo "Minikube not running, starting..."
                        minikube start --driver=docker
                    ) ELSE (
                        echo "Minikube is running"
                    )
                '''
            }
        }

        stage('Wait for Kubernetes API Server') {
            steps {
                bat '''
                    echo 🕒 Waiting for Kubernetes API server...

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
                    ping -n 6 127.0.0.1 >nul
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
                    echo ⏳ Waiting for pod to be Running...

                    set COUNT=0
                    :wait_pod
                    kubectl get pods | findstr "cohabgrid" | findstr "Running" >nul
                    if %ERRORLEVEL% EQU 0 (
                        echo ✅ Pod is running!
                        goto showurl
                    )
                    if %COUNT% GEQ 15 (
                        echo ❌ Pod did not start in time.
                        exit /b 1
                    )
                    echo ⏳ Waiting for pod... (%COUNT%/15)
                    set /a COUNT+=1
                    ping -n 6 127.0.0.1 >nul
                    goto wait_pod

                    :showurl
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
