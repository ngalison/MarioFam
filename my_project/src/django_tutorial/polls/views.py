# -*- coding: utf-8 -*-
from django.http import HttpResponse

# Create your views here.

def index(request):
	return HttpResponse("Server is up and running")
