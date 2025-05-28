pipeline {
    agent any
    environment {
        IMAGE_NAME = 'ashvinjoby/roommate-app'
    }

    stages {
        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }

        stage('Clone Repo') {
            steps {
                git branch: 'main', url: 'https://github.com/AshvinJoby/CohabGrid.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${IMAGE_NAME}:latest")
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'docker-hub-cred') {
                        docker.image("${IMAGE_NAME}:latest").push()
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG_FILE')]) {
                    script {
                        env.KUBECONFIG = "${KUBECONFIG_FILE}"

                        //deployment and service files
                        bat 'kubectl apply -f streamlit-deployment.yaml'
                        bat 'kubectl apply -f service.yaml'
                    }
                }
            }
        }

        stage('Run Smoke Test') {
            steps {
                script {
                    //Wait for the pod/service to start
                    bat 'timeout /t 30'
                    
                    //NodePort IP
                    bat 'curl 10.101.184.107 '
                }
            }
        }
    }
}
