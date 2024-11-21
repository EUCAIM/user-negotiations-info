
# Setup

Once you cloned your repository and entered the root dir, follow the next steps:

1. Create a python virtual env for your application

```python3 -m venv .env```

2. Activate the env

```source .env/bin/activate```

3. Install the requirements

```pip install -r requirements.txt```



# Execution

Once  the web server has been setup (see section **Setup**) follow the next steps to run it:

1. Create your custom configuration file (see the **Configuration** section) - here we export the env var

```export USER_NEGOTIATIONS_INFO_CONFIG=<path to config.json>```

2. Start the server

```
cd src
flask run -h <your host> -p <your port>
```


# Configuration

The web service expects a json file with all the configuration parameters.
The __config_example.json__ file (found in the __src/__ dir) contains all the fields  that can be configured for the application.
There are two ways to pass your custom configuration: either create a file named __config.json__ in the application's root dir (__src/__ in our case),or set the env variable __USER_NEGOTIATIONS_INFO_CONFIG__ with the path of your custom configuration.