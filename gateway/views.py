from django.shortcuts import render
from rest_framework.decorators import api_view
from decouple import config
from rest_framework.status import (
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_400_BAD_REQUEST
)
from rest_framework.response import Response
import requests
import json

SERVER_COMMUNICATION_ERROR = 'Nao foi possivel se comunicar com o servidor'

@api_view(["POST"])
def register(request):
    url = "{base_user_url}{params}".format(
        base_user_url = config('USER_BASE_URL'), 
        params = "/api/user/register_market/"
    )

    # Data should have first_name, last_name, owner_phone_number, comercial_name, cnpj, cep, phone_number, agricultural_producer, email, password, password2

    return api_redirect(url, request.data)

@api_view(["POST"])
def login(request):
    url = "{base_user_url}{params}".format(
        base_user_url = config('USER_BASE_URL'), 
        params = "/api/user/login/"
    )

    # Data should have username, password

    return api_redirect(url, request.data)

@api_view(["POST"])
def check_token(request):
    url = "{base_user_url}{params}".format(
        base_user_url = config('USER_BASE_URL'), 
        params = "/api/user/"
    )

    # Data should have acces-token, refresh-token

    response = api_redirect_get(url, None, {'Authorization': 'Bearer {token}'.format(token = request.data.get("acces-token"))})

    if response.status_code != 200:
        url = "{base_user_url}{params}".format(
            base_user_url = config('USER_BASE_URL'), 
            params = "/api/user/login/refresh/"
        )

        data = {
            "refresh": request.data.get("refresh-token")
        }

        return api_redirect(url, data)
    else:
        return response

