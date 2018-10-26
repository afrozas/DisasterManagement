from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignUpForm, AddWatchForm
from .models import Watch


class SignUpView(FormView):
    template_name = 'accounts/signup.html'
    form_class = SignUpForm
    success_url = '/accounts/login'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class AddWatchView(LoginRequiredMixin, FormView):
    template_name = 'accounts/addwatch.html'
    form_class = AddWatchForm
    success_url = '/dashboard'

    def post(self, request, *args, **kwargs):
        self.user = request.user
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        watchees = form.cleaned_data['watchees']
        if self.user in watchees:
            form.add_error(None, "User cannot add themself to watch.")
            return super().form_invalid(form)
        for watchee in watchees:
            Watch.objects.get_or_create(watcher=self.user, watchee=watchee)
        return super().form_valid(form)
