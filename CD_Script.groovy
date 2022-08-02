job("CD-job1") {
  description("This job will login to ecr and tag the image and push the image to ECR")
  command = """
            aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 176660025607.dkr.ecr.us-west-2.amazonaws.com
            docker push 176660025607.dkr.ecr.us-west-2.amazonaws.com/django_repository:latest
            """
 
  steps {
    shell(command)
    }
}


job("CD-job2") {
  description("This job will pull the image and deploy it")
  triggers {
    upstream('CD-job1', 'SUCCESS')
  }
 
  command = """
  docker pull 176660025607.dkr.ecr.us-west-2.amazonaws.com/django_repository:latest
  docker run -d -p 5000:8000  176660025607.dkr.ecr.us-west-2.amazonaws.com/django_repository:latest
"""
 
  steps {
    shell(command)
  }
 
}

job("CD-job3") {
  description ("It will test if pod is running else send a mail")
 
  triggers {
    upstream('CD-job2', 'SUCCESS')
  }
  steps {
    shell('''
    echo "job3"
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







buildPipelineView('CD_Groovy') {
  filterBuildQueue(true)
  filterExecutors(false)
  title('CD_Groovy')
  displayedBuilds(3)
  selectedJob('CD-job1')
  alwaysAllowManualTrigger(false)
  showPipelineParameters(true)
  refreshFrequency(1)
}
