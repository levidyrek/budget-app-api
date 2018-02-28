from rest_framework import serializers
from .models import (Budget, BudgetCategoryGroup, BudgetCategory,
                     Transaction, Income, LongTermGoal, BudgetGoal)
from django.contrib.auth.models import User
from rest_framework.utils.serializer_helpers import ReturnDict

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
    '''
    Overrides default ListSerializer to return a dict with a custom field from
    each item as the key. Makes it easier to normalize the data so that there
    is minimal nesting. Must override to_representation to produce a dict with
    the desired keys.
    '''

    @property
    def data(self):
        ret = super(serializers.ListSerializer, self).data
        return ReturnDict(ret, serializer=self)

    def to_representation(self, data):
        raise Exception('Must override to_representation')


class PkDictSerializer(DictSerializer):

    def to_representation(self, data):
        items = super(DictSerializer, self).to_representation(data)
        ret = {}
        for item in items:
            try:
                ret[item['pk']] = item
            except AttributeError:
                raise Exception(
                    'Item has no pk. Returning list instead of dict.')

        return ret


class MonthYearDictSerializer(DictSerializer):

    def to_representation(self, data):
        items = super(DictSerializer, self).to_representation(data)
        ret = {}
        for item in items:
            try:
                ret[item['month'] + str(item['year'])] = item
            except AttributeError:
                raise Exception(
                    'Item has no month/year. Returning list instead of dict.')

        return ret


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


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='budgetapp:transaction-detail')
    budget_category = budget_category_field

    class Meta:
        model = Transaction
        fields = ('pk', 'url', 'amount', 'recipient',
                  'budget_category', 'date')
        list_serializer_class = PkDictSerializer


class BudgetCategorySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='budgetapp:budgetcategory-detail')
    group = serializers.PrimaryKeyRelatedField(
        queryset=BudgetCategoryGroup.objects.all()
    )
    transactions = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )

    class Meta:
        model = BudgetCategory
        fields = ('url', 'pk', 'category', 'group', 'limit', 'spent',
                  'transactions',)
        list_serializer_class = PkDictSerializer


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
        list_serializer_class = PkDictSerializer


class BudgetDetailSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='budgetapp:budget-detail')
    owner = owner_field
    budget_category_groups = BudgetCategoryGroupSerializer(
        many=True,
        read_only=True
    )
    budget_categories = serializers.SerializerMethodField()
    incomes = IncomeSerializer(
        many=True,
        read_only=True
    )
    transactions = serializers.SerializerMethodField()
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

    def get_transactions(self, budget):
        result = Transaction.objects.filter(
            budget_category__group__budget__pk=budget.pk)
        serializer = TransactionSerializer(
            result,
            many=True,
            context={'request': self.context['request']}
        )
        return serializer.data

    class Meta:
        model = Budget
        fields = ('url', 'owner', 'month', 'year', 'budget_category_groups',
                  'budget_categories', 'incomes', 'transactions',
                  'budget_goals')


class BudgetListSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='budgetapp:budget-detail')
    owner = owner_field

    class Meta:
        model = Budget
        fields = ('url', 'owner', 'month', 'year')
        list_serializer_class = MonthYearDictSerializer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='budgetapp:user-detail')
    budgets = serializers.HyperlinkedRelatedField(
        view_name='budgetapp:budget-detail',
        many=True,
        read_only=True
    )
    long_term_goals = serializers.HyperlinkedRelatedField(
        view_name='budgetapp:longtermgoal-detail',
        many=True,
        read_only=True
    )

    class Meta:
        model = User
        fields = ('url', 'email', 'username', 'password',
                  'budgets', 'long_term_goals',)
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
