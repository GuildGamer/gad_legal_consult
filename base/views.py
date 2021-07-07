from django.shortcuts import render

def home(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def experience(request):
    return render(request, "experience.html")

def service(request):
    return render(request, "service.html")
