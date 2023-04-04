import json
import random

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt

from app02.models import Department, Employee, Task, Order, Customer
from django import forms
from utils.Form import BootStrapForm
from utils.ModelForm import BootStrapModelForm
from utils.encrypt import md5
from app03.models import Admin
from app03.views import AdminModelForm
from captcha.fields import CaptchaField
from django.core.validators import ValidationError
from datetime import datetime

# Create your views here.
PASSWORD = "12345"


def department_list(request):
    form = DepartmentModelForm()
    query_set = Department.objects.all().order_by("id")
    return render(request, "department_list.html", {'query_set': query_set, "form": form})


def department_delete(request):
    uid = request.GET.get("uid")
    flag = Department.objects.filter(id=uid).exists()
    if flag:
        Department.objects.filter(id=uid).delete()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": "data not exist"})


@csrf_exempt
def department_add(request):
    form = DepartmentModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": form.errors})


@csrf_exempt
def department_edit(request):
    uid = request.GET.get("uid")
    query_object = Department.objects.filter(id=uid).first()
    form = DepartmentModelForm(data=request.POST, instance=query_object)
    if query_object and form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": form.errors})


def department_detail(request):
    uid = request.GET.get("uid")
    flag = Department.objects.filter(id=uid).exists()
    if flag:
        query = Department.objects.filter(id=uid).first()
        return JsonResponse({"status": True, "data": {"department": query.department}})
    return JsonResponse({"status": False, "error": "data not exist"})


class DepartmentModelForm(BootStrapModelForm):
    class Meta:
        model = Department
        fields = '__all__'

    def clean_department(self):
        department = self.cleaned_data["department"]
        # 排除自己本身并检测有没有相同的手机号
        exists = Department.objects.exclude(id=self.instance.pk).filter(department=department).exists()
        if exists:
            raise ValidationError("Department already exists")
        return department


def user_list(request):
    query_set = Employee.objects.all()
    return render(request, "user_list.html", {'query_set': query_set})


class UserModelForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        # widgets = {"name": forms.TextInput(attrs={"class": "form-control"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == "register_time":  # 修改成日期选择框
                field.widget = forms.DateInput(attrs={'type': 'date'})
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def user_add(request):
    form = UserModelForm()
    if request.method == "GET":
        return render(request, "add_edit.html", {"form": form, "title": "Add New Employee"})
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    return render(request, "add_edit.html", {"form": form, "title": "Add New Employee"})


def user_delete(request, uid):
    Employee.objects.filter(id=uid).delete()
    return redirect("/user/list/")


def user_edit(request, uid):
    row_object = Employee.objects.filter(id=uid).first()
    form = UserModelForm(instance=row_object)
    if request.method == "GET":
        return render(request, "add_edit.html", {"form": form, "title": "Edit Employee"})
    row_object = Employee.objects.filter(id=uid).first()
    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")
    return render(request, "add_edit.html", {"form": form, "title": "Edit Employee"})  # 把报错信息显示出来


def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {"form": form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        username = form.cleaned_data["username"]
        pwd = form.cleaned_data["password"]
        user = Admin.objects.filter(username=username, password=pwd).first()
        if user:
            # 网站生成随机字符串 写入到cookie中再写入到session中
            request.session['info'] = {"ID": user.pk, "username": user.username}
            return redirect("/user/list/")
        else:
            form.add_error("password", "Invalid Username/Password")
    return render(request, "login.html", {"form": form})


class LoginForm(BootStrapForm):
    username = forms.CharField(label="Username", widget=forms.TextInput)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    captcha = CaptchaField(label="Enter Captcha", output_format=u'%(image)s %(hidden_field)s %(text_field)s')

    def clean_password(self):
        return md5(self.cleaned_data.get("password"))


def logout(request):
    request.session.clear()
    return redirect("/login/")


class TaskModelForm(BootStrapModelForm):
    class Meta:
        model = Task
        fields = "__all__"
        widgets = {"detail": forms.TextInput}


def task_list(request):
    form = TaskModelForm()
    return render(request, "task_list.html", {"form": form})


@csrf_exempt
def task_add(request):
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        dct = {"status": True}
        return HttpResponse(json.dumps(dct))
    dct = {"status": False, "error": form.errors}
    return HttpResponse(json.dumps(dct))


class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = Order
        exclude = ["order_number"]


def order_list(request):
    form = OrderModelForm()
    value = request.GET.get("query", "")
    dct = {}
    if value:
        dct[""] = value
    query_set = Order.objects.filter(**dct)
    paginator = Paginator(query_set, 20)
    page = request.GET.get("page", "")
    try:
        result_set = paginator.page(page)
    except PageNotAnInteger:
        result_set = paginator.page(1)
    except EmptyPage:
        result_set = paginator.page(paginator.num_pages)
    return render(request, "order_list.html", {"query_set": result_set, "value": value, "form": form})


@csrf_exempt
def order_add(request):
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        form.instance.order_number = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))
        form.save()
        dct = {"status": True}
        return HttpResponse(json.dumps(dct))
    dct = {"status": False, "error": form.errors}
    return HttpResponse(json.dumps(dct))


