from django.db import connection
from django.db.utils import OperationalError
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckAPIView(APIView):
    """
    Usado para checar status da aplicação.
    """

    permission_classes = [AllowAny]

    def get(self, *args, **kwargs) -> Response:
        """
        Retorna status da aplicação.
        """
        try:
            connection.ensure_connection()
            db_connection = 'OK'
            status_response = status.HTTP_200_OK
        except OperationalError:
            db_connection = 'ERROR'
            status_response = status.HTTP_503_SERVICE_UNAVAILABLE
        response = {
            'status': 'OK',
            'db_connection': db_connection,
        }
        return Response(response, status=status_response)
