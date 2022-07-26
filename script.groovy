job("my-job1") {
  description("This job will pull the github repo on every push, update the container using given Dockerfile and push image to DockerHub")
 
  scm {
    github('mac912/StackOverFlow_Backend','main')
  }
 
  triggers {
    githubPush()
  }
 
  command = """
    echo "pull the code from github"
            """
 
  steps {
    shell(command)
    }
}


job("my-job2") {
  description("This will run on slave nodes and control K8S.")
  triggers {
    upstream('my-job1', 'SUCCESS')
  }
 
  command = """
  docker build -t django_os_five /home/manish/Desktop/mydockerfile
  docker-compose up
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
    shell(''' echo "job3" ''')
  }
  publishers {
    extendedEmail {
      contentType('text/html')
      triggers {
        success{
          attachBuildLog(true)
          subject('Build successfull')
          content('The build was successful and deployment was done.')
          recipientList('manishdwarkas912@gmail.com')
        }
        failure{
          attachBuildLog(true)
          subject('Failed build')
          content('The build was failed')
          recipientList('heymanishsaini@gmail.com')
        }
      }
    }
  }
}







buildPipelineView('Groovy') {
  filterBuildQueue(true)
  filterExecutors(true)
  title('Groovy')
  displayedBuilds(1)
  selectedJob('my-job1')
  alwaysAllowManualTrigger(false)
  showPipelineParameters(true)
  refreshFrequency(1)
}