from flask import request, current_app
from werkzeug.utils import secure_filename
import requests
from requests  import Response
import traceback
import copy
import json
from dataclasses import  asdict

from app.services_extra import oidc_user_info, get_negotiations, get_datasets
from app.models import ErrorResponse, Negotiation, Resource
from flask import Blueprint
from app.exceptions import DatasetsListException

mainbp = Blueprint('mainbp', __name__, template_folder='templates', 
                        url_prefix='/api/v1')

#NEGOTIATION_TYPES = ["CONCLUDED", "IN_PROGRESS"]
DATASET_STATUS_TYPE = ["AVAILABLE", "IN_PROGRESS"]
DEFAULT_PAGE_SIZE = 30

@mainbp.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    header['Access-Control-Allow-Headers'] = '*' #'x-requested-with, Origin, Content-Type, X-Auth-Token'
    # Other headers can be added here if needed
    return response

@mainbp.route('/datasets')
def getNegotiations():
    try:
        type = request.args.get('type')
        if type not in DATASET_STATUS_TYPE:
            return json.dumps(asdict(ErrorResponse("Bad request", 400, 
                    "Missing 'type' query parameter. It can be one of the following values: " + ", ".join(DATASET_STATUS_TYPE)))),  400
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
        negotiation_types = ["IN_PROGRESS"]
        if type == "AVAILABLE":
            negotiation_types.append("CONCLUDED")
        content, code = get_negotiations(authH, ui["id"], negotiation_types, 0, 1)
        if code > 299 and code < 200:
            return content, code
        
        all_datasets = []
        totalElements = content["page"]["totalElements"]
        if totalElements >= 1:
          content, code = get_negotiations(authH, ui["id"], negotiation_types, 0, totalElements)
          if code > 299 and code < 200:
              return content, code
          negotiations: list = content["_embedded"]["negotiations"]
          for n in negotiations: 
              try:
                  datasets: list[Resource] = get_datasets(authH, n["id"], type)
                  all_datasets.extend(datasets)
              except DatasetsListException as dle:
                  print(traceback.format_exc())
                  return json.dumps(asdict(ErrorResponse("Error", dle.status, dle.message))), dle.status
        page: dict= {
            "number": 0,
            "totalItems": len(all_datasets),
            "totalPages": 1,
            "size": len(all_datasets),
            "data": all_datasets
        }
        return page, 200
        
    except Exception as ex:
        print(traceback.format_exc())
        return json.dumps(asdict(ErrorResponse("Error", 500, str(ex)))), 500

# @mainbp.route('/negotiations')
# def getNegotiations():
#     try:
#         type = request.args.get('type')
#         if type not in NEGOTIATION_TYPES:
#             return json.dumps(asdict(ErrorResponse("Bad request", 400, "Missing 'type' query parameter. It can be one of the following values: " + ", ".join(NEGOTIATION_TYPES)))),  400
#         page = request.args.get('page')
#         if page == None:
#             page = 0
#         size = request.args.get('size')
#         if size == None:
#             size = DEFAULT_PAGE_SIZE

#         authH = request.headers.get("authorization")
#         if authH == None:
#             return json.dumps(asdict(ErrorResponse("Unauthorized", 401, "Missing 'authorization' header"))), 401
#         content, status = oidc_user_info(authH)
#         if status > 299 or status < 200:
#             return content, status
#         ui = json.loads(content)
#         headers = {
#             "authorization": authH,
#             "accept": "application/json, text/plain, */*"
#         }
#         negotiations_res: Response = requests.get(current_app.config["CUSTOM"]["negotiator_url"] + "/api/v3/users/{}/negotiations?status={}&sortOrder=DESC&page={}&size={}".format(ui["id"], type, page, size), headers = headers)
#         if negotiations_res.status_code > 299 and negotiations_res.status_code < 200:
#             return negotiations_res.content, negotiations_res.status_code
#         # else:
#         #     return negotiations.content, 200
#         js: dict = negotiations_res.json()
#         page: dict = copy.deepcopy(js["page"])
#         page["data"] = []
#         if not page["totalElements"] == 0:
#             negotiations: list = js["_embedded"]["negotiations"]
#             for n in negotiations: 
#                 nobj = Negotiation(n["id"], n["creationDate"], n["modifiedDate"])
#                 resources_res: Response = requests.get(current_app.config["CUSTOM"]["negotiator_url"] + "/api/v3/negotiations/{}/resources".format(n["id"]), headers = headers)
#                 if resources_res.status_code > 299 and resources_res.status_code < 200:
#                     return "Error  obtaining the resources for negotiation {}: {}".format(n["id"], resources_res.raw.data), resources_res.status_code
#                 js: dict = resources_res.json()
#                 resources = js["_embedded"]["resources"]
#                 # print(resources)
#                 if type == "CONCLUDED":
#                     resources = list(filter(lambda r: r["currentState"] == "RESOURCE_MADE_AVAILABLE", resources) )
#                 for r in resources:
#                     orgR: Response = requests.get(
#                         current_app.config["CUSTOM"]["negotiator_url"] + 
#                             "/api/v3/organizations/{}".format(r["organization"]["id"]), 
#                         headers = headers)
#                     org: dict = orgR.json()
#                     print(org)
#                 tmp  = list(map(lambda r: Resource(r["id"], r["name"], r["sourceId"]), resources))
#                 nobj.set_resources(tmp)
#                 page["data"].append(asdict(nobj))    
#                 #print(js)

#         return page, 200
#     except Exception as ex:
#         print(traceback.format_exc())
#         return json.dumps(asdict(ErrorResponse("Error", 500, str(ex)))), 500
    
