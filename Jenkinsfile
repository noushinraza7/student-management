pipeline{
    agent any
    environment{
        image_name = 'nousheenr/new-project'
        container_name = 'student-container'
    }
    stages{
        stage("checkout"){
            steps{
                git branch: 'main',
                    url: 'https://github.com/noushinraza7/student-management.git'
            }
        }
        
        stage("build"){
            steps{
                sh'''
                    docker build -t ${image_name}:${BUILD_NUMBER} .
                '''
            }
        }

        stage("test"){
            steps{
                sh'docker image inspect ${image_name}:${BUILD_NUMBER}'
            }
        }
    
        stage("push"){
            steps{
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub',
                    usernameVariable: 'DOCKERHUB_USER',
                    passwordVariable: 'DOCKERHUB_PASSWORD'
                )])
                   { 
                    sh'''
                        echo "$DOCKERHUB_PASSWORD" | docker login \
                        -u "$DOCKERHUB_USER" --password-stdin

                        docker push ${image_name}:${BUILD_NUMBER}
                        
                        docker logout
                    '''
                }
            }
        }

        stage("deploy"){
            steps{
                        
                sh '''
                    docker compose pull
                    docker compose up -d
                    docker ps
                '''
            }
        }
            

        stage("verify"){
            steps{
                sh'curl -f http://localhost:8085'
            }
        }
    }
}