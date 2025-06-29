pipeline {
    agent any

    environment {
        IMAGE_NAME = 'cohabgrid-app'
    }

    stages {

        stage('Start Minikube') {
            steps {
                bat '''
                    echo 🚀 Starting Minikube...
                    minikube start --driver=docker
                    if ERRORLEVEL 1 (
                        echo ❌ Failed to start Minikube.
                        exit /b 1
                    )
                '''
            }
        }

        stage('Wait for Kubernetes API') {
            steps {
                bat '''
                    echo 🕒 Waiting for Kubernetes API to be ready...
                    kubectl wait --for=condition=Ready nodes --timeout=120s
                    if ERRORLEVEL 1 (
                        echo ❌ Kubernetes API server did not become ready.
                        exit /b 1
                    )
                '''
            }
        }

        stage('Set Docker Env (Minikube)') {
            steps {
                bat '''
                    echo 🔧 Configuring Docker to use Minikube daemon...
                    FOR /F "tokens=*" %%i IN ('minikube docker-env --shell cmd') DO CALL %%i
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                bat '''
                    echo 🏗️ Building Docker image...
                    docker build -t %IMAGE_NAME% .
                    if ERRORLEVEL 1 (
                        echo ❌ Docker build failed.
                        exit /b 1
                    )
                '''
            }
        }

        stage('Apply K8s Manifests') {
            steps {
                bat '''
                    echo 📦 Applying Kubernetes manifests...
                    kubectl apply -f k8s/
                    if ERRORLEVEL 1 (
                        echo ❌ Failed to apply manifests.
                        exit /b 1
                    )
                '''
            }
        }

        stage('Wait for Pod to be Ready') {
            steps {
                bat '''
                    SET /A RETRIES^=30
                    :waitForPod
                    SET FOUND=
                    FOR /F "tokens=* USEBACKQ" %%i IN (`kubectl get pods -l app=cohabgrid --no-headers`) DO (
                        SET FOUND=1
                    )
                    IF NOT DEFINED FOUND (
                        echo 🔁 Pod not yet created. Retrying...
                        timeout /t 3 >nul
                        SET /A RETRIES^-=1
                        IF %RETRIES% GTR 0 GOTO waitForPod
                        echo ❌ Timed out waiting for pod to appear.
                        exit /b 1
                    )

                    FOR /F "delims=" %%i IN ('kubectl get pods -l app=cohabgrid --sort-by=.metadata.creationTimestamp -o "jsonpath={.items[-1].metadata.name}"') DO (
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
                    minikube service cohabgrid-service --url
                '''
            }
        }
    }

    post {
        failure {
            echo '❌ Deployment failed'
        }
        success {
            echo '✅ Deployment succeeded'
        }
    }
}
