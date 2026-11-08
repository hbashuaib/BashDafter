from django.urls import path

from .views import (
        CustomerStatementView,
        CustomerSummaryReportView,
        RecentTransactionsReportView,
        TopDebtorsReportView,
)

urlpatterns = [
    path("reports/customer-summary/", CustomerSummaryReportView.as_view(), name="customer-summary-report",),
    path("reports/top-debtors/", TopDebtorsReportView.as_view(), name="top-debtors-report",),
    path("reports/recent-transactions/", RecentTransactionsReportView.as_view(), name="recent-transactions-report",),
    path("reports/customer-statement/<int:customer_id>/", CustomerStatementView.as_view(), name="customer-statement",),
]