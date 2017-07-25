from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import viewsets, generics
from .models import (Budget, BudgetCategoryGroup, BudgetCategory,
					 Transaction, Income, LongTermGoal, BudgetGoal, OwnedModel)
from .permissions import IsOwnerOrAdmin
from .serializers import (BudgetDetailSerializer, BudgetListSerializer, BudgetCategoryGroupSerializer,
						  BudgetCategorySerializer, TransactionSerializer,
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
	serializer_class = BudgetDetailSerializer
	permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)

	def get_serializer_class(self):
		if self.action == 'list':
			return BudgetListSerializer
		else:
			return BudgetDetailSerializer

	def get_queryset(self):
		return Budget.objects.filter(owner=self.request.user)


class LongTermGoalViewSet(OwnedModelViewSet):
	queryset = LongTermGoal.objects.all()
	serializer_class = LongTermGoalSerializer
	permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)

	def get_queryset(self):
		return LongTermGoal.objects.filter(owner=self.request.user)


class BudgetCategoryViewSet(OwnedModelViewSet):
	queryset = BudgetCategory.objects.all()
	serializer_class = BudgetCategorySerializer
	permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)

	def get_queryset(self):
		return BudgetCategory.objects.filter(owner=self.request.user)


class IncomeViewSet(OwnedModelViewSet):
	queryset = Income.objects.all()
	serializer_class = IncomeSerializer
	permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)

	def get_queryset(self):
		return Income.objects.filter(owner=self.request.user)


class BudgetCategoryGroupViewSet(OwnedModelViewSet):
	queryset = BudgetCategoryGroup.objects.all()
	serializer_class = BudgetCategoryGroupSerializer
	permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)

	def get_queryset(self):
		return BudgetCategoryGroup.objects.filter(owner=self.request.user)


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


class UserCreateView(generics.CreateAPIView):
	"""
	Used to create a user. Anonymous users can use this.
	TODO: Prevent automated usage of this view
	"""
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = (permissions.AllowAny,)

	def perform_create(self, serializer):
		check_for_owner_conflict(self, serializer.validated_data)
		serializer.save()


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
	"""
	Actions an authenticated user can do only to their own User
	object (Retrieve, Update, Destroy). 
	"""
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin,)

	def perform_update(self, serializer):
		check_for_owner_conflict(self, serializer.validated_data)
		serializer.save()


class UserListView(generics.ListAPIView):
	"""
	List view for Users. Only admin users can use this.
	"""
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = (permissions.IsAdminUser,)


""" API Exceptions """


class OwnerConflictException(APIException):
	status_code = 403
	default_detail = 'Conflict of owners within object'
	default_code = 'owner_conflict'
