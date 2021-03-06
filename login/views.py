from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
# Create your views here.
from .models import *
from .forms import OrderForm
from .filters import OrderFilter
