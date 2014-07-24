import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render

from app.forms import PointForm
from app.models import Station
from app.utils import pager


def index(request):

    form = PointForm()

    stations_queryset = Station.objects.all()
    stations, paginate = pager(stations_queryset, request)

    return render(request, "index.html", {
        "form": form,
        "stations": stations,
        "paginate": paginate,
    })


def check_point(request):
    form = PointForm(request.GET)
    if form.is_valid():
        data = form.cleaned_data
        points = Station.objects.find_points(data["latitude"], data["longitude"])
        points_json = [p.to_json() for p in points]
        res = {
            "result": bool(points_json),
            "points": points_json,
        }
        return HttpResponse(json.dumps(res), content_type="application/json")
    else:
        return HttpResponseBadRequest(json.dumps(form.errors), content_type="application/json")