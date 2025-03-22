from django.shortcuts import render

# Create your views here

def create_miniature(request):
    return render(request, "create_miniature.html", {})