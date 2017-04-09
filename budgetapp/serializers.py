from rest_framework import serializers
from .models import (Budget, CategoryBudgetGroup, Category, CategoryBudget,
                     Transaction, Income, LongTermGoal, BudgetGoal)
from django.contrib.auth.models import User

# Multi-use fields
owner_field = serializers.ReadOnlyField(source='owner.username')
budget_field = serializers.HyperlinkedRelatedField(
    queryset=Budget.objects.all(),
    view_name='budgetapp:budget-detail'
)
category_budget_field = serializers.HyperlinkedRelatedField(
    queryset=CategoryBudget.objects.all(),
    view_name='budgetapp:categorybudget-detail'
)
category_budgets_field = serializers.HyperlinkedRelatedField(
    queryset=CategoryBudget.objects.all(),
    view_name='budgetapp:categorybudget-detail',
    many=True
)


class LongTermGoalSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="budgetapp:longtermgoal-detail")
    owner = owner_field
    budget_goals = serializers.HyperlinkedRelatedField(
        queryset=BudgetGoal.objects.all(),
        view_name='budgetapp:budgetgoal-detail',
        many=True
    )

    class Meta:
        model = LongTermGoal
        fields = ('url', 'name', 'goal_amount', 'progress', 'due_date', 'owner', 'budget_goals')


class BudgetGoalSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="budgetapp:budgetgoal-detail")
    owner = owner_field
    budget = budget_field
    long_term_goal = serializers.HyperlinkedRelatedField(
        queryset=LongTermGoal.objects.all(),
        view_name='budgetapp:longtermgoal-detail'
    )

    class Meta:
        model = BudgetGoal
        fields = ('url', 'owner', 'name', 'goal_amount', 'progress', 'budget', 'long_term_goal')


class IncomeSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="budgetapp:income-detail")
    owner = owner_field
    budget = budget_field

    class Meta:
        model = Income
        fields = ('url', 'owner', 'name', 'amount', 'budget')


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="budgetapp:transaction-detail")
    owner = owner_field
    category_budget = category_budget_field

    class Meta:
        model = Transaction
        fields = ('url', 'owner', 'amount', 'recipient', 'category_budget', 'date')


class CategoryBudgetSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="budgetapp:categorybudget-detail")
    owner = owner_field
    category = serializers.HyperlinkedRelatedField(
        queryset=Category.objects.all(),
        view_name='budgetapp:category-detail'
    )
    group = serializers.HyperlinkedRelatedField(
        queryset=CategoryBudgetGroup.objects.all(),
        view_name='budgetapp:categorybudgetgroup-detail'
    )
    transactions = serializers.HyperlinkedRelatedField(
        queryset=Transaction.objects.all(),
        view_name='budgetapp:transaction-detail',
        many=True
    )

    class Meta:
        model = CategoryBudget
        fields = ('url', 'owner', 'category', 'group', 'limit', 'spent', 'transactions')


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="budgetapp:category-detail")
    owner = owner_field
    category_budgets = category_budgets_field

    class Meta:
        model = Category
        fields = ('url', 'name', 'owner', 'category_budgets')


class CategoryBudgetGroupSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="budgetapp:categorybudgetgroup-detail")
    owner = owner_field
    budget = serializers.HyperlinkedRelatedField(
        queryset=Budget.objects.all(),
        view_name='budgetapp:budget-detail'
    )
    category_budgets = category_budgets_field

    class Meta:
        model = CategoryBudgetGroup
        fields = ('url', 'owner', 'name', 'budget', 'category_budgets')


class BudgetSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="budgetapp:budget-detail")
    owner = owner_field
    category_budget_groups = serializers.HyperlinkedRelatedField(
        queryset=CategoryBudgetGroup.objects.all(),
        view_name='budgetapp:categorybudgetgroup-detail',
        many=True
    )
    incomes = serializers.HyperlinkedRelatedField(
        queryset=Income.objects.all(),
        view_name='budgetapp:income-detail',
        many=True
    )
    budget_goals = serializers.HyperlinkedRelatedField(
        queryset=BudgetGoal.objects.all(),
        view_name='budgetapp:budgetgoal-detail',
        many=True
    )

    class Meta:
        model = Budget
        unique_together = ('owner', 'month', 'year')
        fields = ('url', 'month', 'year', 'owner', 'category_budget_groups', 'incomes',
                  'budget_goals')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="budgetapp:user-detail")
    budgets = serializers.HyperlinkedRelatedField(
        queryset=Budget.objects.all(),
        view_name='budgetapp:budget-detail',
        many=True
    )
    long_term_goals = serializers.HyperlinkedRelatedField(
        queryset=LongTermGoal.objects.all(),
        view_name='budgetapp:longtermgoal-detail',
        many=True
    )
    categories = serializers.HyperlinkedRelatedField(
        queryset=Category.objects.all(),
        view_name='budgetapp:category-detail',
        many=True
    )

    class Meta:
        model = User
        fields = ('url', 'email', 'username', 'password', 'budgets',
                  'long_term_goals', 'categories')
