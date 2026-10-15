from django.urls import path
from spending.views import UserregisterView
from spending.views import GetMeView,ExpenseListCreateView,ExpenseRetrieveUpdateDeleteView,ExpenseSummaryView,BudgetPlanView
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns=[
    path("register/",UserregisterView.as_view()),
    path('getme/',GetMeView.as_view()),
    path('listcreate/',ExpenseListCreateView.as_view()),
    path('retrieveupdel/<int:pk>/',ExpenseRetrieveUpdateDeleteView.as_view()),
    path('token/',ObtainAuthToken.as_view()),
    path('summary/',ExpenseSummaryView.as_view()),
    path('month/',BudgetPlanView.as_view()),

]