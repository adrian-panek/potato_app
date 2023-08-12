pipeline {
    agent { docker {image 'python'} }
    stages {
        stage('Checkout Repository'){
            git branch: 'jenkins', credentialsId: 'e7ac38b9-2a09-4d78-8608-8fc1179b55b2', url: 'https://github.com/adrian-panek/potato_app'
        }
        stage('List all downloaded files'){
            sh('ls -a')
        }
    } //stages
} //pipeline