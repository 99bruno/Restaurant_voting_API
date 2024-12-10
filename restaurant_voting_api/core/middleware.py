from django.http import JsonResponse
from rest_framework import status


class AppVersionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Middleware to check the app version in the request header

        :param request:
        :return:
        """
        app_version = request.headers.get('App-Version', None)

        request.app_version = app_version

        if app_version and float(app_version) < 1.0:
            return JsonResponse({'error': 'Unsupported app version. Please update.'},
                                status=status.HTTP_426_UPGRADE_REQUIRED)

        response = self.get_response(request)
        return response
