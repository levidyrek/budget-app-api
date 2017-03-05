from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import viewsets
from .models import (Budget, CategoryBudgetGroup, Category, CategoryBudget,
					 Transaction, Income, LongTermGoal, BudgetGoal, OwnedModel)
from .permissions import IsOwnerOrAdmin
from .serializers import (BudgetSerializer, CategoryBudgetGroupSerializer,
						  CategorySerializer, CategoryBudgetSerializer, TransactionSerializer,
						  IncomeSerializer, LongTermGoalSerializer, BudgetGoalSerializer,
						  UserSerializer)
from rest_framework.exceptions import APIException


def check_for_owner_conflict(viewset, data):
	"""
	Static method that checks for owner conflicts
	"""

	# Get all owned models
	owned_items = list()
	for item in data.items():
		if isinstance(item, tuple):
			obj = item[1]
			if isinstance(obj, OwnedModel):
				owned_items.append(obj)
			elif isinstance(obj, list):
				for list_item in obj:
					if isinstance(list_item, OwnedModel):
						owned_items.append(list_item)

	# Check if any of the owned items have owner conflicts
	for owned_model in owned_items:
		if owned_model.has_owner_conflict(viewset.request.user):
			raise OwnerConflictException


class OwnedModelViewSet(viewsets.ModelViewSet):
	"""
	Provides methods to validate ownership
	"""

	def check_for_owner_conflict(self, data):
		check_for_owner_conflict(self, data)

	def perform_create(self, serializer):
		self.check_for_owner_conflict(serializer.validated_data)
		serializer.save(owner=self.request.user)

	def perform_update(self, serializer):
		self.check_for_owner_conflict(serializer.validated_data)
		serializer.save()


class BudgetViewSet(OwnedModelViewSet):
	queryset = Budget.objects.all()
	serializer_class = BudgetSerializer
	permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)

	def get_queryset(self):
		return Budget.objects.filter(owner=self.request.user)


class LongTermGoalViewSet(OwnedModelViewSet):
	queryset = LongTermGoal.objects.all()
	serializer_class = LongTermGoalSerializer
	permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)

	def get_queryset(self):
		return LongTermGoal.objects.filter(owner=self.request.user)


class CategoryBudgetViewSet(OwnedModelViewSet):
	queryset = CategoryBudget.objects.all()
	serializer_class = CategoryBudgetSerializer
	permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)

	def get_queryset(self):
		return CategoryBudget.objects.filter(owner=self.request.user)


class IncomeViewSet(OwnedModelViewSet):
	queryset = Income.objects.all()
	serializer_class = IncomeSerializer
	permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)

	def get_queryset(self):
		return Income.objects.filter(owner=self.request.user)


class CategoryViewSet(OwnedModelViewSet):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer
	permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)

	def get_queryset(self):
		return Category.objects.filter(owner=self.request.user)


class CategoryBudgetGroupViewSet(OwnedModelViewSet):
	queryset = CategoryBudgetGroup.objects.all()
	serializer_class = CategoryBudgetGroupSerializer
	permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)

	def get_queryset(self):
		return CategoryBudgetGroup.objects.filter(owner=self.request.user)


class TransactionViewSet(OwnedModelViewSet):
	queryset = Transaction.objects.all()
	serializer_class = TransactionSerializer
	permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)

	def get_queryset(self):
		return Transaction.objects.filter(owner=self.request.user)


class BudgetGoalViewSet(OwnedModelViewSet):
	queryset = BudgetGoal.objects.all()
	serializer_class = BudgetGoalSerializer
	permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)

	def get_queryset(self):
		return BudgetGoal.objects.filter(owner=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = (permissions.IsAdminUser,)

	def perform_create(self, serializer):
		check_for_owner_conflict(self, serializer.validated_data)
		serializer.save()

	def perform_update(self, serializer):
		check_for_owner_conflict(self, serializer.validated_data)
		serializer.save()


""" API Exceptions """


class OwnerConflictException(APIException):
	status_code = 403
	default_detail = 'Conflict of owners within object'
	default_code = 'owner_conflict'
