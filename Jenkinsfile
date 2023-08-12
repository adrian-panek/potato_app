pipeline {
    agent { docker {image 'python'} }
    stages {
        stage('List all downloaded files'){
            steps {
                sh('ls -a')
            }
        }
        stage('Install all required dependencies'){
            steps {
                sh('pip install -r requirements.txt')
            }
        }
    } //stages
} //pipeline