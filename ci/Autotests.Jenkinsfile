def isStartedByUser = currentBuild.rawBuild.getCause(hudson.model.Cause$UserIdCause) != null

pipeline {
    agent any

    parameters {
        string(name: 'BRANCH', description: 'Branch to run tests from and use CI script')
        string(name: 'ENV_URL', description: 'URL of ENV to run tests on')
    }

    stages {
        stage('PullCheckout') {
            steps {
                git 'https://github.com/saveli-khulup-epam/test'
                sh 'git checkout $BRANCH'
            }
        }
        stage('Install deps') {
            steps {
                sh """#!/bin/bash
                python3 -m venv venv
                source venv/bin/activate
                pip install -r tests/requirements.txt
                """
            }
        }
        stage('Run tests') {
            steps {
                sh """#!/bin/bash
                source venv/bin/activate
                PYTHONPATH=\$(pwd)/tests pytest tests --html=report.html --self-contained-html"""
            }
            post {
                always {
                    archiveArtifacts artifacts: 'report.html'
                }
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
