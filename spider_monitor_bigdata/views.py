# -*- coding: utf-8 -*-
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from . import search_data, excel
from django import forms
import xlwt
import time
import json
import os
import StringIO
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class UserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


# 登录
def login(request):
    message = ''
    if request.method == "POST":
        uf = UserForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            is_ok = search_data.check_name_pass(username, password)
            if is_ok:
                request.session['username'] = username
                return HttpResponseRedirect('/index')
            else:
                message = u"账号密码不正确!"
    else:
        uf = UserForm()
    return render_to_response('login.html', {'message': message})


# 登出
def Logout(request):
    request.session.flush()
    return HttpResponseRedirect('/login')


# 主页面
def home(request):
    if request.session.get('username'):
        times = request.GET.get("time") or time.strftime('%Y-%m-%d', time.localtime(time.time()))
        search = request.GET.get("search") or ''
        context = {}
        return render(request, 'index.html', context)
    else:
        return HttpResponseRedirect('/login')


# 首页信息
def index(request):
    if request.session.get('username'):
        context = {}
        db_list = {
            "seventeen_zwd": ["shop_message", "chuzu_message_2", "daifa_list", "station_message"],
            # "soubu": ["shop_info_mess", "product_list"],
            "soubu_app": ["product_info", "product_list", "shop_info_message"],
            "sf_fy": ["company_name", "qiye_name2"]
        }
        # 表结构改变
        # db_list2 = [
        #     {
        #         "seventeen_zwd": ["shop_message", "chuzu_message_2", "daifa_list", "station_message"]
        #     },
        #     {
        #         "soubu_app": ["product_info", "product_list", "shop_info_message"],
        #     },
        #     {
        #         "sf_fy": ["company_name", "qiye_name2"]
        #     }
        # ]
        search = request.GET.get("search") or ""

        db_lists = db_list.keys()
        db_name = request.GET.get("db_name") or db_lists[0]
        table_name = request.GET.get("table_name") or db_list[db_name][0]
        page = request.GET.get("page") or 1
        context["db_list"] = db_lists
        context["table_name_list"] = db_list[db_name]
        context["table_list"] = search_data.get_db_message(db_name, table_name, search, page)
        context["table_th_list"] = context["table_list"][0].keys()
        context["select_list"] = search_data.get_db_message(db_name, table_name, "", page)[0].keys()
        table_lists = []
        for i in context["table_list"]:
            tmp = []
            for j in i:
                tmp.append(i[j])
            table_lists.append(tmp)
        context["table_lists"] = table_lists
        context["db_name"] = db_name
        context["table_name"] = table_name
        context["page"] = page
        context["totalSize"] = search_data.get_db_num(db_name, table_name)
        context["totalPage"] = int(context["totalSize"]) / 10 + 1
        return render(request, 'index.html', context)
    else:
        return HttpResponseRedirect('/login')


def index2(request):
    return render_to_response('index2.html')


def index3(request):
    context = {}
    context["wordClouds"] = search_data.get_word_clouds()
    context["result"] = search_data.time_tongji()
    return render(request, 'index3.html', context)

def chatbot(request):
    return render(request, 'chatbot.html')

def chatwithme(request):
    question = request.GET.get("question") or ""
    result = search_data.chat_with_me(question)
    return JsonResponse(result)

def get_tongji(request):
    result = search_data.date_tongji()
    return JsonResponse(result)


def get_jiage(request):
    result = search_data.get_jiage_tongji()
    return JsonResponse(result)


