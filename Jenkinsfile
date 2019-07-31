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
pip3 install -r requirements.txt'''
      }
    }
    stage('test') {
      steps {
        sh '''source .venv/bin/activate
pytest -sss predictor'''
      }
    }
    stage('image') {
      steps {
        sh 'docker build -t eros.fiehnlab.ucdavis.edu/predictor:latest predictor'
      }
    }
  }
}