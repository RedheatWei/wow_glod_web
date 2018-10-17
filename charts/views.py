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
        time_interval = create_timestrap(24,25200)
        glod_price_obj = get_min_unit(time_interval)
        main_data = struct_change(glod_price_obj)
        main_data.reverse()
        return JsonResponse({"data":main_data})
    def post(self,request):
       pass

def create_timestrap(count=24,interval=3600):
    now_time = time.time()
    return [(now_time-interval*i,now_time-interval*(i+1)) for i in range(count)]

def get_min_unit(time_interval):
    glod_price_obj = []
    for interval in time_interval:
        glod_price_obj.append(WowGlodPrice.objects.filter(push_timestrap__range=(interval[1],interval[0])).order_by('-unit_price').first())
    return glod_price_obj

def struct_change(all_data):
    base_struct = [f.name for f in WowGlodPrice._meta.get_fields()]
    main_data = []
    for data in all_data:
        single_data = {}
        for base in base_struct:
            single_data[base] = getattr(data,base,None)
        main_data.append(single_data)
    return main_data
