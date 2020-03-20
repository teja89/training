from django.urls import path
from .views import ListAllEmployeeView, EmployeeDetailView


urlpatterns = [
    path('employee/<int:id>/', EmployeeDetailView.as_view(), name="employee-detail"),
    path('employee/', ListAllEmployeeView.as_view(), name="employee-list")
]