def chooseNode() {
    if(env.ENV == "PROD") {
        env.node = "main"
    } else {
        env.node = "vm3"
    }
}

chooseNode()

pipeline {
    agent {
        label "${node}"
    }

    parameters {
        string(name: 'ENV', defaultValue: 'TEST', description: 'Commit hash or branch to build on')
        string(name: 'DOCKER_TAG', description: 'Commit hash or branch to build on')
        string(name: 'BRANCH', description: 'Branch from which k8s and ci will be applied')
        string(name: 'DOCKER_REGISTRY', defaultValue: '192.168.56.105:5000', description: 'IP and PORT of the docker registry')
    }

    stages {
        stage('ApplyK8s') {
            steps {
                git 'https://github.com/saveli-khulup-epam/test'
                sh 'git checkout $BRANCH'
                sh 'microk8s.kubectl apply -f k8s'
            }
        }
        stage('SetImage') {
            steps {
                sh 'microk8s.kubectl set image deployments/cache-deployment cache-pod=$DOCKER_REGISTRY/cache_number:$DOCKER_TAG'
                sh 'microk8s.kubectl set image deployments/sum-deployment sum-pod=$DOCKER_REGISTRY/sum_number:$DOCKER_TAG'
                sh 'microk8s.kubectl set image deployments/rand-deployment random-pod=$DOCKER_REGISTRY/random_number:$DOCKER_TAG'
            }
        }
        stage('WaitRollout') {
            steps {
                sh 'microk8s.kubectl rollout status deploy/cache-deployment'
                sh 'microk8s.kubectl rollout status deploy/sum-deployment'
                sh 'microk8s.kubectl rollout status deploy/rand-deployment'
            }
        }
        stage('UpdateTags') {
            steps {
                sh "curl 'http://$DOCKER_REGISTRY/v2/cache_number/manifests/$DOCKER_TAG' -H 'accept: application/vnd.docker.distribution.manifest.v2+json' > manifest.json"
                sh "curl -XPUT 'http://192.168.56.105:5000/v2/cache_number/manifests/prod' -H 'content-type: application/vnd.docker.distribution.manifest.v2+json' -d '@manifest.json'"

                sh "curl 'http://$DOCKER_REGISTRY/v2/random_number/manifests/$DOCKER_TAG' -H 'accept: application/vnd.docker.distribution.manifest.v2+json' > manifest.json"
                sh "curl -XPUT 'http://192.168.56.105:5000/v2/random_number/manifests/prod' -H 'content-type: application/vnd.docker.distribution.manifest.v2+json' -d '@manifest.json'"

                sh "curl 'http://$DOCKER_REGISTRY/v2/sum_number/manifests/$DOCKER_TAG' -H 'accept: application/vnd.docker.distribution.manifest.v2+json' > manifest.json"
                sh "curl -XPUT 'http://192.168.56.105:5000/v2/sum_number/manifests/prod' -H 'content-type: application/vnd.docker.distribution.manifest.v2+json' -d '@manifest.json'"

            }

        }
    }
    post {
        always {cleanWs()}
    }
}
