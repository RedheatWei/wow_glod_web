from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from charts.models import WowGlodPrice
import json
import time

class MainChart(View):
    def get(self, request):
        return render(request,'charts/mainchar.html')
    def post(self,request):
       pass

class MainChartApi(View):
    def get(self, request):
        time_interval = create_timestrap()
        glod_price_obj = get_min_unit(time_interval)
        data = create_data(glod_price_obj)
        return JsonResponse(data)
    def post(self,request):
       pass

def create_timestrap(count=24,interval=3600):
    now_time = time.time()
    return [(now_time-interval*i,now_time-interval*(i+1)) for i in range(count)]

def get_min_unit(time_interval):
    glod_price_obj = []
    for interval in time_interval:
        glod_price_obj.append(WowGlodPrice.objects.filter(push_timestrap__range=(interval[1],interval[0])).order_by('-unit_price')[:1])
    print(glod_price_obj)
    return glod_price_obj

def create_data(min_unit):
    xAxis = [min.push_timestrap for min in min_unit]
    yAxis = [min.unit_price for min in min_unit]
    return {"xAxis":xAxis,"yAxis":yAxis}