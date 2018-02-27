from djmoney.models.fields import MoneyField
from django.db import models
from datetime import date, datetime


class OwnedModel(models.Model):
    """
    Contains necessary fields and methods for models that are owned.
    """

    # Should be given a value in subclass with proper related_name
    owner = None

    def has_owner_conflict(self, user):
        """
        Checks to see if there is a conflict of owners based on owner param.
        Returns false if owner is not set
        :param user: The user to check against
        :return: True if there is a conflict, False otherwise
        """
        username = user.username

        # Check self
        try:
            if self.owner.username != username:
                return True
        except NameError:
            print("Owner is not set")

        # Check relationships
        for field in self._meta.get_fields():
            if isinstance(field, OwnedModel) and \
               field.has_owner_conflict(user):
                return True

        return False

    class Meta:
        abstract = True


class Budget(OwnedModel):
    related_name = 'budgets'

    MONTH_CHOICES = (
        ('JAN', 'January'),
        ('FEB', 'February'),
        ('MAR', 'March'),
        ('APR', 'April'),
        ('MAY', 'May'),
        ('JUN', 'June'),
        ('JUL', 'July'),
        ('AUG', 'August'),
        ('SEP', 'September'),
        ('OCT', 'October'),
        ('NOV', 'November'),
        ('DEC', 'December')
    )

    YEAR_CHOICES = []
    for r in range(2000, (datetime.now().year + 1)):
        YEAR_CHOICES.append((r, r))

    month = models.CharField(
        max_length=100,
        choices=MONTH_CHOICES,
        default='JAN',
    )
    year = models.IntegerField(
        choices=YEAR_CHOICES,
        default=datetime.now().year
    )
    owner = models.ForeignKey('auth.User', related_name=related_name)

    class Meta:
        unique_together = ('owner', 'month', 'year')

    def __str__(self):
        return self.owner.username + \
               '\'s ' + \
               str(self.month) + \
               ' ' + \
               str(self.year) + \
               ' Budget'


class BudgetCategoryGroup(OwnedModel):
    related_name = 'budget_category_groups'
    owner = models.ForeignKey('auth.User', related_name=related_name)
    name = models.CharField(max_length=100)
    budget = models.ForeignKey(Budget,
                               on_delete=models.CASCADE,
                               related_name=related_name)

    class Meta:
        unique_together = ('owner', 'name', 'budget')

    def __str__(self):
        return self.name + ' [owner=' + self.owner.username + ']'


class BudgetCategory(OwnedModel):
    related_name = 'budget_categories'
    owner = models.ForeignKey('auth.User', related_name=related_name)
    category = models.CharField(max_length=100)
    group = models.ForeignKey(BudgetCategoryGroup,
                              on_delete=models.CASCADE,
                              related_name=related_name)
    limit = MoneyField(max_digits=10,
                       decimal_places=2,
                       default=0,
                       default_currency='USD')
    spent = MoneyField(max_digits=10,
                       decimal_places=2,
                       default=0,
                       default_currency='USD')

    class Meta:
        unique_together = ('owner', 'category', 'group',)

    def get_money_left(self):
        return self.limit - self.spent

    def __str__(self):
        return str(self.category) + ' ' + \
               self.group.budget.month + ' ' + \
               str(self.group.budget.year) + \
               ' [owner=' + self.owner.username + ']'


class Transaction(OwnedModel):
    related_name = 'transactions'
    owner = models.ForeignKey('auth.User', related_name=related_name)
    amount = MoneyField(max_digits=10,
                        decimal_places=2,
                        default_currency='USD')
    recipient = models.CharField(max_length=100)
    budget_category = models.ForeignKey(BudgetCategory,
                                        on_delete=models.CASCADE,
                                        related_name=related_name)
    date = models.DateField()

    def __str__(self):
        return str(self.amount) + ' ' \
               + self.recipient + ' ' \
               + str(self.budget_category) + ' ' \
               + str(self.date)


class Income(OwnedModel):
    related_name = 'incomes'
    owner = models.ForeignKey('auth.User', related_name=related_name)
    name = models.CharField(max_length=100)
    amount = MoneyField(max_digits=10,
                        decimal_places=2,
                        default_currency='USD')
    budget = models.ForeignKey(Budget,
                               on_delete=models.CASCADE,
                               related_name=related_name)

    def __str__(self):
        return self.name + ': ' + str(self.amount)


class Goal(OwnedModel):
    name = models.CharField(max_length=100)
    goal_amount = MoneyField(max_digits=10,
                             decimal_places=2,
                             default_currency='USD')
    progress = MoneyField(max_digits=10,
                          decimal_places=2,
                          default=0,
                          default_currency='USD')

    def is_met(self):
        return self.progress >= self.goal_amount

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class LongTermGoal(Goal):
    related_name = 'long_term_goals'
    due_date = models.DateField()
    owner = models.ForeignKey('auth.User', related_name=related_name)

    def is_past_due(self):
        return date.today() > self.due_date


class BudgetGoal(Goal):
    related_name = 'budget_goals'
    owner = models.ForeignKey('auth.User', related_name=related_name)
    budget = models.ForeignKey(Budget,
                               on_delete=models.CASCADE,
                               related_name=related_name)
    long_term_goal = models.ForeignKey(LongTermGoal,
                                       on_delete=models.CASCADE,
                                       null=True,
                                       related_name=related_name)

    class Meta:
        unique_together = ('owner', 'budget', 'long_term_goal',)
