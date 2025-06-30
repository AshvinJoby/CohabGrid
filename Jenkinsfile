pipeline {
    agent any

    environment {
        KUBECONFIG = "C:\\Users\\ashvin\\.kube\\config"
        DOCKER_HOST = 'npipe:////./pipe/docker_engine'
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
                    echo Checking Minikube status...
                    minikube status
                    IF %ERRORLEVEL% NEQ 0 (
                        echo Starting Minikube...
                        minikube start --driver=docker --embed-certs=true
                    ) ELSE (
                        echo Minikube already running.
                    )
                '''
            }
        }

        stage('Debug Cluster Access') {
            steps {
                bat '''
                    echo Verifying Minikube and kubectl access...
                    minikube status
                    kubectl config current-context
                    kubectl get nodes
                '''
            }
        }

        stage('Wait for Kubernetes API Server') {
            steps {
                bat '''
                    echo Waiting for Kubernetes API server...

                    set COUNT=0
                    :loop
                    kubectl get nodes >nul 2>&1
                    if %ERRORLEVEL% EQU 0 (
                        echo Kubernetes API server is ready!
                        goto done
                    )
                    if %COUNT% GEQ 15 (
                        echo Kubernetes API server did not start in time.
                        exit /b 1
                    )
                    echo Still waiting... (%COUNT%/15)
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
                    echo Setting Minikube Docker daemon environment...

                    :: You can also dynamically extract these using:
                    :: minikube -p minikube docker-env --shell=cmd

                    set DOCKER_TLS_VERIFY=1
                    set DOCKER_HOST=tcp://127.0.0.1:51607
                    set DOCKER_CERT_PATH=C:\\Users\\ashvin\\.minikube\\certs
                    set MINIKUBE_ACTIVE_DOCKERD=minikube
                    set PATH=%PATH%;C:\\Program Files\\Docker\\Docker\\resources\\bin;C:\\Program Files\\Docker

                    echo Confirming Docker info:
                    docker info

                    echo Building image:
                    docker build -t cohabgrid-app .
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat '''
                    echo Deploying app to Kubernetes...
                    kubectl apply -f k8s/
                '''
            }
        }

        stage('Wait for Pod to Run') {
            steps {
                bat 'scripts\\wait_for_pod.bat'
            }
        }

        stage('Get App URL') {
            steps {
                bat '''
                    echo Getting app URL...
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
