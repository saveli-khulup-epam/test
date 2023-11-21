pipeline {
    agent any

	parameters {
        string(name: 'COMMIT_HASH', description: 'Commit hash or branch to build on')
        string(name: 'DOCKER_REGISTRY', defaultValue: '192.168.56.105:5000', description: 'IP and PORT of the docker registry')
    }

    stages {
      stage('Build') {
        steps {
            git 'https://github.com/saveli-khulup-epam/test'
            sh 'git checkout $COMMIT_HASH'
            script {
                GIT_COMMIT_HASH = sh (script: "git log -n 1 --pretty=format:'%H'", returnStdout: true)
                env.GIT_COMMIT = GIT_COMMIT_HASH.take(5)
            }
      		sh 'echo $GIT_COMMIT'
      		script {
      		    build(job: 'Build',
                      parameters: [
                        string(name: 'COMMIT_HASH', value: env.GIT_COMMIT),
                        string(name: 'SERVICE_FOLDER', value: 'sum_service'),
                        string(name: 'DOCKER_REGISTRY', value: env.DOCKER_REGISTRY),
                        string(name: 'IMAGE_NAME', value: 'sum_number'),
                        ],
                        propagate: true,
                        wait: true)
                build(job: 'Build',
                      parameters: [
                        string(name: 'COMMIT_HASH', value: env.GIT_COMMIT),
                        string(name: 'SERVICE_FOLDER', value: 'cache_service'),
                        string(name: 'DOCKER_REGISTRY', value: env.DOCKER_REGISTRY),
                        string(name: 'IMAGE_NAME', value: 'cache_number'),
                        ],
                        propagate: true,
                        wait: true)
                build(job: 'Build',
                      parameters: [
                        string(name: 'COMMIT_HASH', value: env.GIT_COMMIT),
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
                  build(job: 'Deploy DEV',
                      parameters: [
                        string(name: 'COMMIT_HASH', value: env.GIT_COMMIT)
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
                        string(name: 'ENV_URL', value: 'http://192.168.56.103')
                        ],
                        propagate: true,
                        wait: true)
              }
          }
      }
      stage ('Deploy PROD') {
          steps {
              script {
                  build(job: 'Deploy PROD',
                      parameters: [
                        string(name: 'COMMIT_HASH', value: env.GIT_COMMIT),
                        string(name: 'ENV', value: 'PROD')
                        ],
                        propagate: true,
                        wait: true)
              }
          }
      }
    }
}
