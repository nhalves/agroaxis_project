from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def useful_items_page(request):
    return render(request, 'utils/useful_items_page.html')