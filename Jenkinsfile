pipeline {
    agent none
    triggers {
        githubPush()
    }

    stages {
        stage('Test'){ 
            when { expression { env.GIT_BRANCH != 'origin/main' } }
            agent {label 'testing'}
            steps {
                checkout scm
                echo "Checked out repo on ${NODE_NAME}"
                echo "Running tests on ${NODE_NAME} for branch ${env.GIT_BRANCH}"
            }
        }

        stage('Deploy'){
            when { expression { env.GIT_BRANCH == 'origin/main' } }
            agent {label 'deployment'}
            steps {
                checkout scm
                echo "Checked out repo from ${env.GIT_BRANCH} on ${NODE_NAME}"
                echo "Deployed from ${env.GIT_BRANCH} on ${NODE_NAME}"
            }
        }
    }
}