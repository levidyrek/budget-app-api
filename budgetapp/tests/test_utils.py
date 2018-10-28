from django.contrib.auth.models import User
from django.test import TestCase

from budgetapp import models

from ..utils.permissions import is_owner_or_admin


class PermissionsTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user1 = User.objects.create(
            username='user1',
            password='user1',
        )
        cls.user2 = User.objects.create(
            username='user2',
            password='user2',
        )
        cls.staff_user = User.objects.create(
            username='staff',
            password='staff',
            is_staff=True,
        )

        cls.budget1 = models.Budget.objects.create(
            month='JAN',
            year=2000,
            owner=cls.user1,
        )
        cls.group1 = models.BudgetCategoryGroup.objects.create(
            name='Group 1',
            budget=cls.budget1,
        )

    def test_is_owner_or_admin_is_owner(self):
        # Direct relationship to owner.
        self.assertTrue(is_owner_or_admin(self.user1, self.budget1))
        # Nested relationship to owner.
        self.assertTrue(is_owner_or_admin(self.user1, self.group1))

    def test_is_owner_or_admin_not_owner(self):
        # Direct relationship to owner.
        self.assertFalse(is_owner_or_admin(self.user2, self.budget1))
        # Nested relationship to owner.
        self.assertFalse(is_owner_or_admin(self.user2, self.group1))

    def test_is_owner_or_admin_is_staff(self):
        self.assertTrue(is_owner_or_admin(self.staff_user, self.budget1))

    def test_is_owner_or_admin_no_owner_attribute(self):
        with self.assertRaises(AttributeError):
            is_owner_or_admin(self.staff_user, object())
