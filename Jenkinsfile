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
                bat '''
                    echo 🕒 Waiting for Kubernetes API server...
                    set COUNT=0
                    :retry
                    %KUBECTL_PATH% get nodes >nul 2>&1
                    if %errorlevel%==0 (
                        echo ✅ Kubernetes API server is ready!
                    ) else (
                        if %COUNT% GEQ 15 (
                            echo ❌ Kubernetes API server did not start in time.
                            exit /b 1
                        )
                        echo Waiting 10 seconds...
                        timeout /t 10 >nul
                        set /a COUNT+=1
                        goto retry
                    )
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
