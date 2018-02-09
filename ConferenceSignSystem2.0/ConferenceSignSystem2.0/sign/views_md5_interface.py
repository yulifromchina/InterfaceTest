# 接口使用md5进行认证,以及超时拒绝请求
# 系统的web接口，为其他开发者调用
# 包括：
# 发布会添加接口
# 发布会查询接口
# 嘉宾添加接口
# 嘉宾查询接口
# 嘉宾签到接口

from django.http import JsonResponse
from sign.models import Event,Guest
from django.core.exceptions import ValidationError,ObjectDoesNotExist
from django.db.utils import IntegrityError
import time
import hashlib


# 超时检查
def timeout_check(request):
    if request.method == 'POST':
        client_time = request.POST.get('time','')
    else:
        client_time = request.GET.get('time','')

    if client_time == '':
        return JsonResponse({'status': 10031, 'message': 'time null'})

    # 服务器时间
    now_time = time.time()
    server_time = str(now_time).split('.')[0]
    #获取时间差
    time_difference = int(server_time) - int(client_time)
    if time_difference>=60:
        return JsonResponse({'status': 10032, 'message': 'time out'})
    return ''


# 签名检查
def sign_check(request, secret_key='&cfssystem'):
    if request.method == 'POST':
        client_sign = request.POST.get('sign','')
        client_time = request.POST.get('time','')
    else:
        client_sign = request.GET.get('sign','')
        client_time = request.GET.get('time','')

    if client_sign == ''or client_time=='':
        return JsonResponse({'status': 10033, 'message': 'sign null'})

    md5 = hashlib.md5()
    sign_str = client_time+ secret_key
    sign_bytes_utf8 = sign_str.encode(encoding='utf8')
    md5.update(sign_bytes_utf8)
    server_sign = md5.hexdigest()
    if server_sign != client_sign:
        return JsonResponse({'status': 10034, 'message': 'sign error'})
    return ''


# 发布会添加接口
def add_event_with_md5(request):

    # 超时检查
    result = timeout_check(request)
    if result!='':
        return result

    # 签名检查
    result = sign_check(request)
    if result!='':
        return result

    eid = request.POST.get('eid','')                      # 发布会id
    name = request.POST.get('name','')                    # 发布会名称
    limit = request.POST.get('limit','')                  # 限制人数
    status = request.POST.get('status','')                # 状态
    address = request.POST.get('address','')              # 地址
    start_time = request.POST.get('start_time','')        # 发布时间


    # 如果以下几项有任何一项为空
    if eid=='' or name=='' or limit=='' or address=='' or start_time=='':
        return JsonResponse({'status':10001,'message':'parameter error'})

    # 如果eid已经存在
    result = Event.objects.filter(id=eid)
    if result:
        return JsonResponse({'status':10002,'message':'event id already exists'})

    # 如果name已经存在
    result = Event.objects.filter(name=name)
    if result:
        return JsonResponse({'status':10003,'message':'event name already exists'})

    # 如果未设置状态，就设置为1
    if status=='':
        status = 1

    # 如果日期格式错误
    try:
        Event.objects.create(id=eid,name=name,limit=limit,address=address,status=int(status),start_time=start_time)
    except ValidationError as e:
        error = 'start_time format error, It must be YYYY-MM-DD HH:MM:SS foramt'
        return JsonResponse({'status':10004,'message':error})

    # 返回添加成功
    return JsonResponse({'status':200,'message':'add event success'})


# 发布会查询接口
def get_event_list_with_md5(request):

    # 超时检查
    result = timeout_check(request)
    if result!='':
        return result

    # 签名检查
    result = sign_check(request)
    if result!='':
        return result

    eid = request.GET.get('eid','')           # 发布会id
    name = request.GET.get('name','')         # 发布会名称

    # 如果eid和name同时为空
    if eid=='' and name=='':
        return JsonResponse({'status':10001,'message':'parameter error'})

    # 如果eid不为空，返回对应的唯一发布会
    if eid !='':
        event = {}
        try:
            result = Event.objects.get(id=eid)
        except ObjectDoesNotExist:
            return JsonResponse({'status':10005,'message':'query result is empty'})
        else:
            event['name'] = result.name
            event['limit'] = result.limit
            event['status'] = result.status
            event['address'] = result.address
            event['start_time'] = result.start_time
            return JsonResponse({'status':200,'message':'success','data':event})

    # 如果eid为空，name不为空，同名的发布会可能有多场，返回一个列表
    if name != '':
        datas = []
        results = Event.objects.filter(name__contains=name)  # 模糊查询
        if results:
            for r in results:
                event = {}
                event['name'] = r.name
                event['limit'] = r.limit
                event['status'] = r.status
                event['address'] = r.address
                event['start_time'] = r.start_time
                datas.append(event)
            return JsonResponse({'status':200,'message':'success','data':datas})
        else:
            return JsonResponse({'status':10005,'message':'query result is empty'})


