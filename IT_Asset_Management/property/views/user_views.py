# views/user_views.py
import csv
from django.http import HttpResponse
import pandas as pd
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from property.forms import UserForm
from property.models import Department, UserInfo


def adminuser_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        adminuser = authenticate(request, username=username, password=password)
        if adminuser is not None:
            login(request, adminuser)
            messages.success(request, "登录成功！")
            return redirect("dashboard")
        else:
            messages.error(request, "用户名或密码错误！")
    return render(request, "property/login.html")


def adminuser_logout(request):
    logout(request)
    messages.success(request, "成功登出！")
    return redirect("adminuser_login")


# def register(request):
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "注册成功！请登录。")
#             return redirect("adminuser_login")
#     else:
#         form = UserCreationForm()
#     return render(request, "property/register.html", {"form": form})


@login_required
def userinfo_list(request):
    userinfo = UserInfo.objects.all()
    return render(request, "property/userinfo_list.html", {"userinfo": userinfo})


def add_userinfo(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "用户添加成功！")
            return redirect("userinfo_list")
        else:
            messages.error(request, "表单验证失败！")
    else:
        form = UserForm()
    return render(request, "property/add_userinfo.html", {"form": form})


def manage_userinfo(request, id, action):
    userinfo = get_object_or_404(UserInfo, id=id)

    if action == "useredit":
        if request.method == "POST":
            form = UserForm(request.POST, instance=userinfo)
            if form.is_valid():
                form.save()
                messages.success(request, "用户信息已成功更新！")
                return redirect("userinfo_list")
        else:
            form = UserForm(instance=userinfo)
        return render(
            request,
            "property/manage_userinfo.html",
            {
                "form": form,
                "userinfo": userinfo,
                "action": "useredit",
                "departments": Department.objects.all(),  # 传递部门列表
            },
        )

    elif action == "delete":
        if request.method == "POST":
            userinfo.delete()
            messages.success(request, "用户已成功删除！")
            return redirect("userinfo_list")
        return render(
            request,
            "property/manage_userinfo.html",
            {
                "userinfo": userinfo,
                "action": "delete",
            },
        )

    messages.error(request, "不支持的操作。")
    return redirect("userinfo_list")


def import_userinfos(request):
    if request.method == "POST" and request.FILES.get("file"):
        file = request.FILES["file"]
        if file.name.endswith(".csv"):
            try:
                data = pd.read_csv(file)

                for index, row in data.iterrows():
                    user_name = row.get("用户名")
                    fullname = row.get("全名")
                    email = row.get("邮箱")

                    if not user_name or not fullname or not email:
                        messages.error(request, "用户名、全名和邮箱不能为空。")
                        continue

                    # 创建用户
                    UserInfo.objects.create(
                        user_name=user_name,
                        fullname=fullname,
                        email=email,
                    )
                messages.success(request, "用户导入成功！")
            except Exception as e:
                messages.error(request, f"导入失败: {str(e)}")
        else:
            messages.error(request, "请上传有效的 CSV 文件。")
    return render(request, "property/import_userinfos.html")


def export_userinfos(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="userinfos.csv"'
    writer = csv.writer(response)
    response.write("\ufeff".encode("utf-8"))
    writer.writerow(["用户名", "全名", "邮箱", "所属部门"])

    userinfos = UserInfo.objects.all().values_list("user_name", "fullname", "email",'department__dept_name')
    for user in userinfos:
        writer.writerow(user)

    return response
