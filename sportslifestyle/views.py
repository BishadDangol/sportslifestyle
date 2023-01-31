from django.shortcuts import render


# Create your views here.

def index(request):
   data = {
      'name': 'sonam'
   }
   return render(request, 'index.html', data)

def about(request):
   return render(request, 'about.html')

def contact(request):
   return render(request, 'contact.html')