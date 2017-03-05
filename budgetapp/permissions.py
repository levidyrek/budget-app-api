from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
	"""
	Custom permission that only allows owners of an object to view or edit it
	"""

	def has_object_permission(self, request, view, obj):
		try:
			has_permission = obj.owner == request.user
		except AttributeError:
			print("Object has no attribute 'owner'")
			has_permission = False

		return has_permission or request.user.is_staff
