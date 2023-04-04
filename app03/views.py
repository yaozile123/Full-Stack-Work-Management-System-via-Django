from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from app03.models import Admin
from django import forms
from django.core.validators import RegexValidator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from utils.ModelForm import BootStrapModelForm
from utils.encrypt import md5


# Create your views here.


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
            raise ValidationError("Username Already exists")
        return txt_username

    def clean_password(self):
        pwd = self.cleaned_data["password"]
        return md5(pwd)

    def clean_confirm(self):
        txt_pwd = self.cleaned_data["password"]
        if txt_pwd != md5(self.cleaned_data["confirm"]):
            raise ValidationError("Passwords do not match. Please re-enter.")
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
            raise ValidationError("Username Already Exists")
        return txt_username


def admin_add(request):
    form = AdminModelForm()
    if request.method == "GET":
        return render(request, "add_edit.html", {"form": form, "title": "Add New Admin"})
    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/admin_user/list/")
    return render(request, "add_edit.html", {"form": form, "title": "Add New Admin"})


def admin_delete(request, uid):
    Admin.objects.filter(id=uid).delete()
    return redirect("/admin_user/list/")


def admin_edit(request, uid):
    query_set = Admin.objects.filter(id=uid).first()
    if not query_set:
        return redirect("/admin_user/list/")
    form = AdminEditForm(instance=query_set)
    if request.method == "GET":
        return render(request, "add_edit.html", {"form": form, "title": 'Edit Admin'})
    form = AdminEditForm(instance=query_set, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/admin_user/list/")
    return render(request, "add_edit.html", {"form": form, "title": 'Edit Admin'})


class AdminResetForm(BootStrapModelForm):
    # username = forms.CharField(label="管理员账号", widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    confirm = forms.CharField(label="Confirm Password")

    class Meta:
        model = Admin
        fields = ["password", "confirm"]

    def clean_password(self):
        pwd = self.cleaned_data["password"]
        md5_pwd = md5(pwd)
        exists = Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exists:
            raise ValidationError("The password cannot be the same as before!")
        return md5_pwd

    def clean_confirm(self):
        txt_pwd = self.cleaned_data.get("password")
        if txt_pwd is not None and txt_pwd != md5(self.cleaned_data["confirm"]):
            raise ValidationError("Passwords do not match. Please re-enter")
        return txt_pwd


def admin_reset(request, uid):
    row_object = Admin.objects.filter(id=uid).first()
    if not row_object:
        return redirect("/admin_user/list/")
    title = "Reset Password-{}".format(row_object.username)
    if request.method == "GET":
        form = AdminResetForm()
        return render(request, "add_edit.html", {"form": form, "title": title})
    form = AdminResetForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/admin_user/list/")
    return render(request, "add_edit.html", {"form": form, "title": title})
