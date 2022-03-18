from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from dashboard.models import Switches, Commands, Devices
from dashboard.forms import SwitchForm, CommandForm, DeviceForm
from dashboard.scheduler import Processes

# Create your views here.
@never_cache
def dashboard(request):
    context = {}
    return render(request, "base/index.html", context)


class SwitchCreateView(CreateView):
    template_name = "form/index.html"
    extra_context = {'title': 'Add Switch'}
    model = Switches
    form_class = SwitchForm
    success_url = "/"


class SwitchUpdateView(UpdateView):
    template_name = "form/index.html"
    extra_context = {'title': 'Update Switch'}
    model = Switches
    form_class = SwitchForm
    success_url = "/"


class CommandCreateView(CreateView):
    template_name = "form/index.html"
    extra_context = {'title': 'Add Command'}
    model = Commands
    form_class = CommandForm
    success_url = "/"


class CommandUpdateView(UpdateView):
    template_name = "form/index.html"
    extra_context = {'title': 'Update Command'}
    model = Commands
    form_class = CommandForm
    success_url = "/"


class DeviceCreateView(CreateView):
    template_name = "form/index.html"
    extra_context = {'title': 'Add Port'}
    model = Devices
    form_class = DeviceForm
    success_url = "/"


class DeviceUpdateView(UpdateView):
    template_name = "form/index.html"
    extra_context = {'title': 'Update Port'}
    model = Devices
    form_class = DeviceForm
    success_url = "/"
