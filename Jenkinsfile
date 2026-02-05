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

        stage('Build'){
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

                echo "Build ${VERSION} complete"
            }
        }

        stage('Code Quality Analysis'){
            when { expression { env.GIT_BRANCH == 'origin/main' } } 
            agent {label 'deployment'}
            steps {
                checkout scm
                withSonarQubeEnv('SonarQube') {
                    sh """
                        sonar-scanner \
                        -Dsonar.projectKey=devops-hw4 \
                        -Dsonar.sources=. \
                        -Dsonar.python.coverage.reportPaths=sq_report.xml
                    """
                }
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'sq_report.xml', allowEmptyArchive: true
                }
            }
        }

        stage('Staging'){
            when { expression { env.GIT_BRANCH == 'origin/main' } }
            agent {label 'deployment'}
            steps {
                checkout scm
                withCredentials([
                    string(credentialsId: 'DB_HOST', variable: 'DB_HOST'),
                    string(credentialsId: 'DB_PORT', variable: 'DB_PORT'),
                    string(credentialsId: 'MYSQL_USER', variable: 'MYSQL_USER'),
                    string(credentialsId: 'MYSQL_PASSWORD', variable: 'MYSQL_PASSWORD'),
                    string(credentialsId: 'MYSQL_ROOT_PASSWORD', variable: 'MYSQL_ROOT_PASSWORD')
                ]) {
                sh """                
                    docker-compose up -d db
                    sleep 10

                    echo "Creating Staging"
                    docker-compose exec -T db mysql -uroot -p${MYSQL_ROOT_PASSWORD} < staging_schema.sql

                    echo "Seeding Staging"
                    docker-compose exec -T db mysql -uroot -p${MYSQL_ROOT_PASSWORD} < staging_seed.sql
                    
                    echo "Verifying Staging:"
                    docker-compose exec -T db mysql -uroot -p${MYSQL_ROOT_PASSWORD} -e "SHOW DATABASES; USE staging_db; DESCRIBE to_do; SELECT COUNT(*) as total_tasks FROM to_do;"

                """}
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

                withCredentials([
                    string(credentialsId: 'DB_HOST', variable: 'DB_HOST'),
                    string(credentialsId: 'DB_PORT', variable: 'DB_PORT'),
                    string(credentialsId: 'MYSQL_USER', variable: 'MYSQL_USER'),
                    string(credentialsId: 'MYSQL_PASSWORD', variable: 'MYSQL_PASSWORD'),
                    string(credentialsId: 'MYSQL_ROOT_PASSWORD', variable: 'MYSQL_ROOT_PASSWORD')
                ]){
                    sh """
                    docker-compose down -v
                    docker-compose build web
                    docker-compose up -d db web
                    sleep 15
                    docker-compose exec -T web pytest test_e2e.py --junitxml=test-results/e2e.xml -v || true
                    docker-compose logs web --tail 200 || true   # add this right after pytest


                    echo "=== WEB LOGS ==="
                    docker-compose logs web | tail -200
                
                """} 

                echo "Running E2E tests on ${NODE_NAME} for branch ${env.GIT_BRANCH}"
            }
            post {
                always {
                    sh 'docker-compose down || true'
                    archiveArtifacts artifacts: 'e2e.xml', allowEmptyArchive: true
                }
            }
        }


       stage('K6 Load') {
  when { expression { env.GIT_BRANCH == 'origin/main' } }
  agent { label 'deployment' }
  steps {
    sh """
      set -euxo pipefail

      # bring up the stack
      docker-compose up -d db web
      # wait a bit for web to be ready
      sleep 10
      docker-compose exec -T web curl -sf http://localhost:8000/ || exit 1

      # find the compose network name (often devops-hw4_default)
      NET=$(docker network ls --format '{{.Name}}' | grep devops-hw4 | head -1)

      # run k6 from the official image, mounting the workspace
      docker run --rm \
        --network="$NET" \
        -v "$PWD":/scripts \
        -w /scripts \
        grafana/k6 run loadtest.js
    """
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
                echo "Project is ready to deploy!"
            }
        }
    }
}