@api_view(["POST"])
def password_recovery(request):
    url = "{base_user_url}{params}".format(
        base_user_url = config('USER_BASE_URL'), 
        params = "/api/user/password_recovery/"
    )

    # Data should have email
    try:
        _session = requests.Session()

        _session.get(url)

        data = request.data
        data['csrfmiddlewaretoken'] = _session.cookies['csrftoken']

        response = _session.post(url, data=data)

        try:
            response_json = response.json()
            return Response(data=response_json, status=response.status_code)
        except Exception:
            return Response(response, status=response.status_code)

    except Exception:
        return Response(
            {'error': SERVER_COMMUNICATION_ERROR},
            status=HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(["POST"])
def password_reset(request, user, token):
    url = "{base_user_url}{params}".format(
        base_user_url = config('USER_BASE_URL'), 
        params = "/api/user/password_recovery/reset/{user}/{token}/".format(user = user, token = token)
    )

    # Data should have password, password2
    try:
        _session = requests.Session()

        _session.get(url)

        data = request.data
        data['csrfmiddlewaretoken'] = _session.cookies['csrftoken']

        url = "{base_user_url}{params}".format(
            base_user_url = config('USER_BASE_URL'), 
            params = "/api/user/password_recovery/reset/{user}/set-password/".format(user = user)
        )

        response = _session.post(url, data=data)

        status = response.status_code

        if (response.text.find('class="errorlist"') >= 0):
            status = HTTP_400_BAD_REQUEST

        try:
            response_json = response.json()
            return Response(data=response_json, status=status)
        except Exception:
            return Response(response, status=status)

    except Exception:
        return Response(
            {'error': SERVER_COMMUNICATION_ERROR},
            status=HTTP_500_INTERNAL_SERVER_ERROR
        )
    
@api_view(["GET"])
def get_producers(request, id):
    url = "{base_user_url}{params}".format(
            base_user_url = config('USER_BASE_URL'), 
            params = "/api/user/producers/"
        )
    if id:
        url = url + id + '/'

    return api_redirect_get(url, request.data)
    
@api_view(["GET"])
def get_supermarkets(request, id):
    url = "{base_user_url}{params}".format(
            base_user_url = config('USER_BASE_URL'), 
            params = "/api/user/supermarkets/"
        )
    if id:
        url = url + id + '/'

    return api_redirect_get(url, request.data)

@api_view(["GET"])
def get_producer_supermarket(request):
    url = "{base_user_url}{params}".format(
            base_user_url = config('USER_BASE_URL'), 
            params = "/api/user/get_producer_supermarket/"
        )

    return api_redirect_get(url, request.data, request.headers)

@api_view(["GET"])
def material_types(request):
    url = "{base_composter_url}{params}".format(
            base_composter_url = config('COMPOSTER_BASE_URL'), 
            params = "/api/composter/material_types/"
        )

    return api_redirect_get(url, request.data)

@api_view(["POST"])
def register_material(request):
    url = "{base_composter_url}{params}".format(
            base_composter_url = config('COMPOSTER_BASE_URL'), 
            params = "/api/composter/register_material/"
        )

    # Data should have name, imageLink, materialType

    return api_redirect(url, request.data)

@api_view(["GET"])
def materials(request):
    url = "{base_composter_url}{params}".format(
            base_composter_url = config('COMPOSTER_BASE_URL'), 
            params = "/api/composter/materials/"
        )

    return api_redirect_get(url, request.data)

@api_view(["PUT", "DELETE"])
def update_material(request, id):
    url = "{base_composter_url}{params}{id}".format(
            base_composter_url = config('COMPOSTER_BASE_URL'), 
            params = "/api/composter/update_material/",
            id = id
        )
    if request.method == "DELETE":
        return api_redirect_delete(url, request.data)

    return api_redirect_put(url, request.data)

@api_view(["POST"])
def register_composter(request):
    url = "{base_composter_url}{params}".format(
            base_composter_url = config('COMPOSTER_BASE_URL'), 
            params = "/api/composter/register_composter/"
        )

    # Data should have supermarketId, name, macAddress, description

    return api_redirect(url, request.data)

@api_view(["PUT", "DELETE"])
def update_composter(request, id):
    url = "{base_composter_url}{params}{id}".format(
            base_composter_url = config('COMPOSTER_BASE_URL'), 
            params = "/api/composter/update_composter/",
            id = id
        )
    if request.method == "DELETE":
        return api_redirect_delete(url, request.data)

    return api_redirect_put(url, request.data)

@api_view(["GET"])
def get_producer_composters(request):
    url = "{base_user_url}{params}".format(
            base_user_url = config('COMPOSTER_BASE_URL'), 
            params = "/api/composter/get_producer_composters/"
        )

    get_producer_supermarket_url = "{base_user_url}{params}".format(
            base_user_url = config('USER_BASE_URL'), 
            params = "/api/user/get_producer_supermarket/"
        )
    producer_supermarkets = api_redirect_get(get_producer_supermarket_url, None, request.headers)
    try:
        producer_supermarkets_json = json.dumps(producer_supermarkets.data)
    except Exception:
        return Response(
            {'error': SERVER_COMMUNICATION_ERROR},
            status=HTTP_500_INTERNAL_SERVER_ERROR
        )
    return api_redirect(url, {'markets': producer_supermarkets_json})


def api_redirect(url, data, header = None):
    try:
        if header:
            response = requests.get(url, headers=header)
        else:
            response = requests.post(url, data=data)
        try:
            response_json = response.json()
            return Response(data=response_json, status=response.status_code)
        except Exception:
            return Response(response, status=response.status_code)
    except Exception:
        return Response(
            {'error': SERVER_COMMUNICATION_ERROR},
            status=HTTP_500_INTERNAL_SERVER_ERROR
        )

def api_redirect_get(url, data, header = None):
    try:
        if header:
            response = requests.get(url, headers=header)
        else:
            response = requests.get(url)
        try:
            response_json = response.json()
            return Response(data=response_json, status=response.status_code)
        except Exception:
            return Response(response, status=response.status_code)
    except Exception:
        return Response(
            {'error': SERVER_COMMUNICATION_ERROR},
            status=HTTP_500_INTERNAL_SERVER_ERROR
        )

def api_redirect_delete(url, data, header = None):
    try:
        response = requests.delete(url, data=data)
        try:
            response_json = response.json()
            return Response(data=response_json, status=response.status_code)
        except Exception:
            return Response(response, status=response.status_code)
    except Exception:
        return Response(
            {'error': SERVER_COMMUNICATION_ERROR},
            status=HTTP_500_INTERNAL_SERVER_ERROR
        )

def api_redirect_put(url, data, header = None):
    try:
        response = requests.put(url, data=data)
        try:
            response_json = response.json()
            return Response(data=response_json, status=response.status_code)
        except Exception:
            return Response(response, status=response.status_code)
    except Exception:
        return Response(
            {'error': SERVER_COMMUNICATION_ERROR},
            status=HTTP_500_INTERNAL_SERVER_ERROR
        )