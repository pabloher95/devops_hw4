pipeline {
    agent none
    triggers {
        githubPush()
    }

    stages {
        stage('Debug') {
            agent any
            steps {
                echo ${env.BRANCH_NAME}
                echo ${NODE_NAME}
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
            when {not {branch 'main'}}
            agent {label 'testing'}
            steps {
                echo "Running tests on ${NODE_NAME}"
            }
        }

        stage('Deploy'){
            when {branch 'main'}
            agent {label 'deployment'}
            steps {
                echo "Deployed from main on ${NODE_NAME}"
            }
        }
    }
}