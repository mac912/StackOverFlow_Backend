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
    project_folder=\$(cat /var/lib/jenkins/workspace/my-job1/proname)
    docker build --build-arg project_folder=$project_folder -t django_os_server /var/lib/jenkins/workspace/my-job1 --no-cache
    docker-compose up &
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
          recipientList('heymanishsaini@gmail.com')
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
