pipeline {
    agent { docker {image 'python'} }
    stages {
        stage('List all downloaded files'){
            steps {
                sh('ls -a')
            }
        }
        stage('Install all required dependencies'){
            sh('pip install -r requirements.txt')
        }
    } //stages
} //pipeline