from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from .models import Shipment, StatusHistory


def home(request):
    return render(request, "tracking/home.html")


def track_shipment(request, tracking_number):
    shipment = Shipment.objects.filter(tracking_number=tracking_number).first()
    return render(request, "tracking/track.html", {
        "shipment": shipment,
        "tracking_number": tracking_number,
    })


def basic_auth_required(view_func):
    def wrapper(request, *args, **kwargs):
        import base64
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header:
            auth_type, credentials = auth_header.split(' ', 1)
            if auth_type == 'Basic':
                decoded = base64.b64decode(credentials).decode('utf-8')
                username, password = decoded.split(':', 1)
                import os
                if username == os.environ.get('ADMIN_USER', 'admin') and \
                   password == os.environ.get('ADMIN_PASSWORD'):
                    return view_func(request, *args, **kwargs)
        response = HttpResponse('Authentication required', status=401)
        response['WWW-Authenticate'] = 'Basic realm="Admin Area"'
        return response
    return wrapper


@basic_auth_required
def admin_home(request):
    shipments = Shipment.objects.all().order_by("-created_at")
    return render(request, "tracking/admin_home.html", {"shipments": shipments})


@basic_auth_required
def admin_create(request):
    if request.method == "POST":
        shipment = Shipment.objects.create(
            origin=request.POST["origin"],
            destination=request.POST["destination"],
            carrier=request.POST.get("carrier", ""),
            current_status="Created",
        )
        StatusHistory.objects.create(shipment=shipment, status="Created", note="Shipment created")
        return redirect("admin_home")
    return render(request, "tracking/admin_create.html")


@basic_auth_required
def admin_update_status(request, tracking_number):
    shipment = get_object_or_404(Shipment, tracking_number=tracking_number)
    if request.method == "POST":
        new_status = request.POST["status"]
        note = request.POST.get("note", "")
        shipment.current_status = new_status
        shipment.save()
        StatusHistory.objects.create(shipment=shipment, status=new_status, note=note)
        return redirect("admin_home")
    return render(request, "tracking/admin_update.html", {"shipment": shipment})
