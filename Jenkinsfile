pipeline {
  agent {
    kubernetes {
      label 'temp-sc-ds-live-airflow-sync'
      yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: dind
    image: sc-mum-armory.platform.internal/devops/dind:v2
    securityContext:
      privileged: true
    env:
    - name: DOCKER_TLS_CERTDIR
      value: ''
    readinessProbe:
      tcpSocket:
        port: 2375
      initialDelaySeconds: 30
      periodSeconds: 10
    livenessProbe:
      tcpSocket:
        port: 2375
      initialDelaySeconds: 30
      periodSeconds: 20
    volumeMounts:
      - name: dind-storage
        mountPath: /var/lib/docker
  - name: builder
    image: sc-mum-armory.platform.internal/devops/builder-image-armory
    command:
    - sleep
    - infinity
    env:
    - name: DOCKER_HOST
      value: tcp://localhost:2375
    - name: DOCKER_BUILDKIT
      value: "0"
    volumeMounts:
      - name: jenkins-sa
        mountPath: /root/.gcp/
  volumes:
    - name: dind-storage
      emptyDir: {}
    - name: jenkins-sa
      secret:
        secretName: jenkins-sa
"""
    }
  }

  stages {
    stage('Sync') {
      when { branch 'main' }
      steps {
        container('builder') {
          sh 'gcloud auth activate-service-account --key-file=/root/.gcp/jenkins-sa.json'
          sh 'bash ./deploy.sh'
        }
      }
    }
  }
}