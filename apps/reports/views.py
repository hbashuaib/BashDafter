from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.customers.models import Customer


class CustomerSummaryReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        customers = Customer.objects.filter(shop=request.user.shop)
        data = []

        for customer in customers:
            data.append({
                "id": customer.id,
                "name": customer.name,
                "phone": customer.phone,
                "total_purchases": customer.total_purchases,
                "total_payments": customer.total_payments,
                "balance": customer.balance,
            })

        return Response(data)


class TopDebtorsReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        customers = Customer.objects.filter(shop=request.user.shop)
        data = []

        for customer in customers:
            data.append({
                "id": customer.id,
                "name": customer.name,
                "balance": customer.balance,
            })

        data = sorted(data, key=lambda x: x["balance"], reverse=True)

        return Response(data[:10])
