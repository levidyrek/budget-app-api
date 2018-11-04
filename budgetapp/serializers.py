from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict

from .models import (Budget, BudgetCategory, BudgetCategoryGroup, BudgetGoal,
                     Income, LongTermGoal, Transaction)

# Multi-use fields
owner_field = serializers.PrimaryKeyRelatedField(
    read_only=True, default=serializers.CurrentUserDefault())
budget_field = serializers.HyperlinkedRelatedField(
    queryset=Budget.objects.all(),
    view_name='budgetapp:budget-detail'
)
budget_category_field = serializers.HyperlinkedRelatedField(
    queryset=BudgetCategory.objects.all(),
    view_name='budgetapp:budgetcategory-detail'
)
budgets_category_field = serializers.HyperlinkedRelatedField(
    view_name='budgetapp:budgetcategory-detail',
    many=True,
    read_only=True
)


class DictSerializer(serializers.ListSerializer):
    """
    Overrides default ListSerializer to return a dict with a custom field from
    each item as the key. Makes it easier to normalize the data so that there
    is minimal nesting. dict_key defaults to 'pk' but can be overridden.
    """
    dict_key = 'pk'

    @property
    def data(self):
        """
        Overriden to return a ReturnDict instead of a ReturnList.
        """
        ret = super(serializers.ListSerializer, self).data
        return ReturnDict(ret, serializer=self)

    def to_representation(self, data):
        """
        Converts the data from a list to a dictionary.
        """
        items = super(DictSerializer, self).to_representation(data)
        return {item[self.dict_key]: item for item in items}


class LongTermGoalSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='budgetapp:longtermgoal-detail')
    owner = owner_field
    budget_goals = serializers.HyperlinkedRelatedField(
        view_name='budgetapp:budgetgoal-detail',
        many=True,
        read_only=True
    )

    class Meta:
        model = LongTermGoal
        fields = ('url', 'name', 'goal_amount', 'progress', 'due_date',
                  'owner', 'budget_goals',)


class BudgetGoalSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='budgetapp:budgetgoal-detail')
    budget = budget_field
    long_term_goal = serializers.HyperlinkedRelatedField(
        queryset=LongTermGoal.objects.all(),
        view_name='budgetapp:longtermgoal-detail'
    )

    class Meta:
        model = BudgetGoal
        fields = ('url', 'name', 'goal_amount', 'progress', 'budget',
                  'long_term_goal')


class IncomeSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='budgetapp:income-detail')
    budget = budget_field

    class Meta:
        model = Income
        fields = ('url', 'name', 'amount', 'budget')


class BudgetCategorySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='budgetapp:budgetcategory-detail')
    group = serializers.PrimaryKeyRelatedField(
        queryset=BudgetCategoryGroup.objects.all()
    )

    def validate(self, data):
        super().validate(data)

        # Enforce uniqueness between category name and budget.
        existing = BudgetCategory.objects.filter(
            group__budget=data['group'].budget,
            category=data['category'],
        )
        if existing.exists():
            raise serializers.ValidationError(
                'Category must be unique within this budget.'
            )

        return data

    class Meta:
        model = BudgetCategory
        fields = ('url', 'pk', 'category', 'group', 'limit', 'spent',)
        list_serializer_class = DictSerializer


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='budgetapp:transaction-detail')
    budget_category_id = serializers.IntegerField()

    class Meta:
        model = Transaction
        fields = ('url', 'amount', 'recipient',
                  'budget_category_id', 'date')


class BudgetCategoryGroupSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='budgetapp:budgetcategorygroup-detail')
    budget = serializers.HyperlinkedRelatedField(
        queryset=Budget.objects.all(),
        view_name='budgetapp:budget-detail'
    )
    budget_categories = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )

    class Meta:
        model = BudgetCategoryGroup
        fields = ('url', 'pk', 'name', 'budget', 'budget_categories',)
        list_serializer_class = DictSerializer


class BudgetSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='budgetapp:budget-detail')
    owner = owner_field
    budget_category_groups = BudgetCategoryGroupSerializer(
        many=True,
        read_only=True
    )
    budget_categories = serializers.SerializerMethodField()
    budget_goals = BudgetGoalSerializer(
        many=True,
        read_only=True
    )

    def get_budget_categories(self, budget):
        budget_cats = BudgetCategory.objects.filter(
            group__budget__pk=budget.pk)
        serializer = BudgetCategorySerializer(
            budget_cats,
            many=True,
            context={'request': self.context['request']}
        )
        return serializer.data

    class Meta:
        model = Budget
        fields = ('url', 'owner', 'month', 'year', 'budget_category_groups',
                  'budget_categories', 'budget_goals')


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username', 'password',)
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
