from django import forms
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from rest_framework import generics, permissions, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Budget, BudgetCategory, BudgetCategoryGroup, Transaction
from .permissions import IsOwnerOrAdmin
from .serializers import (BudgetCategoryGroupSerializer,
                          BudgetCategorySerializer, BudgetSerializer,
                          TransactionSerializer, UserSerializer)


class OwnerMixin:
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BudgetViewSet(OwnerMixin, viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)
    filter_fields = ('month', 'year',)

    def get_queryset(self):
        return Budget.objects.filter(owner=self.request.user)


class CopyBudgetForm(forms.Form):
    source = forms.ModelChoiceField(
        queryset=Budget.objects.all(), required=False)
    target_year = forms.IntegerField()
    target_month = forms.CharField()

    def __init__(self, request_user, *args, **kwargs):
        self.request_user = request_user
        super().__init__(*args, **kwargs)

    def clean_source(self):
        source = self.cleaned_data['source']
        if source and source.owner != self.request_user:
            raise forms.ValidationError(
                'You cannot copy another user\'s budget.'
            )

        return source


class CopyBudgetView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        form = CopyBudgetForm(request.user, request.data)
        if form.is_valid():
            params = form.cleaned_data
            self.copy_budget(
                params['target_year'],
                params['target_month'],
                request.user,
                params.get('source'),
            )
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

    def copy_budget(self, target_year, target_month, user, source=None):
        target, created = Budget.objects.get_or_create(
            year=target_year,
            month=target_month,
            owner=user,
        )

        # Default the source to the previous month's budget.
        if not source:
            source = target.previous

        # If there is a source budget, copy the categories. Otherwise,
        # delete all categories, since the non-existing budget appears blank
        # in the UI.
        if source:
            target.copy_categories(source)
        else:
            target.delete_categories()


class BudgetCategoryGroupViewSet(viewsets.ModelViewSet):
    queryset = BudgetCategoryGroup.objects.all()
    serializer_class = BudgetCategoryGroupSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)

    def get_queryset(self):
        return BudgetCategoryGroup.objects.filter(
            budget__owner=self.request.user)


class BudgetCategoryViewSet(viewsets.ModelViewSet):
    queryset = BudgetCategory.objects.all()
    serializer_class = BudgetCategorySerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)

    def get_queryset(self):
        return BudgetCategory.objects.filter(
            group__budget__owner=self.request.user)


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin)

    def get_queryset(self):
        return Transaction.objects.filter(
            budget_category__group__budget__owner=self.request.user)


class UserCreateView(generics.CreateAPIView):
    """
    Used to create a user. Anonymous users can use this.
    TODO: Prevent automated usage of this view
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Actions an authenticated user can do only to their own User
    object (Retrieve, Update, Destroy).
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrAdmin,)


class UserListView(generics.ListAPIView):
    """
    List view for Users. Only admin users can use this.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)


class ObtainAuthTokenCookieView(ObtainAuthToken):
    """
    Custom auth token view that returns the token in a response,
    and also saves the token as an HTTP-only cookie on the client.
    """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user_data = UserSerializer(user, context={'request': request})
        response = JsonResponse(user_data.data)
        response.set_cookie(
            'Token',
            token.key,
            max_age=60*60*24*14,  # Two weeks.
            httponly=True
        )
        return response


class UserDetailView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data)


def logout(request):
    """
    Sets an expired cookie on the client, logging the user out.
    """
    response = HttpResponse()
    response.set_cookie(
        key='Token',
        value='logout',
        max_age=0,
        expires='Wed, 21 Oct 1900 07:28:00 GMT',
        httponly=True
    )
    return response
