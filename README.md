# Emotion Detection Using Speech Dialogue

## About
This project is a web application which takes a speech dialogue as an input in the form of spoken audio by the user to predict an emotion using combination of keyword spotting, natural language processing (NLP) and machine learning (ML). <br />

## Setup
1) First ensure that your machine have Python >= 3.8.1 and pip >= 19.2.3.<br />
   ```
   python3 --version
   ```
   ```
   pip3 --version
   ```

2) Create a virtual environment for the project.<br />
   For conda in Anaconda:
   ```
   conda create --name <env-name>
   ```
   For venv in Python:
   ```
   python3 -m venv /path/to/new/virtual/environment
   ``` 
   Replace _\<env-name>_ with the desired name for your virtual environment and _/path/to/new/virtual/environment_ with the desired path for your virtual environment.<br /> 
   Instead of using _venv_ tool in Python to create and manage a virtual environment, any other alternative can also be used like _pipenv_, _virtualenv_, _virtualenvwrapper_, etc.<br />

3) Activate the created virtual environment.<br />
   For conda in Anaconda:
   ```
   conda activate <env-name>
   ```
   For venv in Python:
   ```
   source /path/to/new/virtual/environment/bin/activate
   ``` 

4) Install all the packages in the activated virtual environment using the _requirements.txt_ file.<br />
   ```
   pip install -r requirements.txt
   ```

5) Inside the project directory either create a file with the name _.env_ or rename the file with the name _.env.example_ to _.env_ and intialise all environment variables given in that file with appropriate values.<br />
   For example, to generate a secret key for the project run the following commands inside the activated virtual environment:
   ```
   from django.core.management.utils import get_random_secret_key
   ```
   ```
   get_random_secret_key()
   ```
   Copy the generated secret key and paste it in front of the _SECRET_KEY_ variable in _.env_ file.

6) Finally run the following command inside the project directory to run the project and then open the generated server URL in the browser to view the running project.<br />
   ```
   python manage.py runserver
   ```

**NOTE**: When not working with the project, deactivate the virtual environment.<br />
   For conda in Anaconda:<br />
   ```
   conda deactivate
   ```
   For venv in python:
   ```
   source deactivate
   ```

## Working
<img src="images/home-page.png" width="1000" alt="Image of home page" /><br />
<img src="images/recordings-page.png" width="1000" alt="Image of recordings page" /><br />