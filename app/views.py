from django.shortcuts import render

def index_page(request):
    content = {}
    
    return render(request, 'index.html', content)
    