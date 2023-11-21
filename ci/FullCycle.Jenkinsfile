pipeline {
    agent any

	parameters {
        string(name: 'BRANCH', description: 'Branch to build on')
        string(name: 'DOCKER_REGISTRY', defaultValue: '192.168.56.105:5000', description: 'IP and PORT of the docker registry'),
        string(name: 'ENV', description: 'ENV to deploy on')
    }

    stages {
      stage('Build') {
        steps {
            git 'https://github.com/saveli-khulup-epam/test'
            sh 'git checkout $BRANCH'
            script {
                GIT_COMMIT_HASH = sh (script: "git log -n 1 --pretty=format:'%H'", returnStdout: true)
                env.GIT_COMMIT = GIT_COMMIT_HASH.take(5)
            }
      		sh 'echo $GIT_COMMIT'
      		script {
      		    build(job: 'Build',
                      parameters: [
                        string(name: 'BRANCH', value: env.BRANCH),
                        string(name: 'SERVICE_FOLDER', value: 'sum_service'),
                        string(name: 'DOCKER_REGISTRY', value: env.DOCKER_REGISTRY),
                        string(name: 'IMAGE_NAME', value: 'sum_number'),
                        ],
                        propagate: true,
                        wait: true)
                build(job: 'Build',
                      parameters: [
                        string(name: 'BRANCH', value: env.BRANCH),
                        string(name: 'SERVICE_FOLDER', value: 'cache_service'),
                        string(name: 'DOCKER_REGISTRY', value: env.DOCKER_REGISTRY),
                        string(name: 'IMAGE_NAME', value: 'cache_number'),
                        ],
                        propagate: true,
                        wait: true)
                build(job: 'Build',
                      parameters: [
                        string(name: 'BRANCH', value: env.BRANCH),
                        string(name: 'SERVICE_FOLDER', value: 'random_number'),
                        string(name: 'DOCKER_REGISTRY', value: env.DOCKER_REGISTRY),
                        string(name: 'IMAGE_NAME', value: 'random_number'),
                        ],
                        propagate: true,
                        wait: true)
      		}
        }
      }
      stage ('Deploy DEV') {
          steps {
              script {
                  build(job: 'Deploy',
                      parameters: [
                        string(name: 'BRANCH', value: env.BRANCH),
                        string(name: 'DOCKER_REGISTRY', value: env.DOCKER_REGISTRY),
                        string(name: 'ENV', value: 'DEV')
                        ],
                        propagate: true,
                        wait: true)
              }
          }
      }
      stage ('E2E Tests') {
          steps {
              script {
                  build(job: 'Auto tests',
                      parameters: [
                        string(name: 'ENV_URL', value: 'http://192.168.56.103'),
                        string(name: 'BRANCH', value: env.BRANCH)
                        ],
                        propagate: true,
                        wait: true)
              }
          }
      }
      stage ('Deploy PROD') {
          when {
            expression {
                return env.ENV == 'PROD';
             }
          }
          steps {
              script {
                  build(job: 'Deploy',
                      parameters: [
                        string(name: 'DOCKER_TAG', value: env.GIT_COMMIT),
                        string(name: 'K8S_BRANCH', value: env.BRANCH),
                        string(name: 'ENV', value: 'PROD')
                        ],
                        propagate: true,
                        wait: true)
              }
          }
      }
    }
}
