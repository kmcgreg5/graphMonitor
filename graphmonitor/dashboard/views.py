from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from dashboard.models import Switches, Commands, Devices, DataPoints
from dashboard.forms import SwitchForm, CommandForm, DeviceForm
from dashboard.scheduler import Processes
from django.http import JsonResponse, HttpResponseNotFound, HttpResponse
from datetime import datetime

# Create your views here.
@never_cache
def dashboard(request):
    context = {}
    context['switches'] = {switch:[device.pk for device in Devices.objects.filter(switch=switch).order_by('name')] for switch in Switches.objects.all().order_by('name')}
    context['poll_status'] = {switch.pk:Processes.isProcessRunning(switch.pk) for switch in Switches.objects.all().order_by('name')}
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
    
    return HttpResponseNotFound("This path does not support GET requests.")


@never_cache
def get_switch_commands(request, pk):
    if request.method == "GET":
        switch = Switches.objects.get(pk=pk)
        response = {'commands': {str(command):command.pk for command in Commands.objects.filter(switch=switch).order_by('priority')}}
        return JsonResponse(response)

    return HttpResponseNotFound("This path does not support POST requests.")


def delete_switch(request, pk):
    if request.method == "GET":
        Switches.objects.get(pk=pk).delete()
        return HttpResponse('')
    
    return HttpResponseNotFound("This path does not support POST requests.")

def delete_device(request, pk):
    if request.method == "GET":
        Devices.objects.get(pk=pk).delete()
        return HttpResponse('')
    
    return HttpResponseNotFound("This path does not support POST requests.")


def start_switch(request, pk):
    if request.method == "GET":
        if Processes.startProcess(pk) is True:
            response = HttpResponse("This switch has been started.")
        else:
            response = HttpResponse("This switch is already being polled.")
            response.status_code = 409
        
        return response

    return HttpResponseNotFound("This path does not support POST requests.")


def stop_switch(request, pk):
    if request.method == "GET":
        if Processes.stopProcess(pk) is True:
            response = HttpResponse("This switch has been stopped.")
        else:
            response = HttpResponse("This switch is already stopped.")
            response.status_code = 409
        
        return response
        
    return HttpResponseNotFound("This path does not support POST requests.")


def delete_device_data(request, pk):
    if request.method == "POST":
        start = datetime.strptime(request.POST['start'], "%Y-%m-%d %H:%M")
        end = datetime.strptime(request.POST['end'], "%Y-%m-%d %H:%M")
        device = Devices.objects.get(pk=pk)
        DataPoints.objects.filter(device=device, datetime__gt=start, datetime__lt=end).delete()

        return HttpResponse("Data points deleted.")

    return HttpResponseNotFound("This path does not support GET requests.")

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
    extra_context = {'title': 'Add Device'}
    model = Devices
    form_class = DeviceForm
    success_url = "/"


class DeviceUpdateView(UpdateView):
    template_name = "form/index.html"
    extra_context = {'title': 'Update Device'}
    model = Devices
    form_class = DeviceForm
    success_url = "/"