# 嘉宾添加接口
def add_guest_with_md5(request):

    # 超时检查
    result = timeout_check(request)
    if result!='':
        return result

    # 签名检查
    result = sign_check(request)
    if result!='':
        return result

    eid = request.POST.get('eid','')             # 关联发布会id
    realname = request.POST.get('realname','')   # 姓名
    phone = request.POST.get('phone','')         # 手机号
    email = request.POST.get('email','')         # 邮箱

    # 以下几项不能为空
    if eid=='' or realname == '' or phone=='':
        return JsonResponse({'status':10001,'message':'parameter error'})

    # 如果关联的eid为空
    result = Event.objects.filter(id=eid)  # filter是返回一个对象列表
    if not result:
        return JsonResponse({'status':10006,'message':'event id null'})

    # 如果获取不到发布会是否开启，则不能添加
    result = Event.objects.get(id=eid).status   # get是返回一个对象
    if not result:
        return JsonResponse({'status':10007,'message':'event status is not available'})

    # 如果发布会人数已满，则不能添加
    event_limit = Event.objects.get(id=eid).limit                   # 发布会限制人数
    guest_limit = Guest.objects.filter(event_id=eid)                # 发布会已添加的嘉宾列表
    if len(guest_limit) >= event_limit:
        return JsonResponse({'status':10008,'message':'event number is full'})


    # 如果发布会已经开始，也不能添加
    # 发布会时间
    event_time = Event.objects.get(id=eid).start_time
    etime = str(event_time).split('+')[0]  # 数据库中DateTimeField字段会带有小数点
    timeArray = time.strptime(etime, "%Y-%m-%d %H:%M:%S")  # timeArray是表示时间的结构体
    e_time = int(time.mktime(timeArray))  # 转化为unix时间戳

    # 当前时间
    now_time = str(time.time())
    ntime = now_time.split('.')[0]
    ntime = int(ntime)

    if ntime > e_time:
        return JsonResponse({'status':10009,'message':'event has started'})


    # 外键检查失败，或外键重复，会导致IntegrityError抛出
    try:
        Guest.objects.create(realname=realname,phone=int(phone),email=email,sign=0,event_id=int(eid))
    except IntegrityError:
        return JsonResponse({'status':10010,'message':'the event guest phone number repeat'})

    return JsonResponse({'status':200,'message':'add guest success'})


# 嘉宾查询接口
def get_guest_list_with_md5(request):

    # 超时检查
    result = timeout_check(request)
    if result!='':
        return result

    # 签名检查
    result = sign_check(request)
    if result!='':
        return result

    eid = request.GET.get('eid','')          # 关联发布会Id
    phone = request.GET.get('phone','')      # 嘉宾手机号

    # 关联发布会id为空，返回失败
    if eid=='':
        return JsonResponse({'status':10006,'message':'event id null'})

    # 关联发布会id不为空，手机号为空，返回该发布会的所有嘉宾
    if eid!='' and phone=='':
        datas=[]
        results = Guest.objects.filter(event_id=eid)
        if results:
            for r in results:
                guest = {}
                guest['realname'] = r.realname
                guest['phone'] = r.phone
                guest['email'] = r.email
                guest['sign'] = r.sign
                datas.append(guest)
            return JsonResponse({'status':200,'message':'success','data':datas})
        else:
            return JsonResponse({'status':10005,'message':'query result is empty'})

    # 如果eid和phone都不为空，通过联合主键来查找
    if eid!='' and phone !='':
        guest = {}
        try:
            result = Guest.objects.get(phone=phone,event_id=eid)
        except ObjectDoesNotExist:
            return JsonResponse({'status':10005,'message':'query result is empty'})
        else:
            guest['realname'] = result.realname
            guest['phone'] = result.phone
            guest['email'] = result.email
            guest['sign'] = result.sign
            return JsonResponse({'status':200,'message':'success','data':guest})


# 嘉宾签到接口
def user_sign_with_md5(request):

    # 超时检查
    result = timeout_check(request)
    if result!='':
        return result

    # 签名检查
    result = sign_check(request)
    if result!='':
        return result

    eid = request.POST.get('eid','')                  # 发布会id
    phone = request.POST.get('phone','')              # 嘉宾手机号

    # eid和phone均不能为空
    if eid=='' and phone=='':
        return JsonResponse({'status':10001,'message':'parameter error'})

    # 查找签到的发布会
    result = Event.objects.filter(id=eid)
    if not result:
        return JsonResponse({'status':10006,'message':'event id null'})

    result = Event.objects.get(id=eid).status
    if not result:
        return JsonResponse({'status':10007,'message':'event status is not available'})

    # 如果发布会已经开始，也不能签到
    # 发布会时间
    event_time = Event.objects.get(id=eid).start_time
    etime = str(event_time).split('+')[0]  # 数据库中DateTimeField字段会带有小数点
    timeArray = time.strptime(etime, "%Y-%m-%d %H:%M:%S")  # timeArray是表示时间的结构体
    e_time = int(time.mktime(timeArray))  # 转化为unix时间戳

    # 当前时间
    now_time = str(time.time())
    ntime = now_time.split('.')[0]
    ntime = int(ntime)

    if ntime > e_time:
        return JsonResponse({'status':10009,'message':'event has started'})

    # 未查询到手机号
    result = Guest.objects.filter(phone=phone)
    if not result:
        return JsonResponse({'status':10010,'message':'user phone null'})

    # 通过联合主键查询
    result = Guest.objects.filter(event_id=eid, phone=phone)
    if not result:
        return JsonResponse({'status':10011,'message':'user did not participate in the conference'})

    # 已签到也返回失败
    result = Guest.objects.get(event_id=eid, phone=phone).sign
    if result:
        return JsonResponse({'status':10012,'message':'user has sign in'})
    else:
        Guest.objects.filter(event_id=eid, phone=phone).update(sign='1')
        return JsonResponse({'status':200,'message':'sign success'})