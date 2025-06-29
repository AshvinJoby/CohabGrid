pipeline {
    agent any

    environment {
        IMAGE_NAME = 'cohabgrid-app'
        DEPLOYMENT_NAME = 'cohabgrid-deployment'
        SERVICE_NAME = 'cohabgrid-service'
        APP_LABEL = 'cohabgrid'
        APP_PORT = '8501'
    }

    stages {
        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE_NAME% .'
            }
        }

        stage('Load Image into Minikube') {
            steps {
                bat 'minikube image load %IMAGE_NAME%'
            }
        }

        stage('Apply K8s Manifests') {
            steps {
                bat '''
                    kubectl apply -f k8s/
                    kubectl rollout restart deployment %DEPLOYMENT_NAME%
                '''
            }
        }

        stage('Wait for Pod to be Ready') {
            steps {
                bat '''
                    echo ⏳ Waiting for pod to be ready...
                    SET RETRIES=30
                    SET FOUND=
:waitLoop
                    FOR /F "delims=" %%i IN ('kubectl get pods -l "app=%APP_LABEL%" --field-selector=status.phase=Running --sort-by=.metadata.creationTimestamp -o "jsonpath={.items[-1].metadata.name}"') DO (
                        SET FOUND=1
                        SET POD_NAME=%%i
                        echo 🔍 Found pod: %%i
                        kubectl wait --for=condition=ready pod %%i --timeout=90s
                        IF ERRORLEVEL 1 (
                            echo ❌ Pod did not become ready in time.
                            exit /b 1
                        )
                    )
                    IF NOT DEFINED FOUND (
                        echo 🔁 Pod not yet created. Retrying...
                        timeout /t 3 >nul
                        SET /A RETRIES-=1
                        IF %RETRIES% GTR 0 GOTO waitLoop
                        echo ❌ Timed out waiting for pod to appear.
                        exit /b 1
                    )
                '''
            }
        }

        stage('Port Forward App') {
            steps {
                bat '''
                    FOR /F "delims=" %%i IN ('kubectl get pods -l "app=%APP_LABEL%" --field-selector=status.phase=Running --sort-by=.metadata.creationTimestamp -o "jsonpath={.items[-1].metadata.name}"') DO (
                        echo 🌐 Access your app at: http://localhost:%APP_PORT%
                        start "" cmd /c kubectl port-forward pod/%%i %APP_PORT%:%APP_PORT%
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
