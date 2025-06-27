pipeline {
    agent any
    environment {
        IMAGE_NAME = 'ashvinjoby/roommate-app'
        TAG = 'latest'
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
                    docker.build("${IMAGE_NAME}:${TAG}")
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'docker-hub-cred') {
                        docker.image("${IMAGE_NAME}:${TAG}").push()
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG_FILE')]) {
                    script {
                        // Set KUBECONFIG environment variable to the provided config path
                        env.KUBECONFIG = "${KUBECONFIG_FILE}"

                        // Confirm cluster is reachable
                        bat 'kubectl config current-context'
                        bat 'kubectl cluster-info'

                        //validation off
                        bat 'kubectl apply -f streamlit-deployment.yaml --validate=false'
                        bat 'kubectl apply -f service.yaml --validate=false'
                    }
                }
            }
        }

        stage('Run Smoke Test') {
            steps {
                script {
                    echo "Waiting for the application to become available..."
                    bat 'powershell -Command "Start-Sleep -Seconds 60"'

                    def nodeIp = '192.168.49.2'
                    def nodePort = '30545'

                    echo "Testing Streamlit app via curl at http://${nodeIp}:${nodePort}"
                    bat """
                        curl --fail --connect-timeout 10 http://${nodeIp}:${nodePort} || (
                            echo Streamlit app is not reachable at ${nodeIp}:${nodePort}
                            exit /b 1
                        )
                    """
                }
            }
        }
    }
}
