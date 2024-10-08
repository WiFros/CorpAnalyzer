pipeline {
    agent{
        label 'slave2'
    }

    parameters {
        booleanParam(name: 'BUILD_FRONTEND', defaultValue: true, description: 'Build the frontend project')
        booleanParam(name: 'BUILD_BACKEND', defaultValue: true, description: 'Build the backend project')
    }

    environment {
        FRONTEND_DIR = "${WORKSPACE}/front"
        BACKEND_DIR = "backend"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Frontend') {
            when {
                expression { params.BUILD_FRONTEND }
            }
            stages {
                stage('Setup Environment') {
                    steps {
                        script {
                            // 현재 작업 디렉토리 확인
                            sh "pwd"
                            sh "ls"
                            // front 디렉토리 존재 확인 및 내용 리스트
                            sh "ls -la ${FRONTEND_DIR}"
                            
                            // 환경 파일 복사
                            withCredentials([file(credentialsId: 'react-env-file', variable: 'ENV_FILE')]) {    
                                
                                //sh "cp \$ENV_FILE ${FRONTEND_DIR}/.env"
                                // 복사 후 확인
                                //sh "ls -la ${FRONTEND_DIR}/.env"
                                sh '''
                                    cp \$ENV_FILE ${FRONTEND_DIR}/.env

                                    ls -la ${FRONTEND_DIR}/.env
                                '''

                            }
                        }
                    }
                }

                stage('Install Dependencies') {
                    steps {
                        dir("${FRONTEND_DIR}") {
                            sh 'npm install'
                        }
                    }
                }

                stage('Build') {
                    steps {
                        dir("${FRONTEND_DIR}") {
                            sh 'npm run build'
                        }
                    }
                }

                stage('Test') {
                    steps {
                        dir("${FRONTEND_DIR}") {
                            sh 'npm test'
                        }
                    }
                }

                stage('Deploy') {
                    steps {
                        dir("${FRONTEND_DIR}") {
                            sh 'echo "Deploying frontend..."'
                            // 실제 프론트엔드 배포 명령어를 여기에 추가하세요
                        }
                    }
                }
            }
        }

        stage('Backend') {
            when {
                expression { params.BUILD_BACKEND }
            }
            stages {
                stage('Setup Environment') {
                    steps {
                        dir("${BACKEND_DIR}") {
                            script {
                                withCredentials([file(credentialsId: 'backend-env-file', variable: 'ENV_FILE')]) {
                                    sh "cp \$ENV_FILE .env"
                                }
                            }
                        }
                    }
                }

                stage('Install Dependencies') {
                    steps {
                        dir("${BACKEND_DIR}") {
                            sh 'npm install'  // 또는 해당 백엔드의 의존성 설치 명령어
                        }
                    }
                }

                stage('Build') {
                    steps {
                        dir("${BACKEND_DIR}") {
                            sh 'npm run build'  // 또는 해당 백엔드의 빌드 명령어
                        }
                    }
                }

                stage('Test') {
                    steps {
                        dir("${BACKEND_DIR}") {
                            sh 'npm test'  // 또는 해당 백엔드의 테스트 명령어
                        }
                    }
                }

                stage('Deploy') {
                    steps {
                        dir("${BACKEND_DIR}") {
                            sh 'echo "Deploying backend..."'
                            // 실제 백엔드 배포 명령어를 여기에 추가하세요
                        }
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded! Selected projects have been built and deployed.'
        }
        failure {
            echo 'Pipeline failed. Please check the logs for errors.'
        }
        always {
            script {
                if (params.BUILD_FRONTEND) {
                    sh "rm -f ${FRONTEND_DIR}/.env"
                }
                if (params.BUILD_BACKEND) {
                    sh "rm -f ${BACKEND_DIR}/.env"
                }
            }
        }
    }
}
