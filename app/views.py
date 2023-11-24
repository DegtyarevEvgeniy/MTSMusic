from django.shortcuts import render

def index_page(request):
    content = {}
    content['server'] = {'time': 12}
    return render(request, 'index.html', content)
    