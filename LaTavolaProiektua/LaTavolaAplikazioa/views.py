from django.shortcuts import render

# Create your views here.
def ikasle_list(request):
    return render(request, 'latavola.html', {})