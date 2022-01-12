from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from .models import Category, Post, PostCategory
from django.core.paginator import Paginator
from django.views import View 
from django.shortcuts import render
from .filters import PostFilter
from .forms import PostForm, SubscriberForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.template import RequestContext
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import datetime
from .models import Subscriber
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt


@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/news/')


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'

def handler404(request, *args, **argv):
    response = render('404.html', {}, context_instance=RequestContext(request))
    response.status_code = 404
    return response

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'protected_index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_auhtor'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context

class PostListNews(ListView):
    model = Post
    template_name = 'news.html' 
    context_object_name = 'news'
    queryset = Post.objects.filter(post_type='NW')
    ordering = ['id']
    paginate_by = 1
    
class PostDetail(DetailView):
    model = Post
    template_name = 'details_news.html' 
    context_object_name = 'news'

class PostDetailEdit(DetailView):
    model = Post
    template_name = 'details_news.html' 
    context_object_name = 'news'
    queryset = Post.objects.filter(post_type='news')

class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.add_post',)
    template_name = 'add_news.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)
 
 
class PostDeleteView(LoginRequiredMixin,DeleteView):
    template_name = 'delete_news.html'
    queryset = Post.objects.all()
    context_object_name = 'news'
    success_url = '/news/'


class PostSearch(ListView):
    model = Post
    template_name = 'search_news.html' 
    context_object_name = 'news'
    paginate_by = 1
    form_class = PostForm

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['PostCategory'] = PostCategory.objects.all()
        context['form'] = PostForm()
        return context
 
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST) 
        
        if form.is_valid(): 
            form.save()
 
        return super().get(request, *args, **kwargs)

class PostAdd(PermissionRequiredMixin, ListView):
    permission_required = ('news.add_post', )
    model = Post
    template_name = 'add_news.html'
    context_object_name = 'news'
    paginate_by = 1
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['PostCategory'] = PostCategory.objects.all()
        context['form'] = PostForm()
        return context
    

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        
        if form.is_valid(): 
            form.save()
            article_text=form.cleaned_data['article_text']
            article_author=form.cleaned_data['post_author']
            created = datetime.datetime.now()
            print(form)
            tuple = {
                'article_text':article_text,
                'article_author':article_author,
            }
            print (tuple['article_text'])
            html_content = render_to_string('email_template.html', { 'context': form, 'article_author':article_author, 'article_text':article_text[:50], 'article_date': created})
            print (html_content)
            msg = EmailMultiAlternatives(
                subject='новая новость!',
                body=html_content,
                from_email='skillfacroty@mail.ru',
                to=['skillfacroty@mail.ru',])
            msg.attach_alternative(html_content, "text/html")
            msg.send() 
        return super().get(request, *args, **kwargs)

@login_required
@csrf_exempt
def subsribe_me(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        print(form)
        email_entered = form.cleaned_data['email']
        category_chosen = form.cleaned_data['category']
        b = str(category_chosen[0])
        if not Subscriber.objects.filter(email=email_entered).exists() and b == 'fiction':
            Subscriber.objects.create(email=email_entered)
        return HttpResponseRedirect('/news/')         
    else:
        return render(request,'subscribe.html', {'form': SubscriberForm(initial={'email':request.user.email})})


