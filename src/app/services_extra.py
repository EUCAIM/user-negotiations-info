from flask import current_app
import requests
import json
from requests  import Response
from app.models import Resource

from app.exceptions import BaseException, DatasetsListException


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
        return BaseException("Error from {}".format(service), status, ex)
    
def get_negotiations(auth_header_value: str, user_id: str, negotiation_types: list[str], page: int, size: int) -> tuple[dict, int]:
    headers = {
        "authorization": auth_header_value,
        "accept": "application/json, text/plain, */*"
    }
    negotiations_res: Response = requests.get(current_app.config["CUSTOM"]["negotiator_url"] 
            + "/api/v3/users/{}/negotiations?status={}&sortOrder=DESC&page={}&size={}".format(user_id, ",".join(negotiation_types), page, size), 
            headers = headers)
    #if negotiations_res.status_code > 299 and negotiations_res.status_code < 200:
    return negotiations_res.json(), negotiations_res.status_code

def get_datasets(auth_header_value: str, negotiation_id: str, dataset_type: str) -> list[Resource]:
    headers = {
        "authorization": auth_header_value,
        "accept": "application/json, text/plain, */*"
    }
    resources_res: Response = requests.get(current_app.config["CUSTOM"]["negotiator_url"] 
        + "/api/v3/negotiations/{}/resources".format(negotiation_id), headers = headers)
    if resources_res.status_code > 299 and resources_res.status_code < 200:
        raise DatasetsListException("Error obtaining the resources for negotiation {}: {}".format(negotiation_id, resources_res.raw.data),
            resources_res.status_code)
    js: dict = resources_res.json()
    resources = js["_embedded"]["resources"]
    if dataset_type == "AVAILABLE":
        resources = list(filter(lambda r: r["currentState"] == "RESOURCE_MADE_AVAILABLE", resources) )
    elif dataset_type == "IN_PROGRESS":
        resources = list(filter(lambda r: not r["currentState"] == "RESOURCE_MADE_AVAILABLE", resources) )
    else:
        raise ValueError("Unhandled datasets type '{}'".format(dataset_type))
    return list(map(lambda r: Resource(r["id"], r["name"], r["sourceId"], negotiation_id), resources))
    
