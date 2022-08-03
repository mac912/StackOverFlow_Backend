job("my-job1") {
  description("This job will pull the github repo on every push")
 
  scm {
    github('mac912/StackOverFlow_Backend','main')
  }
 
  triggers {
    githubPush()
  }
 
  command = """
    echo "pull the code from github"
    export GIT_COMMIT=\$(git log  -1 --format=%h)
            """
 
  steps {
    shell(command)
    }
}


job("my-job2") {
  description("This will build the job and run a docker-compose infrastructure.")
  triggers {
    upstream('my-job1', 'SUCCESS')
  }
 
  command = """
    docker build --build-arg proname=\$(cat /var/lib/jenkins/workspace/my-job1/proname) -t django_os_server /var/lib/jenkins/workspace/my-job1 --no-cache
    echo "docker compose up"
    docker-compose up -d
    echo "compose up success"
    sleep 5
"""
 
  steps {
    shell(command)
  }
 
}

job("my-job3") {
  description ("It will test if pod is running else send a mail")
 
  triggers {
    upstream('my-job2', 'SUCCESS')
  }
  steps {
    shell('''
    echo "job3"
    sleep 10
    docker exec my-job2_djos_1 python3 manage.py makemigrations
    docker exec my-job2_djos_1 python3 manage.py migrate
    docker exec my-job2_djos_1 python3 manage.py test
    docker tag django_os_server:latest django_os_server:$GIT_COMMIT
    aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 176660025607.dkr.ecr.us-west-2.amazonaws.com
    ''')
  }
  publishers {
    extendedEmail {
      contentType('text/html')
      triggers {
        success{
          attachBuildLog(true)
          subject('Build successfull')
          content('The build was successful and deployment was done.')
          recipientList('products.notifications@ganitinc.com')
        }
        failure{
          attachBuildLog(true)
          subject('Failed build')
          content('The build was failed')
          recipientList('products.notifications@ganitinc.com')
        }
      }
    }
  }
}







buildPipelineView('Groovy') {
  filterBuildQueue(true)
  filterExecutors(false)
  title('Groovy')
  displayedBuilds(3)
  selectedJob('my-job1')
  alwaysAllowManualTrigger(false)
  showPipelineParameters(true)
  refreshFrequency(1)
}
