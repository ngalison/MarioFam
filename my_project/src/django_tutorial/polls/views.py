# -*- coding: utf-8 -*-
from django.http import HttpResponse

# Create your views here.

def index(request):
	return HttpResponse("MarioFam <3")
