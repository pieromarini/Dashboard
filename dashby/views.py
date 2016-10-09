from django.views.generic import View
from django.http import HttpResponse
from django.views.generic import CreateView, UpdateView, DeleteView,ListView, DetailView
from django.core.urlresolvers import reverse_lazy, reverse
from dashby.models import Document
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
import os
import mimetypes
from .response import JSONResponse, response_mimetype
from .forms import UserForm, LoginForm
from django.contrib import messages

def index(request):
    return render(request, 'index.html')

class AllUsersViews(UserPassesTestMixin, View):
    template_name = 'all_users.html'
    login_url = reverse_lazy('dashby-files:files')

    def test_func(self):
        return self.request.user.is_superuser

    # Send message to display popup.
    def handle_no_permission(self):
        messages.add_message(self.request, messages.WARNING, "Superuser required to access this page.")
        return redirect('dashby-files:login')

    # No redirect query.
    def get_redirect_field_name(self):
        return None

    def get(self, request):
        context = {'users': User.objects.all()}
        #messages.add_message(request, messages.SUCCESS, "You have access")
        return render(request, self.template_name, context)

class DashbyView(View):
    template_name = 'dashby.html'

    def get(self, request):
        return render(request, self.template_name)

class IndexView(ListView):
    template_name = 'files.html'
    context_object_name = 'files'

    def get_queryset(self):
        #Filter by is_public to display only public files.
        return Document.objects.all().filter(is_public=True)

class PrivateFilesView(ListView):
    template_name = 'files.html'
    context_object_name = 'files'

    def get_queryset(self):
        # Get Files with access permissions and not public.
        return Document.objects.all().filter(is_public =
        False).filter(allowed_users = self.request.user)

class DetailView(DetailView):
    model = Document
    template_name = 'detail.html'
    context_object_name = 'document'

class DocumentCreate(CreateView):
    model = Document
    fields = ['file', 'is_public']

    def form_valid(self, form):
        self.object = form.save(commit = False)
        self.object.uploaded_by = self.request.user
        self.object.save()
        self.object.allowed_users.add(self.request.user)
        self.object.save()
        data = {'status': 'success'}
        response = JSONResponse(data, mimetype =
        response_mimetype(self.request))
        return response

class DocumentUpdate(UserPassesTestMixin, UpdateView):
    model = Document
    fields = ['file', 'allowed_users']
    template_name_suffix = '_update_form' #document_update_form.html
    #Raise PermissionDenied
    raise_exception = True

    #Only allowed users can modify the file.
    def test_func(self):
        self.object = self.get_object()
        if self.request.user in self.object.allowed_users.all():
            return True
        return False

class DocumentDelete(DeleteView):
    model = Document
    #Handle redirect for private and public files.
    def get_success_url(self):
        if self.object.is_public:
            return reverse('dashby-files:files')
        else:
            return reverse('dashby-files:private')

class UserFormView(View):
    form_class = UserForm
    template_name = 'registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username = username,
                                password = password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('dashby-files:files')

        return render(request, self.template_name, {'form': form})

class LoginFormView(View):
    form_class = LoginForm
    template_name = 'login_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username,
                            password = password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('dashby-files:files')
            else:
                return redirect('dashby-files:login')
        else:
            return render(request, self.template_name,
                         {'form' : form})


class LogoutFormView(View):

    @method_decorator(login_required)
    def get(self, request):
        logout(request)
        return redirect('dashby-files:dashby')
