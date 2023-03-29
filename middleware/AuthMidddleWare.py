from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect


class AuthMiddleWare(MiddlewareMixin):
    def process_request(self, request):
        if request.path_info == "/login/" or "/captcha/" in request.path_info:
            return
        data = request.session.get("info")
        if data:
            return
        return redirect("/login/")
