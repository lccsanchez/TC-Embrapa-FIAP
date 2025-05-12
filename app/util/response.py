import json
from flask import Response


def build_response(data):
    return Response(json.dumps(data, default=lambda k: k.__dict__, indent=4, ensure_ascii=False), status=200, mimetype='application/json')