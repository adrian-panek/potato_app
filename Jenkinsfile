pipeline {
    agent { docker {image 'python'} }
    stages {
        stage('List all downloaded files'){
            steps {
                sh('ls -a')
            }
        }
        stage('Update dependency manager'){
            steps {
                sh('pip install --upgrade pip')
            }
        }
        stage('Install all required dependencies'){
            steps {
                sh('pip install -r requirements.txt --user')
            }
        }
    } //stages
} //pipeline