def excel_export(request):
    db_name = request.GET.get("db_name")
    table_name = request.GET.get("table_name")
    page = request.GET.get("page") or 1
    search = request.GET.get("search") or ""
    datalist = search_data.get_db_message(db_name, table_name, search, page, page_size=5000)
    title_list = datalist[0].keys()
    # 设置HttpResponse的类型
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename=' + table_name + '.xls'
    # new一个文件
    wb = xlwt.Workbook(encoding='utf-8')
    # new一个sheet
    sheet = wb.add_sheet(u'人员表单')
    # 维护一些样式， style_heading, style_body, style_red, style_green
    style_heading = xlwt.easyxf("""
            font:
                name Arial,
                colour_index white,
                bold on,
                height 0xA0;
            align:
                wrap off,
                vert center,
                horiz center;
            pattern:
                pattern solid,
                fore-colour 0x19;
            borders:
                left THIN,
                right THIN,
                top THIN,
                bottom THIN;
            """
                                )
    style_body = xlwt.easyxf("""
            font:
                name Arial,
                bold off,
                height 0XA0;
            align:
                wrap on,
                vert center,
                horiz left;
            borders:
                left THIN,
                right THIN,
                top THIN,
                bottom THIN;
            """
                             )
    style_green = xlwt.easyxf(" pattern: pattern solid,fore-colour 0x11;")
    style_red = xlwt.easyxf(" pattern: pattern solid,fore-colour 0x0A;")
    fmts = [
        'M/D/YY',
        'D-MMM-YY',
        'D-MMM',
        'MMM-YY',
        'h:mm AM/PM',
        'h:mm:ss AM/PM',
        'h:mm',
        'h:mm:ss',
        'M/D/YY h:mm',
        'mm:ss',
        '[h]:mm:ss',
        'mm:ss.0',
    ]
    style_body.num_format_str = fmts[0]
    # 写标题栏
    for i in xrange(0, len(title_list), 1):
        sheet.write(0, i, title_list[i], style_heading)
    DownLoadFileList = datalist
    # 写数据
    row = 1
    for usa in DownLoadFileList:
        for j in xrange(0, len(title_list), 1):
            sheet.write(row, j, str(usa[title_list[j]]), style_body)
        row = row + 1

        # 写出到IO
    output = StringIO.StringIO()
    wb.save(output)
    # 重新定位到开始
    output.seek(0)
    response.write(output.getvalue())
    return response


def form(request):
    return render_to_response('form.html')


def form_advanced(request):
    return render_to_response('form_advanced.html')


def form_validation(request):
    return render_to_response('form_validation.html')


def form_wizards(request):
    return render_to_response('form_wizards.html')


def form_upload(request):
    return render_to_response('form_upload.html')


def form_buttons(request):
    return render_to_response('form_buttons.html')


def general_elements(request):
    return render_to_response('general_elements.html')


def media_gallery(request):
    return render_to_response('media_gallery.html')


def typography(request):
    return render_to_response('typography.html')


def icons(request):
    return render_to_response('icons.html')


def glyphicons(request):
    return render_to_response('glyphicons.html')


def widgets(request):
    return render_to_response('widgets.html')


def invoice(request):
    return render_to_response('invoice.html')


def inbox(request):
    return render_to_response('inbox.html')


def calendar(request):
    return render_to_response('calendar.html')


def tables(request):
    search = request.GET.get("search") or ''
    context = {}
    context['shop_lists'] = search_data.get_shop_message(search)
    context['daifa_lists'] = search_data.get_daifa_list(search)
    context['chuzu_lists'] = search_data.get_chuzu_list(search)
    context['username'] = request.session['username']
    return render(request, 'tables.html', context)


def tables_dynamic(request):
    return render_to_response('tables_dynamic.html')


def fixed_sidebar(request):
    return render_to_response('fixed_sidebar.html')


def upload_file(request):
    if request.method == 'POST':
        ret = {'status': False, 'data': None, 'error': None}
        try:
            # user = request.POST.get('user')
            img = request.FILES.get('img')
            f = open(os.path.join('static/images', img.name), 'wb')
            for chunk in img.chunks(chunk_size=1024):
                f.write(chunk)
            ret['status'] = True
            ret['data'] = os.path.join('static/images', img.name)
        except Exception as e:
            ret['error'] = e
        finally:
            f.close()
            return HttpResponse(json.dumps(ret))
    # return render(request, 'fixed_sidebar.html')
