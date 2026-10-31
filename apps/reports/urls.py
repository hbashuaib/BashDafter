from django.urls import path

from .views import CustomerSummaryReportView, TopDebtorsReportView

urlpatterns = [
    path("reports/customer-summary/", CustomerSummaryReportView.as_view(), name="customer-summary-report",),
    path("reports/top-debtors/", TopDebtorsReportView.as_view(), name="top-debtors-report",),
]