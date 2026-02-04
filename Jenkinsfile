pipeline {
    agent none
    triggers {
        githubPush()
    }

    stages {
        stage('Verify agent setup') {
            agent {label 'deployment || testing'}
            steps {
                echo "running on branch ${env.GIT_BRANCH}" // test
                echo "running on node ${NODE_NAME}"
            }
        }

        stage('Checkout') {
            agent {label 'deployment'}
            steps {
                checkout scm
                echo "Checked out on ${NODE_NAME}"
            }
        }

        stage('Test'){ 
            when { not {expression { env.GIT_BRANCH == 'origin/main' } }}
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