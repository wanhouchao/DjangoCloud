from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponseRedirect
from django.http import HttpResponse


# Create your views here.
def msgproc(request):
    datelist = []
    if request.method == "POST":
        userA = request.POST.get("userA", None)
        userB = request.POST.get("userB", None)
        msg = request.POST.get("msg", None)
        time = datetime.now()
        with open("msgdata.txt", 'a+') as f:
            f.write("{}--{}--{}--{}--\n".format(userB, userA, msg, time.strftime("%Y-%m-%d %H:%M:%S")))
    if request.method == "GET":
        userC = request.GET.get("userC", None)
        if userC != None:
            with open("msgdata.txt", "r") as f:
                cnt = 0
                for line in f:
                    cnt = cnt + 1
                    linedata = line.split("--")
                    if linedata[0] == userC:
                        d = {"userA": linedata[1], "msg": linedata[2], "time": linedata[3]}
                        datelist.append(d)
                    if cnt >= 10:
                        break

    return render(request, "CloudsLeaveMsg.html", {"data": datelist})


def index(request):
    '''登录页面'''
    return render(request, "login.html")

def Login(request):
    '''登录页面逻辑'''
    cut = False
    if request.method == "POST":
        user = request.POST.get('loginUsername', None)
        password = request.POST.get('loginPassword', None)
        with open('UserInfo.txt', 'r') as f:
            data = f.read()  # 数据类型——>|wanhouchao|123456|@
            f.close()
        datalist = data.split('@')
        for i in range(len(datalist) - 1):
            if datalist[i].split("|")[1] == user:
                if datalist[i].split("|")[2] == password:
                    cut = True
    if cut:
        return render(request, 'CloudsLeaveMsg.html')
    else:
        context = {'reminder':'用户名密码错误！！！'}
        return  render(request, 'login.html',context)


def register(request):
    return render(request,'register.html')

def RegisterSubmit(request):
    cut = False
    if request.method =='POST':
        user =request.POST.get('user', None)
        password=request.POST.get('password', None)
        # VerifyPassword=request.POST.get('VerifyPassword', None)
        mail=request.POST.get('mail', None)
        phone=request.POST.get('phone', None)
        if len(user)!=0 and password != 0:
            with open("UserInfo.txt",'a+') as f:
                data="|{}|{}|{}|{}|@".format(user,password,mail,phone)
                f.write(data)
                f.close()
            cut =True
    if cut:
        return HttpResponse('注册成功\n' + '<a href="http://127.0.0.1:8000">点击跳转到首页</a>')
    else:
        return HttpResponse('兄弟别瞎玩，注册不成功\n' + '<a href="http://127.0.0.1:8000/register/">点击跳转到注册页面</a>')
