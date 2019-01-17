from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict

from .models import (Budget, BudgetCategory, BudgetCategoryGroup, Payee,
                     Transaction)

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


class BudgetCategorySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='budgetapp:budgetcategory-detail')
    group = serializers.CharField(source='group.name')
    budget_month = serializers.CharField(write_only=True)
    budget_year = serializers.IntegerField(write_only=True)

    def validate(self, data):
        super().validate(data)

        # Enforce uniqueness between category name and budget.
        budget_month = data.get('budget_month')
        budget_year = data.get('budget_year')
        category = data.get('category')

        # If this is an update, default values to the instance
        # values if updated values were not given.
        if self.instance:
            budget_month = budget_month or self.instance.group.budget.month
            budget_year = budget_year or self.instance.group.budget.year
            category = category or self.instance.category

        existing = BudgetCategory.objects.filter(
            group__budget__month=budget_month,
            group__budget__year=budget_year,
            category=category,
        )

        if self.instance:
            existing = existing.exclude(id=self.instance.id)

        if existing.exists():
            raise serializers.ValidationError(
                'Category must be unique within this budget.'
            )

        return data

    def create(self, validated_data):
        self.get_or_create_related(validated_data)
        return BudgetCategory.objects.create(**validated_data)

    def update(self, instance, validated_data):
        self.get_or_create_related(validated_data)
        return super().update(instance, validated_data)

    def get_or_create_related(self, validated_data):
        """
        Takes given budget/category/group data and either creates
        the corresponding models, if the don't already exist, or uses
        the existing ones to populate the required group field.
        """
        budget_month = validated_data.get('budget_month')
        budget_year = validated_data.get('budget_year')
        category = validated_data.get('category')
        group = validated_data.get('group', {}).get('name')

        # If this is an update, default values to the instance
        # values if updated values were not given.
        if self.instance:
            budget_month = budget_month or self.instance.group.budget.month
            budget_year = budget_year or self.instance.group.budget.year
            category = category or self.instance.category
            group = group or self.instance.group.name

        budget, created = Budget.objects.get_or_create(
            month=budget_month,
            year=budget_year,
            owner=self.context['request'].user,
        )

        group, created = BudgetCategoryGroup.objects.get_or_create(
            budget=budget,
            name=group,
        )

        validated_data.pop('budget_month', None)
        validated_data.pop('budget_year', None)
        validated_data.pop('group', None)

        validated_data['group'] = group

    class Meta:
        model = BudgetCategory
        fields = (
            'url', 'pk', 'budget_month', 'budget_year', 'category', 'group',
            'limit', 'spent',
        )
        list_serializer_class = DictSerializer


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='budgetapp:transaction-detail')
    budget_category = serializers.PrimaryKeyRelatedField(
        queryset=BudgetCategory.objects.all(),
    )
    payee = serializers.CharField()

    def create(self, validated_data):
        self.get_or_create_related(validated_data)
        return Transaction.objects.create(**validated_data)

    def update(self, instance, validated_data):
        self.get_or_create_related(validated_data)
        return super().update(instance, validated_data)

    def get_or_create_related(self, validated_data):
        payee = validated_data.get('payee')

        # If this is not an update or payee is being updated,
        # get or create the payee instance matching the name given.
        if not self.instance or payee is not None:
            payee, created = Payee.objects.get_or_create(
                name=payee,
                owner=self.context['request'].user,
            )
            validated_data['payee'] = payee

    class Meta:
        model = Transaction
        fields = (
            'url', 'pk', 'amount', 'budget_category', 'date', 'inflow',
            'payee',
        )
        list_serializer_class = DictSerializer


class BudgetCategoryGroupListSerializer(DictSerializer):
    dict_key = 'name'


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
        list_serializer_class = BudgetCategoryGroupListSerializer


class BudgetSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='budgetapp:budget-detail')
    owner = owner_field
    budget_category_groups = BudgetCategoryGroupSerializer(
        many=True,
        read_only=True
    )
    budget_categories = serializers.SerializerMethodField()
    transactions = serializers.SerializerMethodField()

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
        transactions = Transaction.objects.filter(
            budget_category__group__budget__pk=budget.pk)
        serializer = TransactionSerializer(
            transactions,
            many=True,
            context={'request': self.context['request']}
        )
        return serializer.data

    class Meta:
        model = Budget
        fields = (
            'url', 'pk', 'owner', 'month', 'year', 'budget_category_groups',
            'budget_categories', 'transactions',
        )


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
