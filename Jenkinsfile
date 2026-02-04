pipeline {
    agent none
    triggers {
        githubPush()
    }

    stages {
        stage('Checkout') {
            agent any 
            steps {
                checkout scm
            }
        }

        stage('Test'){ 
            when {not {branch 'main'}}
            agent {label 'test'}
            steps {
                echo 'Running tests'
            }
        }

        stage('Deploy'){
            when {branch 'main'}
            agent {label 'deployment'}
            steps {
                echo 'Deployed from main'
            }
        }
    }
}