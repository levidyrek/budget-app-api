pipeline {
    agent none
    stages {
        stage('Build') {
            agent any
            steps {
                script {
                    checkout scm
                    def image = docker.build("budget-rest-api:${env.BUILD_ID}")
                    image.push('latest')
                }
            }
        }
        stage('Test') {
            agent {
                docker { image 'budget-rest-api:latest' }
            }
            steps {
                sh 'python manage.py jenkins --enable-coverage'
            }
            post {
                always {
                    junit 'reports/junit.xml'
                }
            }
        }
    }
}
