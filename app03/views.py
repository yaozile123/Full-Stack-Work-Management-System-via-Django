from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from app03.models import Account, Admin
from django import forms
from django.core.validators import RegexValidator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from utils.ModelForm import BootStrapModelForm
from utils.encrypt import md5


# Create your views here.


def account_show(request):
    dct = {}
    value = request.GET.get("query", "")  # 搜索框和？query进行绑定
    if value:
        dct["mobile__contains"] = value
    result_set = Account.objects.filter(**dct)  # 没有关键字则获取数据库所有数据，有则搜索满足条件数据
    paginator = Paginator(result_set, 20)
    page = request.GET.get("page")
    try:
        result_set = paginator.page(page)
    except PageNotAnInteger:
        result_set = paginator.page(1)
    except EmptyPage:
        result_set = paginator.page(paginator.num_pages)
    return render(request, 'account_list.html', {"query_set": result_set, "value": value})


class AccountModelForm(BootStrapModelForm):
    mobile = forms.CharField(validators=[RegexValidator(r'^[2-9]\d{2}[2-9]\d{2}\d{4}$', "手机号码输入格式不正确")],
                             label="手机号")

    class Meta:
        model = Account
        fields = '__all__'

    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        # 排除自己本身并检测有没有相同的手机号
        exists = Account.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")
        return txt_mobile


def account_add(request):
    form = AccountModelForm()
    if request.method == "GET":
        return render(request, 'add_edit.html', {"form": form, "title": "新增靓号"})
    form = AccountModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/account/list/")
    return render(request, 'add_edit.html', {"form": form, "title": "新增靓号"})


def account_delete(request, uid):
    Account.objects.filter(id=uid).delete()
    return redirect("/account/list/")


def account_edit(request, uid):
    row_data = Account.objects.filter(id=uid).first()
    form = AccountModelForm(instance=row_data)
    if request.method == "GET":
        return render(request, "add_edit.html", {"form": form, "title": "靓号管理"})
    form = AccountModelForm(data=request.POST, instance=row_data)
    if form.is_valid():
        form.save()
        return redirect("/account/list/")
    return render(request, "add_edit.html", {"form": form, "title": "靓号管理"})


def admin_list(request):
    dct = {}
    value = request.GET.get("query", "")
    if value:
        dct["username__contains"] = value
    result_set = Admin.objects.filter(**dct)
    paginator = Paginator(result_set, 20)
    page = request.GET.get("page")
    try:
        result_set = paginator.page(page)
    except PageNotAnInteger:
        result_set = paginator.page(1)
    except EmptyPage:
        result_set = paginator.page(paginator.num_pages)
    return render(request, "admin_list.html", {"query_set": result_set, "value": value})


class AdminModelForm(BootStrapModelForm):
    confirm = forms.CharField(label="Confirm password")

    class Meta:
        model = Admin
        fields = '__all__'

    def clean_username(self):
        txt_username = self.cleaned_data["username"]
        # 排除自己本身并检测有没有相同的用户名
        exists = Admin.objects.exclude(id=self.instance.pk).filter(username=txt_username).exists()
        if exists:
            raise ValidationError("账号已存在")
        return txt_username

    def clean_password(self):
        pwd = self.cleaned_data["password"]
        return md5(pwd)

    def clean_confirm(self):
        txt_pwd = self.cleaned_data["password"]
        if txt_pwd != md5(self.cleaned_data["confirm"]):
            raise ValidationError("密码输入不一致,请重新输入")
        return txt_pwd


class AdminEditForm(BootStrapModelForm):
    class Meta:
        model = Admin
        fields = ["username"]

    def clean_username(self):
        txt_username = self.cleaned_data["username"]
        # 排除自己本身并检测有没有相同的用户名
        exists = Admin.objects.exclude(id=self.instance.pk).filter(username=txt_username).exists()
        if exists:
            raise ValidationError("账号已存在")
        return txt_username


def admin_add(request):
    form = AdminModelForm()
    if request.method == "GET":
        return render(request, "add_edit.html", {"form": form, "title": "新增管理员"})
    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/admin_user/list/")
    return render(request, "add_edit.html", {"form": form, "title": "新增管理员"})


def admin_delete(request, uid):
    Admin.objects.filter(id=uid).delete()
    return redirect("/admin_user/list/")


def admin_edit(request, uid):
    query_set = Admin.objects.filter(id=uid).first()
    if not query_set:
        return redirect("/admin_user/list/")
    form = AdminEditForm(instance=query_set)
    if request.method == "GET":
        return render(request, "add_edit.html", {"form": form, "title": '管理员编辑'})
    form = AdminEditForm(instance=query_set, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/admin_user/list/")
    return render(request, "add_edit.html", {"form": form, "title": '管理员编辑'})


class AdminResetForm(BootStrapModelForm):
    # username = forms.CharField(label="管理员账号", widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    confirm = forms.CharField(label="确认密码")

    class Meta:
        model = Admin
        fields = ["password", "confirm"]

    def clean_password(self):
        pwd = self.cleaned_data["password"]
        md5_pwd = md5(pwd)
        exists = Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exists:
            raise ValidationError("密码不可和之前一致！")
        return md5_pwd

    def clean_confirm(self):
        txt_pwd = self.cleaned_data.get("password")
        if txt_pwd is not None and txt_pwd != md5(self.cleaned_data["confirm"]):
            raise ValidationError("密码输入不一致,请重新输入")
        return txt_pwd


def admin_reset(request, uid):
    row_object = Admin.objects.filter(id=uid).first()
    if not row_object:
        return redirect("/admin_user/list/")
    title = "重置密码-{}".format(row_object.username)
    if request.method == "GET":
        form = AdminResetForm()
        return render(request, "add_edit.html", {"form": form, "title": title})
    form = AdminResetForm(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/admin_user/list/")
    return render(request, "add_edit.html", {"form": form, "title": title})
