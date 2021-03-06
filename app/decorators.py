from functools import wraps
from flask import Response, request
import json


def returns_json(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        r = f(*args, **kwargs)
        return Response(r, content_type='text/json; charset=utf-8')

    return decorated_function


# GET /api/modeltype?page=[int]&offset=[int]&sortParam=[string]&sortAscending=[bool]&filter=[string]


def errorJSON(error):
    return json.dumps({"error": error})

def checkRequiredAndOptionalParameters(requiredParameters, optionalParameters):
    parameters = dict()

    for key, cast in requiredParameters:
        if key not in request.args:
            return errorJSON("Required parameter " + key + " not supplied")
        else:
            try:
                # try to use the type to type-cast
                parameters[key] = cast(request.args[key])
            except ValueError:
                # if it fails, notify the user of the API
                return errorJSON("Parameter " + key + ", with value '" + request.args.get(
                    key) + "' is of incorrect type. Expected type: " + str(cast))

    for key, cast in optionalParameters:
        if key in request.args:
            try:
                parameters[key] = cast(request.args[key])
            except ValueError:
                return errorJSON("Parameter " + key + ", with value '" + request.args.get(
                    key) + "' is of incorrect type. Expected type: " + str(cast))

    return parameters

def takes_search_params(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        requiredParameters = [("query", str)]
        optionalParameters = [("page", int)]

        parameters = checkRequiredAndOptionalParameters(requiredParameters, optionalParameters)
        if type(parameters) is dict:
            r = f(**parameters)
            return r
        else:
            # errorJSON
            return parameters

    return decorated_function


def takes_api_params(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        requiredParameters = [("page", int)]
        optionalParameters = [("sortParam", str), ("sortAscending", int), ("filterText", str)]

        parameters = checkRequiredAndOptionalParameters(requiredParameters, optionalParameters)
        if type(parameters) is dict:
            r = f(**parameters)
            return r
        else:
            # errorJSON
            return parameters

    return decorated_function
