import uuid
from django.middleware.clickjacking import XFrameOptionsMiddleware
"""
Django的middlware在项目启动时会被初始化，等接受请求之后会根据settings中的middleware配置顺序挨个调用，传递request作为参数。
在接受请求之后，先生产uid，然后把uid复制给request对象。最后返回response时，设置cookie，并设置httponly只能在服务的访问。这样
用户再次请求时，就会带上同样uid信息了。
"""

USER_KEY = 'uid'
TEN_YEARS = 60 * 60 * 24 * 365 * 10


class UserIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__()

    def __call__(self, request):
        uid = self.generate_uid(request)
        request.uid = uid
        response = self.get_response(request)
        response.set_cookie(USER_KEY, uid, max_age=TEN_YEARS, httponly=True)
        return response

    def generate_uid(self, request):
        try:
            uid = request.COOKIES[USER_KEY]
        except KeyError:
            uid = uuid.uuid4().hex
        return uid
