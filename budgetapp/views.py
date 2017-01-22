from django.shortcuts import render
from django.http import HttpResponse

def test_view(request):
	return HttpResponse("This is the test page")