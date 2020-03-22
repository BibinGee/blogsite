from django.shortcuts import redirect
from django.views.generic import TemplateView

from .forms import CommentForm

# Create your views here.


class CommentView(TemplateView):
    http_method_names = ['post']
    template_name = 'comment/result.html'

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        target = request.POST.get('target')
        # print(target)

        if 'HTTP_X_FORWARDED_FOR' in request.META:  # 获取ip
            client_ip = request.META['HTTP_X_FORWARDED_FOR']
            client_ip = client_ip.split(",")[0]  # 所以这里是真实的ip
        else:
            client_ip = request.META['REMOTE_ADDR']  # 这里获得代理ip

        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.target = target
            instance.nickname = f'游客[{client_ip}]'
            instance.save()
            succeed = True
            return redirect(target)
        else:
            succeed = False

        context = {
            'succeed': succeed,
            'form': comment_form,
            'target': target,
        }

        return self.render_to_response(context)
