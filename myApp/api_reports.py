from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from .reports import get_report_data

class ReporteSistemaAPI(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        start = request.GET.get("start")
        end = request.GET.get("end")

        data = get_report_data(start, end)
        return Response(data)
