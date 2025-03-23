from django.shortcuts import render

# Create your views here.

def get_handbook(request):
    return render(request, "index.html", {})