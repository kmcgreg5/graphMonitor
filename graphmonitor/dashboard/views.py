from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from dashboard.models import Switches, Commands, Devices, DataPoints
from dashboard.forms import SwitchForm, CommandForm, DeviceForm
from dashboard.scheduler import Processes
from django.http import JsonResponse
from datetime import datetime

# Create your views here.
@never_cache
def dashboard(request):
    context = {}
    return render(request, "dashboard/index.html", context)


@never_cache
def all_graphs(request):
    if request.method == "POST":
        start = datetime.strptime(request.POST['start'], "%Y-%m-%d %H:%M")
        end = datetime.strptime(request.POST['end'], "%Y-%m-%d %H:%M")
        data_points = DataPoints.objects.filter(datetime__gt=start, datetime__lt=end)
        graphs = {}
        for device in Devices.objects.all():
            if data_points.filter(device=device).exists():
                graphs[device.pk] = {}
                graphs[device.pk]['title'] = f"{device.name} ({device.port})"
                graphs[device.pk]['start'] = start.timestamp()*1000
                graphs[device.pk]['end'] = end.timestamp()*1000
                graphs[device.pk]['in'] = [{'x':data.datetime.timestamp()*1000, 'y':data.bytes / 1000 / data.interval.total_seconds()} for data in data_points.filter(device=device, input=True).order_by('datetime')]
                graphs[device.pk]['out'] = [{'x':data.datetime.timestamp()*1000, 'y':data.bytes / 1000 / data.interval.total_seconds()} for data in data_points.filter(device=device, input=False).order_by('datetime')]
                
        return JsonResponse(graphs)


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
