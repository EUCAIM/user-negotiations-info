import os
import json    
import tomllib    

basedir = os.path.abspath(os.path.dirname(__file__))
config_env_path = os.environ.get("USER_NEGOTIATIONS_INFO_CONFIG")
print(config_env_path)

def load_custom_config():
    path: str = None
    if config_env_path is None:
        path = os.path.join(basedir, 'config.json')
    else:
        path = config_env_path;
    if os.path.exists(path):
        print("loading config from {}".format(path))
        cnf: dict = None
        with open(path, "r") as js:
            cnf =  json.load(js)
        return cnf
    else:
        raise Exception("Please create a config.json file in the app's"\
                        "root directory following the template found in 'config_example.json',"\
                        "or define an environment variable USER_NEGOTIATIONS_INFO_CONFIG with the path of the config file")

def get_app_ver():
    with open("pyproject.toml", "rb") as f:
        toml_data = tomllib.load(f)

    version = toml_data["project"]["version"]
    print(f"Flask app version: {version}")
    return version

class Config:
    # ...
    CUSTOM = load_custom_config()
    VERSION = get_app_ver()