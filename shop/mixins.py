from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


class StaffRequiredMixin(object):

    login_url = settings.LOGIN_URL

    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        return staff_member_required(view, login_url=cls.login_url)


class LoginRequiredMixin(object):

    login_url = settings.LOGIN_URL

    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        return login_required(view, login_url=cls.login_url)