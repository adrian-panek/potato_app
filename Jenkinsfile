pipeline {
    agent { 
        docker {
            image 'python'
            args '-u root:sudo -v $HOME/workspace/flask-app:/flask-app'
        } 
    }
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
                sh('pip install -r requirements.txt')
            }
        }
        stage('Run static code analysis'){
            steps {
                sh('find . -type f -name "*.py" | xargs pylint -E --load-plugins=pylint_flask | tee pylint.log')
            }
        }
        stage('Run tests'){
            steps {
                sh('pytest')
            }
        }
        stage('Build docker image'){
            steps {
                sh('docker build Dockerfile -t adrianpanek/python-app:latest')
            }
        }
    } //stages
} //pipeline