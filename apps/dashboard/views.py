from django.db.models import Sum
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.customers.models import Customer
from apps.payments.models import Payment
from apps.purchases.models import Purchase


class DashboardView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        shop = request.user.shop
        customer_count = Customer.objects.filter(shop=shop).count()
        total_purchases = Purchase.objects.filter(customer__shop=shop).aggregate(
            total=Sum("total_amount")
        )["total"] or 0

        total_payments = Payment.objects.filter(customer__shop=shop).aggregate(
            total=Sum("amount")
        )["total"] or 0

        total_balance = (total_purchases - total_payments)
        customers = Customer.objects.filter(shop=shop)
        
        top_debtors = []

        for customer in customers:
            top_debtors.append({
                "id": customer.id,
                "name": customer.name,
                "balance": customer.balance,
            })

        top_debtors = sorted(top_debtors, key=lambda x: x["balance"],
            reverse=True
        )[:5]
        
        recent_purchases = Purchase.objects.filter(customer__shop=shop).order_by(
            "-purchase_date"
        )[:5]
        
        recent_purchases_data = [
            {
                "customer": purchase.customer.name,
                "amount": purchase.total_amount,
                "date": purchase.purchase_date,
            }

            for purchase in recent_purchases
        ]
        
        recent_payments = Payment.objects.filter(customer__shop=shop).order_by(
            "-payment_date"
        )[:5]
        
        recent_payments_data = [
            {
                "customer": payment.customer.name,
                "amount": payment.amount,
                "date": payment.payment_date,
            }

            for payment in recent_payments
        ]


        return Response({
            "customers": customer_count,
            "total_purchases": total_purchases,
            "total_payments": total_payments,
            "total_balance": total_balance,
            "top_debtors": top_debtors,
            "recent_purchases": recent_purchases_data,
            "recent_payments": recent_payments_data,
        })