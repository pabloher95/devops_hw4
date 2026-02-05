pipeline {
    agent none
    triggers {
        githubPush()
    }
    environment {
        VERSION = "1.0.${BUILD_NUMBER}"
        DB_HOST = credentials('DB_HOST')
        DB_PORT = credentials('DB_PORT')
        MYSQL_USER = credentials('MYSQL_USER')
        MYSQL_PASSWORD = credentials('MYSQL_PASSWORD')
        MYSQL_DATABASE = credentials('MYSQL_DATABASE')
        MYSQL_ROOT_PASSWORD = credentials('MYSQL_ROOT_PASSWORD')
    }

    stages {
        stage('Analyze'){
            when { expression { env.GIT_BRANCH == 'origin/main' } } 
            agent {label 'deployment'}
            steps {
                checkout scm

                sh """
                    pip install -r requirements.txt
                    pytest test_app.py --cov=. --cov-fail-under=80 --cov-report=xml:coverage.xml || true
                """


                withSonarQubeEnv('SonarQube') {
                    sh """
                        sonar-scanner \
                        -Dsonar.projectKey=devops-hw4 \
                        -Dsonar.sources=. \
                        -Dsonar.python.coverage.reportPaths=coverage.xml
                    """
                }
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Stage'){
            when { expression { env.GIT_BRANCH == 'origin/main' } }
            agent {label 'deployment'}
            steps {
                checkout scm
                sh """                
                    export DB_HOST=${DB_HOST}
                    export DB_PORT=${DB_PORT}
                    export MYSQL_USER=${MYSQL_USER}
                    export MYSQL_PASSWORD=${MYSQL_PASSWORD}
                    export MYSQL_DATABASE=${MYSQL_DATABASE}
                    export MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}

                    docker-compose up -d db
                    sleep 10

                    docker-compose exec -T db mysql -uroot -p${MYSQL_ROOT_PASSWORD} < staging_schema.sql
                    docker-compose exec -T db mysql -uroot -p${MYSQL_ROOT_PASSWORD} < staging_seed.sql
                    docker-compose exec -T db mysql -uroot -p${MYSQL_ROOT_PASSWORD} -e "USE staging_db; SELECT * FROM to_do;"

                """
                echo "Staging complete"
            }
            post {
                always {
                    sh 'docker-compose down || true'
                }
            }
        }

        stage('Test'){ 
            // when { expression { env.GIT_BRANCH != 'origin/main' } }
            agent {label 'testing'}
            steps {
                checkout scm
                echo "Checked out repo from ${env.GIT_BRANCH} on ${NODE_NAME}"

                sh """
                    export DB_HOST=${DB_HOST}
                    export DB_PORT=${DB_PORT}
                    export MYSQL_USER=${MYSQL_USER}
                    export MYSQL_PASSWORD=${MYSQL_PASSWORD}
                    export MYSQL_DATABASE=${MYSQL_DATABASE}
                    export MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}
                    export BASE_URL=http://localhost:8000

                    docker-compose up -d db web
                    sleep 15

                    docker-compose exec -T web pytest test_e2e.py --headed
                
                """ 

                echo "Running tests on ${NODE_NAME} for branch ${env.GIT_BRANCH}"
            }
            post {
                always {
                    sh 'docker-compose down || true'
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
                    echo "Build Number: ${BUILD_NUMBER}" >> build-info.txt
                    echo "Build Date: \$(date)" >> build-info.txt
                    echo "Dependencies:" >> build-info.txt
                    cat requirements.txt >> build-info.txt 
                """

                archiveArtifacts artifacts: 'build-info.txt', fingerprint: true

                echo "Deployed from ${env.GIT_BRANCH} on ${NODE_NAME}"
            }
        }
    }
}