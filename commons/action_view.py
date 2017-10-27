from rest_framework.views import APIView
from django.http import JsonResponse

ACTIONS = {}


class ActionView(APIView, JsonResponse):
    def post(self, request, pk=None, format=None, *args, **kwargs):
        data = request.data
        action = None
        param = {}
        for (d, x) in data.items():
            action = d
            param = x

        return self.run(action,pk, param, request)

    def put(self, request, pk, format=None, *args, **kwargs):
        data = request.data
        action = None
        param = {}
        for (d, x) in data.items():
            action = d
            param = x

        return self.run(action,pk, param, request)

    def run(self, action,pk, param, request):
        func = ACTIONS[self.__class__][action]
        return func(self, request,pk, param)

