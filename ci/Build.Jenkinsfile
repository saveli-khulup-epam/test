def isStartedByUser = currentBuild.rawBuild.getCause(hudson.model.Cause$UserIdCause) != null

pipeline {
    agent any

    parameters {
        string(name: 'BRANCH', description: 'Branch to build')
        string(name: 'IMAGE_NAME', description: 'Name of docker image to push')
        string(name: 'SERVICE_FOLDER', description: 'Folder of a service to build')
        string(name: 'DOCKER_REGISTRY', defaultValue: '192.168.56.105:5000', description: 'IP and PORT of the docker registry')
    }

    stages {
        stage('PullCheckout') {
            steps {
                git 'https://github.com/saveli-khulup-epam/test'
                sh 'git checkout $BRANCH'
                script {
                    GIT_COMMIT_HASH = sh (script: "git log -n 1 --pretty=format:'%H'", returnStdout: true)
                    env.DOCKER_TAG = GIT_COMMIT_HASH.take(5)
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
                sh "docker build $SERVICE_FOLDER -t $DOCKER_REGISTRY/$IMAGE_NAME:$DOCKER_TAG"
            }
        }

        stage('Upload') {
            steps {
                sh "docker push $DOCKER_REGISTRY/$IMAGE_NAME:$DOCKER_TAG"
            }
        }
    }
    post {
        always {
            cleanWs()
        }
        success {
            script {
                if (isStartedByUser){
                    def job_name = java.net.URLEncoder.encode(env.JOB_NAME, "UTF-8")
                    def build_number = env.BUILD_NUMBER
                    httpRequest "http://192.168.56.105:8000/send_notifications?job_id=${build_number}&job_name=${job_name}&status=SUCCESS"
                }
            }
        }
        failure {
            script {
                if (isStartedByUser){
                    def job_name = java.net.URLEncoder.encode(env.JOB_NAME, "UTF-8")
                    def build_number = env.BUILD_NUMBER
                    httpRequest "http://192.168.56.105:8000/send_notifications?job_id=${build_number}&job_name=${job_name}&status=FAILURE"
                }
            }
        }
    }
}
