# -*- coding: utf-8 -*-
import logging
from rest_auth.serializers import JWTSerializer
from rest_auth.views import LoginView
from rest_framework import status
from rest_framework.response import Response


class PycLoginView(LoginView):
    def get_response(self):
        logging.info(self)

        try:
            data = {
                'user': self.user,
                'token': self.token
            }

            serializer = JWTSerializer(instance=data, context={'request': self.request})

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logging.exception(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
