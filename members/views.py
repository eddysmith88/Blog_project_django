from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView

from theblog.models import Profile
from .forms import SignUpForm, EditProfileForm, PasswordChangingForm, ProfilePageForm


class CreateProfilePageView(CreateView):
    """
    View to create a new profile
    """
    model = Profile
    form_class = ProfilePageForm
    template_name = 'registration/create_user_profile.html'

    def form_valid(self, form):
        """
        Validate the form
        :param form:
        :return:
        """
        form.instance.user = self.request.user
        return super().form_valid(form)


class EditProfilePageView(generic.UpdateView):
    """
    View to edit profile page
    """
    model = Profile
    template_name = 'registration/edit_profile_page.html'
    fields = ['bio', 'profile_pic', 'website_url', 'facebook_url', 'instagram_url', 'telegram_url']
    success_url = reverse_lazy('home')


class ShowProfilePage(DetailView):
    """
    View to show profile page
    """
    model = Profile
    template_name = 'registration/user_profile.html'

    def get_context_data(self, *args, **kwargs):
        """
        get context data
        :param args:
        :param kwargs:
        :return:
        """
        users = Profile.objects.all()
        context = super(ShowProfilePage, self).get_context_data(**kwargs)
        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
        context['page_user'] = page_user
        return context


class PasswordsChangeView(PasswordChangeView):
    """
    View to change password
    """
    form_class = PasswordChangingForm
    # form_class = PasswordChangeForm
    success_url = reverse_lazy('password_success')
    # success_url = reverse_lazy('home')


def password_success(request):
    """
    View to show that password correctly changed
    :param request:
    :return:
    """
    return render(request, 'registration/password_success.html', {})


class UserRegisterView(generic.CreateView):
    """
    View to create new profile
    """
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class UserEditView(generic.UpdateView):
    """
    View to edit user profile
    """
    form_class = EditProfileForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user # Вивід інформації про користувача


