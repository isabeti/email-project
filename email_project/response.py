from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.shortcuts import redirect
from django.shortcuts import resolve_url


class Action_To_Serializer(serializers.Serializer):
    action = serializers.CharField()
    url = serializers.CharField()
    params = serializers.JSONField()


class Msg:
    def __init__(self, error=None, success=None):
        self.error = error
        self.success = success

    def Success(self, msg):
        self.success = msg
        self.error = None

    def Error(self, msg):
        self.error = msg
        self.success = None

    def Empty(self):
        self.success = None
        self.error = None


class Action:
    def __init__(self,  action: str, url: str, params={}):
        self.action = action
        self.url = url
        self.params = params

    def data(action, url, params={}):
        return Action_To_Serializer(Action(action, resolve_url(url), params)).data


    def data_dt(action, url, pk, params={}):
        return Action_To_Serializer(Action(action, resolve_url(url, pk), params)).data

    def redirect_to(url):
        return {'redirect': resolve_url(url)}
        
    def redirect_to_dt(url, pk):
        return {'redirect': resolve_url(url, pk)}


def APIResponse(message: Msg, operations: list, data=None):
    response = {
        'message': message.__dict__,
        'operations': operations
    }
    response['data'] = data if data else None
    return response


# def get_user(token):
#     # return Token.objects.get(key=f'caeb67f1d1ae7e833900c34be0615b9c943544a0').user
#     return Token.objects.get(key=f'{token}').user


def set_receive(request, content_type):
    receive = request.data if content_type == 'application/json' else request.POST
    return receive

# Response format example
# {
#     "message": {
#         "error": null,
#         "success": null
#     },
#     "operations": [
#         {
#             "action": "edit",
#             "url": "/api/edit-profile",
#             "params": {
#                 "phone": null,
#                 "gender": null,
#                 "city": null,
#                 "skype": null,
#                 "country": null,
#                 "email": null,
#                 "birthday": null
#             }
#         }
#     ],
#     "data": null
# }