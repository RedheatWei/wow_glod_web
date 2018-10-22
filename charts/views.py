from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from charts.models import WowGlodPrice
import json
import time

points_list = [12, 24, 36, 48, 60]
hours_list = [0.5, 1, 3, 6, 12, 24]


class MainChart(View):
    def get(self, request):
        return render(request, 'charts/mainchar.html', {'points_list': points_list, "hours_list": hours_list,"count_days":points_list[0]*hours_list[0]/24})

    def post(self, request):
        pass


class MainChartApi(View):
    def get(self, request):
        points = request.GET.get('points')
        hours = request.GET.get('hours')
        try:
            points = int(points)
        except ValueError:
            points = 0
        try:
            hours = int(hours)
        except ValueError:
            hours = 0
        if points not in points_list:
            points = points_list[0]
        if hours not in hours_list:
            hours = hours_list[0]
        time_interval = create_timestrap(points, hours * 3600)
        max_glod_price_obj = [WowGlodPrice.objects.filter(push_timestrap__range=(interval[1], interval[0])).order_by(
            '-unit_price').first() for interval in time_interval]
        min_glod_price_obj = [
            WowGlodPrice.objects.filter(push_timestrap__range=(interval[1], interval[0])).order_by('unit_price').first()
            for interval in time_interval]
        max_data = max_min_struct_change(max_glod_price_obj)
        min_data = max_min_struct_change(min_glod_price_obj)
        avg_data = avg_struct_change(time_interval)
        max_data.reverse()
        min_data.reverse()
        avg_data.reverse()
        return JsonResponse({"main_data": {"max_data": max_data, "min_data": min_data, "avg_data": avg_data}})

    def post(self, request):
        pass


def create_timestrap(count=24, interval=3600):
    now_time = time.time()
    return [(now_time - interval * i, now_time - interval * (i + 1)) for i in range(count)]


def max_min_struct_change(all_data):
    base_struct = [f.name for f in WowGlodPrice._meta.get_fields()]
    main_data = []
    for data in all_data:
        single_data = {}
        for base in base_struct:
            single_data[base] = getattr(data, base, None)
        main_data.append(single_data)
    return main_data


def avg_struct_change(time_interval):
    all_data = []
    for interval in time_interval:
        interval_data = WowGlodPrice.objects.filter(push_timestrap__range=(interval[1], interval[0])).order_by(
            '-unit_price').all()
        unit_price = [data.unit_price for data in interval_data]
        if unit_price:
            avg_unit_price = sum(unit_price) / len(unit_price)
            push_timestrap = sum(interval) / 2
        else:
            avg_unit_price = None
            push_timestrap = None
        all_data.append({'avg_unit_price': avg_unit_price, "push_timestrap": push_timestrap,"count":len(unit_price)})
    return all_data
