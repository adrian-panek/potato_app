pipeline {
    agent any
    stages {
        stage('Checkout repo'){
            steps{
                git branch: 'jenkins', credentialsId: 'e7ac38b9-2a09-4d78-8608-8fc1179b55b2', url: 'https://github.com/adrian-panek/potato_app'
            }
        }
        stage('List all downloaded files'){
            steps {
                sh('ls')
            }
        }
        stage('Cleanup previous pip installation'){
            steps {
                sh('cat requirements.txt | sudo xargs pip uninstall -y')
            }
        }
        stage('Cleanup previous Docker image build'){
            steps {
                sh('docker rmi adrianpanek/python-app:latest')
            }
        }
        stage('Update dependency manager'){
            steps {
                sh('pip install --upgrade pip')
            }
        }
        stage('Install all packages'){
            steps {
                sh('pip install -r requirements.txt')
            }
        }
        stage('Run static code analysis'){
            steps {
                sh ('find -name "*.py" -not -path "./venv/*" | xargs pylint -E --load-plugins=pylint_flask | tee pylint.log')
            }
        }
        stage('Run tests'){
            steps {
                sh("python3 -m pytest")
            }
        }
        stage('Build docker image'){
            steps {
                sh('docker build . -t adrianpanek/python-app:latest')
            }
        }
    } //stages
} //pipeline