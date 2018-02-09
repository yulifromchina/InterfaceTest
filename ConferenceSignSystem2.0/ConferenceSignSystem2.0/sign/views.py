from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event,Guest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render,get_object_or_404

# Create your views here.


# 首页
def index(request):
    return render(request, 'index.html')


# 登陆动作
# 认证方式是HTTP basic认证，把用户名和密码保存在session中
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('paassword','')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)  # Log in
            request.session['user'] = username  # 将session记录到服务端
            response = HttpResponseRedirect('/event_manage/')
            return response
        else:
            return render(request, 'index.html', {'error':'username or password error'})


@login_required
def event_manage(request):
    username = request.session.get('user','')  # 如果用户是登陆状态，就从session中取出username
    event_list = Event.objects.all()
    paginator = Paginator(event_list, 5)   # 每页显示5条
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver first page
        contacts = paginator.page(1)
    except EmptyPage:
        # if page is out of range, deliver last page
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'event_manage.html',{'user':username,'events':contacts})


@login_required
def search_event_name(request):
    username = request.session.get('user','')
    search_name = request.GET.get('name','')
    event_list = Event.objects.filter(name__contains=search_name)  # 通过模糊匹配查询发布会的列表
    paginator = Paginator(event_list, 5)   # 每页显示5条
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver first page
        contacts = paginator.page(1)
    except EmptyPage:
        # if page is out of range, deliver last page
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'event_manage.html',{'user':username,'events':contacts,'search_name':search_name})



@login_required
def guest_manage(request):
    username = request.session.get('user', '')
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list, 5)   # 每页显示5条
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver first page
        contacts = paginator.page(1)
    except EmptyPage:
        # if page is out of range, deliver last page
        contacts = paginator.page(paginator.num_pages)
    return render(request,'guest_manage.html',{'user':username,'guests':contacts})


@login_required
def search_guest_name(request):
    username = request.session.get('user','')
    search_name = request.GET.get('name','')
    guest_list = Guest.objects.filter(realname__contains=search_name)  # 通过模糊匹配查询嘉宾
    paginator = Paginator(guest_list, 5)   # 每页显示5条
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver first page
        contacts = paginator.page(1)
    except EmptyPage:
        # if page is out of range, deliver last page
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'guest_manage.html',{'user':username,'guests':contacts,'search_name':search_name})


@login_required
def sign_index(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'sign_index.html',{'event':event})



@login_required
def sign_index_action(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    phone = request.POST.get('phone','')
    sum = Guest.objects.filter(id=event_id).count()
    signed=Guest.objects.filter(id=event_id).filter(sign=1).count()


    # 在数据库中用手机号查询
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign_index.html',{'event':event,'hint':'phone error','sum':sum,'signed':signed})

    # 在数据库中用手机号和发布会查询，确定唯一的嘉宾
    result = Guest.objects.filter(phone=phone,event_id=event_id)
    if not result:
        return render(request, 'sign_index.html',{'event':event,'hint':'event id or phone error','sum':sum,'signed':signed})

    # 获取可操作的对象
    result = Guest.objects.get(phone=phone, event_id=event_id)
    if result.sign:  # 如果已经签到则返回
        return render(request, 'sign_index.html', {'event':event,'hint':'user has sign in','guest':result,'sum':sum,'signed':signed})

    else:
        Guest.objects.filter(phone=phone, event_id=event_id).update(sign='1')
        return render(request,'sign_index.html', {'event':event, 'hint':'sign in success','guest':result,'sum':sum,'signed':signed})


@login_required
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect('/index/')   # 退出登陆后重定向到用户登陆页面
    return response


