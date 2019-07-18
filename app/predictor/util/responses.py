from flask import Response, json


class JsonResponse(Response):
    def __init__(self, json_dict, status=200):
        super().__init__(response=json.dumps(json_dict), status=status, mimetype="application/json")
