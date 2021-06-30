from django.views.generic import CreateView, ListView, DeleteView
from django.shortcuts import render
from django.views.generic import UpdateView, TemplateView
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, FormView
from django.contrib.auth.models import User
from django.db.models import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.conf import settings
from .forms import UserProfileForm
from .tokens import account_activation_token
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from .models import Password, Category
from .forms import PasswordForm, CategoryForm, UserRegistrationForm


class PasswordListView(ListView):

    model = Password

    template_name = 'keep/index.html'
    extra_context = {
        'title': "Home",
    }

    def get_queryset(self):
        return Password.objects.filter(user=self.request.user)


class PasswordCreateView(CreateView):

    model = Password
    form_class = PasswordForm

    def form_valid(self, form):
        passwd = form.save(commit=False)
        passwd.user = self.request.user
        passwd.save()
        return HttpResponseRedirect(reverse("keep:index"))


class PasswordUpdateView(UpdateView):

    model = Password
    form_class = PasswordForm
    success_url = reverse_lazy("keep:index")


class PasswordDeleteView(DeleteView):

    model = Password
    success_url = reverse_lazy("keep:index")


class CategoryListView(ListView):

    model = Category

    extra_context = {
        'title': "Category",
    }

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class CategoryCreateView(CreateView):

    model = Category
    form_class = CategoryForm

    extra_context = {
        'title': "Add Category",
    }

    def form_valid(self, form):
        passwd = form.save(commit=False)
        passwd.user = self.request.user
        passwd.save()
        return HttpResponseRedirect(reverse("keep:category"))


class CategoryUpdateView(UpdateView):

    extra_context = {
        'title': "Update Category",
    }

    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy("keep:category")


class CategoryDeleteView(DeleteView):

    extra_context = {
        'title': "Delete Category",
    }

    model = Category
    success_url = reverse_lazy("keep:category")


class Profile(UpdateView):
    """
    This class puts together everything for the profile update page
    """

    # django built-in attributes
    form_class = UserProfileForm
    template_name = "keep/profile.html"

    extra_context = {
        "title": "Profile",
    }

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, {"form": form, **self.extra_context})

    @method_decorator(login_required())
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("keep:profile"))
        return render(request, self.template_name, {"form": form, **self.extra_context})


class UserLoginView(LoginView):

    redirect_authenticated_user = True
    template_name = "keep/login.html"

    extra_context = {
        "title": "Login",
    }

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        user = form.get_user()
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())


class UserRegistrationView(FormView):

    form_class = UserRegistrationForm
    template_name = 'registration/register.html'

    extra_context = {
        "title": "Resister",
    }

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('keep:index'))
        return render(request, self.template_name, {"form": self.form_class, **self.extra_context})

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('keep:index'))

        user_form = self.form_class(data=request.POST)

        if user_form.is_valid():

            user = user_form.save(commit=False)
            user.is_active = False
            user.save()  # user id is populated after this record is saved

            current_site = get_current_site(request)
            mail_subject = f'Activate your {settings.MAIN_TITLE} account.'

            message = render_to_string('registration/register_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': force_text(urlsafe_base64_encode(force_bytes(user.id))),
                'token': account_activation_token.make_token(user),
            })

            to_email = user_form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email, ])
            email.send()
            return HttpResponseRedirect(reverse('keep:register_email_sent'))
        else:
            return render(request, self.template_name, {"form": user_form})


class RegisterEmailSent(TemplateView):
    template_name = 'registration/register_email_sent.html'

    extra_context = {
        "title": "Registration Email Sent",
    }


class ActivateUser(TemplateView):

    template_name = "registration/register_email_invalid.html"
    template_name_success = "registration/register_email_confirmed.html"

    extra_context = {
        "title": "Account Activation",
    }

    def get(self, request, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(kwargs['uidb64']))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, ObjectDoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, kwargs['token']):
            user.is_active = True
            user.save()
            login(request, user)

            return render(request, self.template_name_success)
        else:
            return render(request, self.template_name)
