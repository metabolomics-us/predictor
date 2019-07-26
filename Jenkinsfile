pipeline {
  agent {
    docker {
      image 'eros.fiehnlab.ucdavis.edu/jenkins-agent:latest'
    }

  }
  stages {
    stage('setup') {
      steps {
        sh '''virtualenv .venv
source .venv/bin/activate
cd predictor
pip3 install -r requirements.txt'''
      }
    }
    stage('test') {
      steps {
        sh '''source .venv/bin/activate
cd predictor
pytest ./'''
      }
    }
    stage('image') {
      steps {
        sh 'docker build -t eros.fiehnlab.ucdavis.edu/predictor:latest predictor'
      }
    }
    stage('integration test') {
      steps {
        waitUntil()
      }
    }
  }
}