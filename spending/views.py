from django.shortcuts import render
from rest_framework.views import APIView
from spending.serializers import Userserializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import authentication,permissions
from spending.models import Expense
from spending.serializers import ExpenseSerializer
from django.shortcuts import get_object_or_404
from spending.permissions import Isowner
from datetime import datetime
from django.db.models import Sum
from spending.ai_summary import get_budget_plan


# Create your views here.
class UserregisterView(APIView):
    def post(self,request):
        form_data=request.data
        serializer_instance=Userserializer(data=form_data)
        if serializer_instance.is_valid():
            cleaned_data=serializer_instance.validated_data

            qs=User.objects.create_user(**cleaned_data)
            serializer_instance=Userserializer(qs)
            return Response(data=serializer_instance.data)
        else:
            return Response(data=serializer_instance.errors)

class GetMeView(APIView):


    authentication_classes=[authentication.BasicAuthentication]

    permission_classes=[permissions.IsAuthenticated]


    def get(self,request):


        auth_user =request.user

        instance =User.objects.get(username=auth_user)

        serializer_inst =Userserializer(instance)

        return Response(data=serializer_inst.data) 


class ExpenseListCreateView(APIView):
    #authentication_classes=[authentication.BasicAuthentication]
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    def get(self,request):

        instance=Expense.objects.filter(owner=request.user)
        serializer_instance=ExpenseSerializer(instance,many=True)
        return Response(data=serializer_instance.data)

    def post(self,request):
        form_data=request.data
        instance=ExpenseSerializer(data=form_data)
        if instance.is_valid():
            instance.save(owner=request.user)
            return Response(data=instance.data)
        else:
            return Response(data=instance.errors)


class ExpenseRetrieveUpdateDeleteView(APIView):

    #authentication_classes = [authentication.BasicAuthentication]
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes = [Isowner]

    def get(self,request,pk=None):

        instance = get_object_or_404(Expense,id=pk)
        self.check_object_permissions(request,instance)

        serializer_instance = ExpenseSerializer(instance)

        return Response(data=serializer_instance.data)

    def put(self,request,pk=None):

        instance = get_object_or_404(Expense,id=pk)
        self.check_object_permissions(request,instance)

        form_data = request.data

        serializer_instance = ExpenseSerializer(data=form_data,instance=instance)

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data=serializer_instance.data)

        else:

            return Response(data=serializer_instance.errors)

    def delete(self,request,pk=None):

        instance = get_object_or_404(Expense,id=pk)
        self.check_object_permissions(request,instance)

        instance.delete()

        return Response(data={"message":"deleted"})


class ExpenseSummaryView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    def get(self,request):

        response_data={
            "todays_total":0
        } 
        current_date=datetime.now().date()



#current month transations
        current_month=datetime.now().month
        current_year=datetime.now().year

        current_month_transations=Expense.objects.filter(owner=request.user,created_at__month=current_month,created_at__year=current_year)
        if current_month_transations:
            current_month_total=current_month_transations.values("amount").aggregate(total=Sum("amount")).get("total")

            
            

#todays summary
        todays_transations=Expense.objects.filter(owner=request.user,created_at__date=current_date) 
        if todays_transations:
            totadys_total=todays_transations.values("amount").aggregate(total=Sum("amount")).get("total")



#category wise summary            
            category_summary=todays_transations.values("category").annotate(total=Sum("amount"))
            response_data={
              "todays_total":totadys_total
        } 
            response_data["category_summary"]=category_summary
            response_data["current_month_total"]=current_month_total
            
        return Response(data=response_data)


#budgetplan
class BudgetPlanView(APIView):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):
        
        response_data={
            "monthly_total":0
        } 
       
        curr_month=datetime.now().month
        curr_year=datetime.now().year

        monthly_transations=Expense.objects.filter(owner=request.user,created_at__month=curr_month,created_at__year=curr_year)
        if monthly_transations:
            total_monthly_transations=monthly_transations.values("amount").aggregate(total=Sum("amount")).get("total")
            category_transation=monthly_transations.values("category").annotate(total=Sum("amount"))
            response_data["monthly_total"]=total_monthly_transations
            response_data["category_summary"]=category_transation
            budgetplan=get_budget_plan(response_data)
            response_data["plan"]=budgetplan

        return Response(data=response_data)    


        

        
            


         
           
         
                
