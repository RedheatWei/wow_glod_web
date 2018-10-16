"""wow_glod_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include,url
from charts import views
urlpatterns = [
    url('^$', views.MainChart.as_view()),
    url('^MainChartApi/', views.MainChartApi.as_view()),
    # url('^login/', views.Login.as_view()),          #登录页面
    # url('^logout/', views.logout),                  #登出按钮
    # url('^overview/',include("overview.urls")),     #主页面app
    # url('^system/', include("system.urls")),        #系统页面app
    # url('^cmdb/', include("cmdb.urls")),            #cmdb页面app
    # url('^monsystem/', include("monsystem.urls")),  #监控配置页面
    # url('^celery/', include("celerytasks.urls")),   #任务队列
    # url('^release/', include("release.urls")),  # 业务上线
]