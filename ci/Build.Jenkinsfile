pipeline {
    agent any

    parameters {
        string(name: 'COMMIT_HASH', description: 'Commit hash or branch to build on'),
        string(name: 'IMAGE_NAME', description: 'Name of docker image to push'),
        string(name: 'SERVICE_FOLDER', description: 'Folder of a service to build'),
        string(name: 'DOCKER_REGISTRY', defaultValue: '192.168.56.105:5000', description: 'IP and PORT of the docker registry')
    }

    stages {
        stage('PullCheckout') {
            steps {
                git 'https://github.com/saveli-khulup-epam/test'
                sh 'git checkout $COMMIT_HASH'
                script {
                    GIT_COMMIT_HASH = sh (script: "git log -n 1 --pretty=format:'%H'", returnStdout: true)
                    env.GIT_COMMIT = GIT_COMMIT_HASH.take(5)
                }
            }
        }
        stage('UnitTests') {
            steps {
                sh """#!/bin/bash
                python3 -m venv venv
                source venv/bin/activate
                cd $SERVICE_FOLDER
                pip install -r tests/requirements.txt
                pip install -r requirements.txt
                PYTHONPATH=\$(pwd) pytest tests --html=../unit_report.html --self-contained-html
                """
            }
            post {
                always {
                    archiveArtifacts artifacts: 'unit_report.html'
            }
        }
        }
        stage('Build') {
            steps {
                sh "docker build $SERVICE_FOLDER -t $DOCKER_REGISTRY/$IMAGE_NAME:$GIT_COMMIT"
            }
        }

        stage('Upload') {
            steps {
                sh "docker push $DOCKER_REGISTRY/$IMAGE_NAME:$GIT_COMMIT"
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}
