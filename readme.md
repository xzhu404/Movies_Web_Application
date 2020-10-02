# Movies Web Application

## Description

A Web application that demonstrates use of Python's Flask framework. The application makes use of libraries such as the Jinja templating library and WTForms. Architectural design patterns and principles including Repository, Dependency Inversion and Single Responsibility have been used to design the application. The application uses Flask Blueprints to maintain a separation of concerns between application functions. Testing includes unit and end-to-end testing using the pytest tool. 

## Installation

**Installation via requirements.txt**

```shell
cd Movies_Web_Application
# Take the conda virtual environment as an example
conda create -n movies_web python=3.7
conda activate movies_web
pip install -r requirements.txt
```

When using PyCharm, set the virtual environment using 'File'->'Settings' and select 'Project:Movies_Web_Application' from the left menu. Select 'Project Interpreter', click on the gearwheel button and select 'Add'. Click the 'Conda Environment' and click the 'Existing environment' radio button to select the virtual environment. 

## Execution

**Running the application**

From the *Movies_Web_Application* directory, and within the activated virtual environment (`conda activate movies_web`):

````shell
flask run
# or 
python wsgi.py runserver
````


## Configuration

The *Movies_Web_Application/.env* file contains variable settings. They are set with appropriate values.

* `FLASK_APP`: Entry point of the application (should always be `wsgi.py`).
* `FLASK_ENV`: The environment in which to run the application (either `development` or `production`).
* `SECRET_KEY`: Secret key used to encrypt session data.
* `TESTING`: Set to False for running the application. Overridden and set to True automatically when testing the application.
* `WTF_CSRF_SECRET_KEY`: Secret key used by the WTForm library.


## Testing

Testing requires that file *Movies_Web_Application/tests/conftest.py* be edited to set the value of `TEST_DATA_PATH`. You should set this to the absolute path of the *Movies_Web_Application/tests/data* directory. 

E.g. 

`TEST_DATA_PATH = os.path.join(BASE_DIR, "tests", "data")`

`BASE_DIR` is in the file *Movies_Web_Application/config.py*, and it's value is the root directory of the project *Movies_Web_Application*.

assigns `TEST_DATA_PATH` with the following value (the use of os.path.join and os.sep ensures use of the correct platform path separator):

```shell
# On Windows 10
C:\Users\ian\Documents\Movies_Web_Application\tests\data
# On macOS
/Users/ian/Documents/Movies_Web_Application/tests/data
# On Linux distribution(e.g. Ubuntu, Debian, arch ...)
/home/ian/Documents/Movies_Web_Application/tests/data
```

You can then run tests from within PyCharm.

 

