from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.customers.models import Customer
from apps.purchases.models import Purchase
from apps.payments.models import Payment


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

class RecentTransactionsReportView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):
        shop = request.user.shop

        purchases = Purchase.objects.filter(
            customer__shop=shop
        ).order_by("-created_at")[:10]

        payments = Payment.objects.filter(
            customer__shop=shop
        ).order_by("-created_at")[:10]

        transactions = []

        for purchase in purchases:
            transactions.append({
                "type": "purchase",
                "customer": purchase.customer.name,
                "amount": purchase.total_amount,
                "date": purchase.purchase_date,
            })

        for payment in payments:
            transactions.append({
                "type": "payment",
                "customer": payment.customer.name,
                "amount": payment.amount,
                "date": payment.payment_date,
            })

        transactions = sorted(
            transactions,
            key=lambda x: x["date"],
            reverse=True
        )

        return Response(
            transactions[:20]
        )


class CustomerStatementView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, customer_id):
        customer = Customer.objects.get(id=customer_id, shop=request.user.shop,)
        transactions = []
        purchases = Purchase.objects.filter(customer=customer)
        payments = Payment.objects.filter(customer=customer)

        for purchase in purchases:
            transactions.append({
                "type": "purchase",
                "date": purchase.purchase_date,
                "amount": float(
                    purchase.total_amount
                ),
            })

        for payment in payments:
            transactions.append({
                "type": "payment",
                "date": payment.payment_date,
                "amount": float(
                    payment.amount
                ),
            })

        transactions = sorted(transactions, key=lambda x: x["date"])

        return Response({
            "customer": customer.name,
            "balance": customer.balance,
            "transactions": transactions
        })