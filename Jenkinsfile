pipeline {
    agent any

    environment {
        KUBECONFIG = "C:\\Users\\ashvin\\.kube\\config"
        PATH = "${env.PATH};C:\\Program Files\\Docker\\Docker\\resources\\bin;C:\\Program Files\\Docker;C:\\Program Files\\Minikube;C:\\Program Files\\Kubernetes"
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

        stage('Build Docker Image inside Minikube') {
            steps {
                bat '''
                    echo 🛠️ Setting Minikube Docker daemon environment...

                    :: You can also dynamically extract these using:
                    :: minikube -p minikube docker-env --shell=cmd

                    set DOCKER_TLS_VERIFY=1
                    set DOCKER_HOST=tcp://127.0.0.1:51607
                    set DOCKER_CERT_PATH=C:\\Users\\ashvin\\.minikube\\certs
                    set MINIKUBE_ACTIVE_DOCKERD=minikube
                    set PATH=%PATH%;C:\\Program Files\\Docker\\Docker\\resources\\bin;C:\\Program Files\\Docker

                    echo 🛠️ Confirming Docker info:
                    docker info

                    echo 🛠️ Building image:
                    docker build -t cohabgrid-app .
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat '''
                    echo 📦 Deploying app to Kubernetes...
                    kubectl apply -f k8s/
                '''
            }
        }

        stage('Wait for Pod to Run') {
            steps {
                bat '''
                    SET /A RETRIES=30

                    :waitForPod
                    SET FOUND=
                    FOR /F "tokens=* USEBACKQ" %%i IN (`kubectl get pods -l app=cohabgrid --no-headers`) DO (
                        SET FOUND=1
                    )
                    IF NOT DEFINED FOUND (
                        echo 🔁 Pod not yet created. Retrying...
                        ping 127.0.0.1 -n 4 >nul
                        SET /A RETRIES-=1
                        IF %RETRIES% GTR 0 GOTO waitForPod
                        echo ❌ Timed out waiting for pod to appear.
                        exit /b 1
                    )

                    FOR /F "delims=" %%i IN ('"kubectl get pods -l app=cohabgrid --sort-by=.metadata.creationTimestamp -o jsonpath={.items[-1].metadata.name}"') DO (
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
                    echo 🌐 Getting app URL...
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
