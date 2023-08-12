pipeline {
    agent { docker {image 'python'} }
    stages {
        stage('Checkout Repository'){
            steps {
                git branch: 'jenkins', credentialsId: 'e7ac38b9-2a09-4d78-8608-8fc1179b55b2', url: 'https://github.com/adrian-panek/potato_app'
            }
        }
        stage('List all downloaded files'){
            steps {
                sh('ls -a')
            }
        }
    } //stages
} //pipeline