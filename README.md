
# Setup

Once you cloned your repository and entered the root dir, follow the next steps:

1. Create a python virtual env for your application

```python3 -m venv .env```

2. Activate the env

```source .env/bin/activate```

3. Install the requirements

```
    pip install toml-to-requirements
    toml-to-req --toml-file src/pyproject.toml --output requirements.txt
    pip install -r requirements.txt
```



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
There are two ways to pass your custom configuration: either create a file named __config.json__ in the application's root dir (__src/__ in our case), or set the env variable __USER_NEGOTIATIONS_INFO_CONFIG__ with the path of your custom configuration.

# API

The OpenAPI 3.1 specification for this web service can be found in **openapi.yml**.
If you prefer, you can visualize it with Swagger, locally, like this:

```
docker run -p 8080:8080 -e SWAGGER_JSON=/api/swagger.yml -v openapi.yml:/api/swagger.yml swaggerapi/swagger-ui
 ```

and then open localhost:8080 in a browser to see the live rendering of the YAML file.

If you want to call the service:

```
  export T=<your token>
  export URL=<server>:<port>/<root_path>
  export TYPE=IN_PROGRESS or AVAILABLE
  curl -v -H "Authorization: Bearer $T" "$URL/api/v1/datasets?type=${TYPE}"

```