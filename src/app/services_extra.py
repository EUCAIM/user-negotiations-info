from flask import current_app
import requests
import json

from app.exceptions import BaseException


def oidc_user_info(auth_header_value: str) -> dict:
    ui = requests.get(current_app.config["CUSTOM"]["negotiator_url"] + "/api/v3/userinfo", 
                      headers={
                          "authorization": auth_header_value
                      })    
    
    return ui.content, ui.status_code

def negotiator_error_handler(service: str, raw_error: str, status: int):
    try:
        js: dict = json.loads(raw_error)
        return js
    except  Exception as ex:
        return BaseException("Error from {}".format(service), status, raw_error)
    
