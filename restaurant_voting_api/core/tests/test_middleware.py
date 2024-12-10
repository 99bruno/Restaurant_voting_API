from django.test import TestCase, RequestFactory
from django.http import JsonResponse
from rest_framework import status
from core.middleware import AppVersionMiddleware


class AppVersionMiddlewareTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = AppVersionMiddleware(self._dummy_get_response)

    def _dummy_get_response(self, request):
        return JsonResponse({'message': 'Success'}, status=status.HTTP_200_OK)

    def test_no_app_version_header(self):
        """Test when the App-Version header is not provided."""
        request = self.factory.get('/')
        response = self.middleware(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(request.app_version, None)

    def test_supported_app_version(self):
        """Test when the App-Version header has a supported version."""
        request = self.factory.get('/', HTTP_APP_VERSION='1.5')
        response = self.middleware(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(request.app_version, '1.5')

    def test_unsupported_app_version(self):
        """Test when the App-Version header has an unsupported version."""
        request = self.factory.get('/', HTTP_APP_VERSION='0.9')
        response = self.middleware(request)

        self.assertEqual(response.status_code, status.HTTP_426_UPGRADE_REQUIRED)
        self.assertJSONEqual(
            response.content,
            {'error': 'Unsupported app version. Please update.'}
        )
