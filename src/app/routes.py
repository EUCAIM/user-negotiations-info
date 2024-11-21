from flask import request, current_app
from werkzeug.utils import secure_filename
import requests
from requests  import Response
import traceback
import copy
import json
from dataclasses import  asdict

from app.services_extra import oidc_user_info
from app.models import ErrorResponse, Negotiation, Resource
from flask import Blueprint

mainbp = Blueprint('mainbp', __name__, template_folder='templates', 
                        url_prefix='/api/v1')

NEGOTIATION_TYPES = ["CONCLUDED", "IN_PROGRESS"]
DEFAULT_PAGE_SIZE = 30


@mainbp.route('/negotiations')
def getNegotiations():
    try:
        type = request.args.get('type')
        if type not in NEGOTIATION_TYPES:
            return json.dumps(asdict(ErrorResponse("Bad request", 400, "Missing 'type' query parameter. It can be one of the following values: " + ", ".join(NEGOTIATION_TYPES)))),  400
        page = request.args.get('page')
        if page == None:
            page = 0
        size = request.args.get('size')
        if size == None:
            size = DEFAULT_PAGE_SIZE

        authH = request.headers.get("authorization")
        if authH == None:
            return json.dumps(asdict(ErrorResponse("Unauthorized", 401, "Missing 'authorization' header"))), 401
        content, status = oidc_user_info(authH)
        if status > 299 or status < 200:
            return content, status
        ui = json.loads(content)
        headers = {
            "authorization": authH,
            "accept": "application/json, text/plain, */*"
        }
        negotiations_res: Response = requests.get(current_app.config["CUSTOM"]["negotiator_url"] + "/api/v3/users/{}/negotiations?status={}&sortOrder=DESC&page={}&size={}".format(ui["id"], type, page, size), headers = headers)
        if negotiations_res.status_code > 299 and negotiations_res.status_code < 200:
            return negotiations_res.content, negotiations_res.status_code
        # else:
        #     return negotiations.content, 200
        js: dict = negotiations_res.json()
        page: dict = copy.deepcopy(js["page"])
        page["data"] = []
        if not page["totalElements"] == 0:
            negotiations: list = js["_embedded"]["negotiations"]
            for n in negotiations: 
                nobj = Negotiation(n["id"], n["creationDate"], n["modifiedDate"])
                resources_res: Response = requests.get(current_app.config["CUSTOM"]["negotiator_url"] + "/api/v3/negotiations/{}/resources".format(n["id"]), headers = headers)
                if resources_res.status_code > 299 and resources_res.status_code < 200:
                    return "Error  obtaining the resources for negotiation {}: {}".format(n["id"], resources_res.raw.data), resources_res.status_code
                js: dict = resources_res.json()
                resources = js["_embedded"]["resources"]
                print(resources)
                if type == "CONCLUDED":
                    resources = list(filter(lambda r: r["currentState"] == "RESOURCE_MADE_AVAILABLE", resources) )
                tmp  = list(map(lambda r: Resource(r["id"], r["name"], r["sourceId"]), resources))
                nobj.set_resources(tmp)
                page["data"].append(asdict(nobj))    
                #print(js)

        return page, 200
    except Exception as ex:
        print(traceback.format_exc())
        return json.dumps(asdict(ErrorResponse("Error", 500, str(ex)))), 500
    
