# LetsHang #

## How to setup your backend development environment ##

This is a description for setting up a development for the LetsHang backend. It assumes that
we will be using Python 3.6, a Python virtual environment, Google App Engine, and Falcon. Google App Engine
will be the web server for hosting our REST API. I have picked Google App Engine because it is
a reasonable platform for hosting a scalable "serverless" backend. We're also using Google Maps and FireBase
so there may be advantages is staying with the Google platform. In any case, it will be fairly simple
to switch to another platform and web server if necessary.

Falcon is the solution I chose for the RESTful API. I picked Falcon because it is fairly simply to
develop with and is a light-weight "bare metal" solution. Basically, it's sole function is providing
a REST API, so there are no other components or complexities to deal with.

The initial setup can be a bit daunting. So I am walking through it step by step in this README. This process
following Google's guidelines for Setting Up a Python Development Environment as described here: <https://cloud.google.com/python/setup,>

### Step 1. Install Python ###

It is recommended that the latest versions of both Python 2.7 and Python 3.x are installed. For simplicity,
install these in common locations, either ...

```.bat
c:\python27
c:\python36
```

or

```.bat
c:\Program Files\python27
c:\Program Files\python36
```

You don't have to do this, but I started by removing my existing instances of Python. Python has a precular ability to
proliferate on computers. I had six of them not include Anaconda. For LetsHang, I wanted to start with a clean system.

### Step 2. Install the Google SDK ###

Go to <https://cloud.google.com/sdk/docs/> and click the link to download the Cloud SDK. You will find the link under "Install the latest Cloud Tools version ...". Click the appropriate OS tab, and the link will be in the instructions. Run the install by following the instructions provided.

### Step 3. Clone the backend repository ###

Clone the repository LetsHang-Backend into a folder on your computer. I'll assume you know how to clone the repo. You should use either the Master branch or a development branch if one exists.

### Step 4. Create a Virtual Environment ###

virtualenv ("virtual environment") is a tool that creates isolated Python environments. These isolated environments can have their own separate versions of Python packages, which allows you to isolate your projects dependencies from the dependencies of other projects. We recommend that you always use a per- project virtualenv when developing locally with Python.

You will need to install virtualenv globally before you can use it. It doesn't matter if you install it with Python 2 or Python 3 by running this from an OS command line.

```.bat
pip install --upgrade virtualenv
```

When you create your virtual environment, be sure to issue the command from the root directory of this project. That would
be the folder that this README.md file resides in. Use the following OS command to create the virtual environment.

```.bat
virtualenv --python "c:\python36\python.exe" venv
```

Notice that the full path to the python executable is specified on this command. Also note that the virtual environment is named "venv". The command will create a folder named "venv" and place it in the current directory. I have added /venv to our .gitignore file, so if you decide to use another name for the virtual environment, just know that you will be adding python to our Git repository (generally not a good thing).

There are two commands in this repository for turning the virtual environment on and off. These are activate.cmd and deactivate.cmd. These command only work if you named your virtual environment "venv".

Run the activate command to start your Python virtual environment.

## Step 5. Installing Dependencies ##

Be sure your virtual environment is running when you install dependencies. These steps basically follow the Google tutorial document for Falcon ... <https://cloud.google.com/community/tutorials/appengine-python-falcon.>

We are using Google to manage Falcon and its' dependencies. This is done through the requirements.txt file. Requirements.txt contains a single line referencing the version of Falcon that we are installing with our application.

Run the following commands (with the virtual environment activated) to install dependencies:

```.bat
pip install --upgrade pylint
pip install --upgrade google-cloud-storage
pip install -t lib -r requirements.txt
```

Note that the last command is putting Falcon dependencies in a folder outside the virtual environment. This is so the Google App Engine can find the Falcon code.

## Step 6. Run the API ##

Start the API with the following command ...

```.bat
dev_appserver.py .
```

Be aware that you must install the Google SDK (step 2 above) for this to work. Be sure that .py files are associated with Python.