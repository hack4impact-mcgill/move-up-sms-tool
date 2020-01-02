# How to Run

First off, make sure to create a virtual environment on your machine. A virtual environment can be created with either `virtualenv` (python 2) or `venv` (python 3). For `venv`:

```
python3 -m venv env

source env/bin/activate
```

The second line activates the virtual environment, and you can type `deactivate` to exit the environment.

To install dependencies from a `requirements.txt` file, do this:

```
pip install -r /path/to/requirements.txt
```

You only need to install the dependencies onece. To see all installed modules:

```
pip list
```

## Running the server

To run the basic server, we'll use ngrok through Twilio's CLI.

Check that you have NodeJs:
```
node -v
```

Download Twilio's CLI.
```
npm install twilio-cli -g
```

Login. The terminal will prompt you for account details. 
```
twilio login
```

Open an ngrok tunnel (aka connect your application to the internet). You can monitor requests at the address that ngrok gives you (i.e. the link showed in the terminal).

Type the following command in ther terminal.
```
twilio phone-numbers:update "+14388003554" --sms-url="http://localhost:5000/message"
```

In a separate terminal, run the application:
```
python manage.py recreate_db  # create the databases
python manage.py dbseed  # load the signup form from json
python manage.py runserver
```

Try texting the number!


## Flask App Folder Structure

```
|-app-name/
	|-backend/
		|-tests/
		|-requirements.txt
		|-config.py # define various configurations
		|-manage.py # script for running the application
		|-app/
			|-main/
				|-__init_.py # set up Blueprint 'main' here
				|-views.py # routes for main Blueprint here
				|-errors.py # set up error routes
			|-other_blueprint/
				|-__init_.py # set up Blueprint 'other_blueprint' here
				|-views.py # routes for other_blueprint Blueprint here
				|-errors.py # set up error routes
			|-__init__.py # create_app factory function goes here
	|-frontend/
		|-...
```

To run a Blueprint-based app, run `python manage.py runserver`. To run all tests, run `python manage.py test`.
