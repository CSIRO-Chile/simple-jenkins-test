pipeline {
    agent any
    stages {
        stage('Checkout from GitHub') {
          steps {
            echo "Checking out repo"  
            git branch: 'main', url: 'https://github.com/CSIRO-Chile/simple-jenkins-test.git'
          }
        }
        stage('Configure venv') {
            steps {
                sh '''
                    cd $WORKSPACE
                    PYENV_HOME=$WORKSPACE/venv

                    # Delete previously built virtualenv
                    if [ -d $PYENV_HOME ]; then
                        rm -rf $PYENV_HOME
                    fi
                    
                    # Create virtualenv and install necessary packages
                    python -m venv $PYENV_HOME
                    . $PYENV_HOME/bin/activate
                    $PYENV_HOME/bin/pip install -r requirements.txt
                '''
            }
        }
        stage('Run Python script') {
            steps {
                sh '''
                cd $WORKSPACE
                . venv/bin/activate
                python get_latest_sst.py
                '''
            }
        }
        stage('Output artifacts'){
            steps {
                archiveArtifacts allowEmptyArchive: true, artifacts: '*.png', followSymlinks: false, onlyIfSuccessful: true
            }
        }
    }
}
