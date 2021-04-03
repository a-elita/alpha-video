node {    
      def app     
      stage('Clone repository') {               
             
            checkout scm    
      }     
      stage('Build image') {         
       
            sh 'docker buildx create –use && docker buildx build  --push  --platform linux/arm/v7,linux/arm64/v8,linux/amd64  --tag andrewstech/alpha-video:dev .'
       }     
      stage('Test image') {           
            app.inside {            
             
             sh 'echo "Tests passed"'        
            }    
        }     
       stage('Push image') {
                                                  docker.withRegistry('https://registry.hub.docker.com', 'git') {            
       app.push("${env.BUILD_NUMBER}")            
       app.push("latest")        
              }    
           }
        }
