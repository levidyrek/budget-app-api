from django.contrib.auth.models import User
from rest_framework import generics, permissions, viewsets

from .models import (Budget, BudgetCategory, BudgetCategoryGroup, BudgetGoal,
                     Income, LongTermGoal, Transaction)
from .permissions import (BudgetCategoryGroupPermission,
                          BudgetCategoryPermission, BudgetGoalPermission,
                          IncomePermission, IsOwnerOrAdmin,
                          TransactionPermission)
from .serializers import (BudgetCategoryGroupSerializer,
                          BudgetCategorySerializer, BudgetSerializer,
                          BudgetGoalSerializer,
                          IncomeSerializer, LongTermGoalSerializer,
                          TransactionSerializer, UserSerializer)


class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)
    filter_fields = ('month', 'year',)

    def get_queryset(self):
        return Budget.objects.filter(owner=self.request.user)


class BudgetCategoryGroupViewSet(viewsets.ModelViewSet):
    queryset = BudgetCategoryGroup.objects.all()
    serializer_class = BudgetCategoryGroupSerializer
    permission_classes = (permissions.IsAuthenticated,
                          BudgetCategoryGroupPermission)

    def get_queryset(self):
        return BudgetCategoryGroup.objects.filter(
            budget__owner=self.request.user)


class BudgetCategoryViewSet(viewsets.ModelViewSet):
    queryset = BudgetCategory.objects.all()
    serializer_class = BudgetCategorySerializer
    permission_classes = (permissions.IsAuthenticated,
                          BudgetCategoryPermission)

    def get_queryset(self):
        return BudgetCategory.objects.filter(
            group__budget__owner=self.request.user)


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = (permissions.IsAuthenticated,
                          TransactionPermission)

    def get_queryset(self):
        return Transaction.objects.filter(
            budget_category__group__budget__owner=self.request.user)


class IncomeViewSet(viewsets.ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    permission_classes = (permissions.IsAuthenticated,
                          IncomePermission)

    def get_queryset(self):
        return Income.objects.filter(budget__owner=self.request.user)


class LongTermGoalViewSet(viewsets.ModelViewSet):
    queryset = LongTermGoal.objects.all()
    serializer_class = LongTermGoalSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)

    def get_queryset(self):
        return LongTermGoal.objects.filter(owner=self.request.user)


class BudgetGoalViewSet(viewsets.ModelViewSet):
    queryset = BudgetGoal.objects.all()
    serializer_class = BudgetGoalSerializer
    permission_classes = (permissions.IsAuthenticated,
                          BudgetGoalPermission)

    def get_queryset(self):
        return BudgetGoal.objects.filter(budget__owner=self.request.user)


class UserCreateView(generics.CreateAPIView):
    """
    Used to create a user. Anonymous users can use this.
    TODO: Prevent automated usage of this view
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Actions an authenticated user can do only to their own User
    object (Retrieve, Update, Destroy).
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin,)


class UserListView(generics.ListAPIView):
    """
    List view for Users. Only admin users can use this.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)
