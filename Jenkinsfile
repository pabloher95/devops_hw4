pipeline {
    agent none
    triggers {
        githubPush()
    }
    environment {
        VERSION = "1.0.${BUILD_NUMBER}"
    }

    stages {
        stage('Test'){ 
            when { expression { env.GIT_BRANCH != 'origin/main' } }
            agent {label 'testing'}
            steps {
                checkout scm
                echo "Checked out repo from ${env.GIT_BRANCH} on ${NODE_NAME}"
                echo "Running tests on ${NODE_NAME} for branch ${env.GIT_BRANCH}"
            }
        }

        stage('SonarQube Analysis'){
            when { expression { env.GIT_BRANCH == 'origin/main' } }
            agent {label 'deployment'}
            steps {
                checkout scm
                withSonarQubeEnv('SonarQube') {
                    sh """
                        sonar-scanner \
                        -Dsonar.projectKey=devops-hw4 \
                        -Dsonar.sources=.
                    """
                }
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Deploy'){
            when { expression { env.GIT_BRANCH == 'origin/main' } }
            agent {label 'deployment'}
            steps {
                checkout scm
                echo "Checked out repo from ${env.GIT_BRANCH} on ${NODE_NAME}"

                sh""" 
                    echo "Version: ${VERSION}" > build-info.txt
                    echo "Build Number:${BUILD_NUMBER}" >> build-info.txt
                    echo "Build Date: \$(date)" >> build-info.txt
                    echo "Dependencies" >> build-info.txt
                    cat requirements.txt >> build-info.txt 

                """

                archiveArtifacts artifacts: 'build-info.txt', fingerprint: false

                echo "Deployed from ${env.GIT_BRANCH} on ${NODE_NAME}"
            }
        }
    }
}