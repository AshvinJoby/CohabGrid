pipeline {
    agent any

    environment {
        KUBECONFIG = "C:\\Users\\ashvin\\.kube\\config"
        PATH = "C:\\Program Files\\Kubernetes;C:\\Program Files\\Docker;C:\\Program Files\\Minikube;${env.PATH}"
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
                echo ✅ Checking Minikube status...
                "C:\\Program Files\\Minikube\\minikube.exe" status
                if errorlevel 1 (
                    echo 🔄 Restarting Minikube...
                    "C:\\Program Files\\Minikube\\minikube.exe" delete
                    "C:\\Program Files\\Minikube\\minikube.exe" start --driver=docker
                ) else (
                    echo 🚀 Minikube already running.
                )
                '''
            }
        }

        stage('Inject Minikube Env') {
            steps {
                bat '''
                echo 🌐 Setting Minikube Docker environment for Jenkins shell
                for /f "tokens=*" %%i in ('"C:\\Program Files\\Minikube\\minikube.exe" -p minikube docker-env --shell cmd') do call %%i
                '''
            }
        }

        stage('Wait for Kubernetes API Server') {
            steps {
                bat '''
                echo 🕒 Waiting for Kubernetes API server...
                set COUNT=0
                :retry
                kubectl get nodes > nul 2>&1
                if %errorlevel%==0 (
                    echo ✅ Kubernetes API server is ready!
                ) else (
                    if %COUNT% GEQ 15 (
                        echo ❌ Kubernetes API server did not start in time.
                        exit /b 1
                    )
                    echo ⏳ Still waiting... (%COUNT%/15)
                    timeout /t 10 > nul
                    set /a COUNT+=1
                    goto retry
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
                echo 🌐 Fetching app service URL...
                "C:\\Program Files\\Minikube\\minikube.exe" service cohabgrid-service --url
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
