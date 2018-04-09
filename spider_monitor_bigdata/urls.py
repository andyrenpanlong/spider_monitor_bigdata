# -*- coding: utf-8 -*-
"""spider_monitor_bigdata URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib import admin
admin.autodiscover()
from . import views
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.login),
    url(r'^Logout', views.Logout),
    url(r'^$', views.index),
    url(r'^index3', views.index3),
    url(r'^index2', views.index2),
    url(r'^index', views.index),
    url(r'^home', views.home),
    url(r'^form', views.form),
    url(r'^form_advanced', views.form_advanced),
    url(r'^form_validation', views.form_validation),
    url(r'^form_wizards', views.form_wizards),
    url(r'^form_upload', views.form_upload),
    url(r'^form_buttons', views.form_buttons),
    url(r'^general_elements', views.general_elements),
    url(r'^media_gallery', views.media_gallery),
    url(r'^typography', views.typography),
    url(r'^icons', views.icons),
    url(r'^glyphicons', views.glyphicons),
    url(r'^widgets', views.widgets),
    url(r'^invoice', views.invoice),
    url(r'^inbox', views.inbox),
    url(r'^calendar', views.calendar),
    url(r'^tables', views.tables),
    url(r'^tables_dynamic', views.tables_dynamic),
    url(r'^fixed_sidebar', views.fixed_sidebar),
    url(r'^upload_file', views.upload_file),

    # 接口
    url(r'^get_tongji', views.get_tongji),
    url(r'^get_jiage', views.get_jiage),
    url(r'^export', views.excel_export),

    # 聊天机器人
    url(r'^chatbot', views.chatbot),
    url(r'^chatwithme', views.chatwithme),
]
