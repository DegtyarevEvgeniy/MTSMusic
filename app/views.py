from django.shortcuts import render
from django.http import HttpResponse

def index_page(request):
    content = {
        "title" : "Trigger python"
    }
    
    return render(request, "index.html", content)
    # content['server'] = {'time': 12}
    # return render(request, 'index.html', content)
def simple_func(request):
    print("\nThis is a simple function\n")
    return HttpResponse("""<html><script>alert('hello')</script></html>""")
