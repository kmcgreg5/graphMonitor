from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from dashboard.models import Switches

# Create your views here.
@never_cache
def dashboard(request):
    context = {}
    return render(request, "base/index.html", context)

class SwitchCreateView(CreateView):
    template_name = "form/index.html"
    model = Switches
    fields = ['name', 'address', 'username', 'password']
    success_url = "/"

class SwitchUpdateView(UpdateView):
    template_name = "form/index.html"
    model = Switches
    fields = ['name', 'address', 'username', 'password']
    success_url = "/"

class SwitchDeleteView(DeleteView):
    template_name = "form/index.html"
    model = Switches
    fields = ['name', 'address', 'username', 'password']
    success_url = "/"