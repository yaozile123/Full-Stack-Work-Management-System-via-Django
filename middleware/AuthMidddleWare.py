from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect


class AuthMiddleWare(MiddlewareMixin):
    def process_request(self, request):
        if request.path_info == "/":
            return
        if "/admin/" in request.path_info:
            return
        if request.path_info == "/login/" or "/captcha/" in request.path_info or request.path_info == "/register/":
            return
        data = request.session.get("info")
        if data:
            if request.path_info == "/":
                return redirect("/user/list/")
            if "admin_user" in request.path_info:
                tmp = request.session.get("admin_user")
                if tmp:
                    return
                else:
                    return redirect("/verify/")
            return
        return redirect("/login/")
