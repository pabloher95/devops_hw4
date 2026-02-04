pipeline {
    agent none
    triggers {
        githubPush()
    }

    stages {
        stage('Agent initialize') {
            agent {label 'deployment || testing'}
            steps {
                echo "running pipeline from branch ${env.GIT_BRANCH} on node ${NODE_NAME}"
            }
        }

        stage('Checkout') {
            agent {label 'deployment || testing'}
            steps {
                checkout scm
                echo "Checked out repo on ${NODE_NAME}"
            }
        }

        stage('Test'){ 
            when { expression { env.GIT_BRANCH == 'origin/testing' } }
            agent {label 'testing'}
            steps {
                echo "Running tests on ${NODE_NAME}"
            }
        }

        stage('Deploy'){
            when { expression { env.GIT_BRANCH == 'origin/main' } }
            agent {label 'deployment'}
            steps {
                echo "Deployed from ${env.GIT_BRANCH} on ${NODE_NAME}"
            }
        }
    }
}