job("CD-job1") {
  description("Pulling docker image from ECR and running on deployment server")
  command = """ 
  docker pull 176660025607.dkr.ecr.us-west-2.amazonaws.com/django_repository:$Docker_Image
  docker run -d -p 5000:8000  176660025607.dkr.ecr.us-west-2.amazonaws.com/django_repository:$Docker_Image
            """
 
  steps {
    shell(command)
    }
}

job("CD-job2") {
  description ("It will test if pod is running else send a mail")
 
  triggers {
    upstream('CD-job1', 'SUCCESS')
  }
  steps {
    shell('''
    echo "Send Email"
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
