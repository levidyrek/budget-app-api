from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission that only allows owners of an object to view or edit it.
    """

    def has_object_permission(self, request, view, obj):
        try:
            has_permission = obj == request.user or \
                             obj.owner == request.user
        except AttributeError:
            print("Object has no attribute 'owner'")
            has_permission = False

        return has_permission or request.user.is_staff


class BudgetCategoryGroupPermission(IsOwnerOrAdmin):

    def has_object_permission(self, request, view, obj):
        return \
            super(BudgetCategoryGroupPermission, self).has_object_permission(
                request, view, obj.budget
            )


class BudgetCategoryPermission(IsOwnerOrAdmin):

    def has_object_permission(self, request, view, obj):
        return \
            super(BudgetCategoryPermission, self).has_object_permission(
                request, view, obj.group.budget
            )


class TransactionPermission(IsOwnerOrAdmin):

    def has_object_permission(self, request, view, obj):
        return \
            super(TransactionPermission, self).has_object_permission(
                request, view, obj.budget_category.group.budget
            )


class IncomePermission(IsOwnerOrAdmin):

    def has_object_permission(self, request, view, obj):
        return \
            super(IncomePermission, self).has_object_permission(
                request, view, obj.budget
            )


class BudgetGoalPermission(IsOwnerOrAdmin):

    def has_object_permission(self, request, view, obj):
        return \
            super(BudgetGoalPermission, self).has_object_permission(
                request, view, obj.budget
            )