def order_delete(request):
    flag = Order.objects.filter(id=request.GET.get("uid")).exists()
    if flag:
        Order.objects.filter(id=request.GET.get("uid")).delete()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": "data not exist"})


def order_detail(request):
    uid = request.GET.get("uid")
    flag = Order.objects.filter(id=uid).exists()
    if flag:
        query = Order.objects.filter(id=uid).first()
        result = {"name": query.name, "price": query.price, "status": query.status,
                  "customer_id": query.customer_id.pk}
        return JsonResponse({"status": True, "data": result})
    return JsonResponse({"status": False, "error": "data not exist"})


@csrf_exempt
def order_edit(request):
    uid = request.GET.get("uid")
    query_object = Order.objects.filter(id=uid).first()
    form = OrderModelForm(instance=query_object, data=request.POST)
    if query_object:
        form.save()
        dct = {"status": True}
        return HttpResponse(json.dumps(dct))
    dct = {"status": False, "error": form.errors}
    return HttpResponse(json.dumps(dct))


def register(request):
    form = AdminModelForm()
    if request.method == "GET":
        return render(request, "register.html", {"form": form})
    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/login/")
    return render(request, "register.html", {"form": form})


@csrf_exempt
def verify(request):
    if request.method == "GET":
        form = VerificationForm()
        return render(request, "verification.html", {"form": form})
    form = VerificationForm(data=request.POST)
    if form.is_valid():
        request.session["admin_user"] = True
        return redirect("/admin_user/list/")
    return render(request, "verification.html", {'form': form})


class VerificationForm(BootStrapForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'}))

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password != PASSWORD:
            raise ValidationError('Incorrect password')
        return password


def customer_list(request):
    value = request.GET.get("query", "")
    dct = {}
    if value:
        dct["username__contains"] = value
    result_set = Customer.objects.filter(**dct)
    paginator = Paginator(result_set, 20)
    page = request.GET.get("page")
    try:
        result_set = paginator.page(page)
    except PageNotAnInteger:
        result_set = paginator.page(1)
    except EmptyPage:
        result_set = paginator.page(paginator.num_pages)
    return render(request, "customer_list.html", {"query_set": result_set, "value": value})


class CustomerModelForm(BootStrapModelForm):
    class Meta:
        model = Customer
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == "birthdate":  # 修改成日期选择框
                field.widget = forms.DateInput(attrs={'type': 'date'})
                field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def customer_add(request):
    form = CustomerModelForm()
    if request.method == "GET":
        return render(request, "add_edit.html", {"form": form, "title": "Add New Customer"})
    form = CustomerModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/customer/list/")
    return render(request, "add_edit.html", {"form": form, "title": "Add New Customer"})


def customer_edit(request, uid):
    query_object = Customer.objects.filter(id=uid).first()
    form = CustomerModelForm(instance=query_object)
    if request.method == "GET":
        return render(request, "add_edit.html", {"form": form, "title": "Add New Customer"})
    form = CustomerModelForm(data=request.POST, instance=query_object)
    if form.is_valid():
        form.save()
        return redirect("/customer/list/")
    return render(request, "add_edit.html", {"form": form, "title": "Add New Customer"})


def customer_delete(request, uid):
    Customer.objects.filter(id=uid).delete()
    return redirect("/customer/list/")