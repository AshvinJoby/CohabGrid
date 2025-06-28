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

                    set COUNT=1
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
                    ping 127.0.0.1 -n 11 >nul
                    goto loop
                    :done
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                bat '''
                    echo 🛠️ Building Docker image inside Minikube...
                    for /f "tokens=*" %%i in ('minikube docker-env --shell=cmd') do call %%i
                    docker build -t cohabgrid-app:latest .
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

        stage('Get App URL') {
            steps {
                bat '''
                    echo 🌐 Waiting for pod to be ready...

                    set COUNT=0
                    :wait_pod
                    kubectl get pods | findstr "cohabgrid" | findstr "Running"
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
                    timeout /t 5 >nul
                    goto wait_pod

                    :showurl
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
