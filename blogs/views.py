from django.shortcuts import render, redirect
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import BlogPost
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

@login_required
def blog_posts(request):
    posts = BlogPost.objects.all()
    return render(request, 'blog_templates/blog_post.html', {'posts': posts})

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }

class BlogPostCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog_templates/create_blog_post.html'
    success_url = reverse_lazy('blog_posts')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog_templates/blog_post_detail.html'
    context_object_name = 'post'

class BlogPostUpdateView(LoginRequiredMixin, UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog_templates/update_blog_post.html'
    context_object_name = 'post'
    success_url = reverse_lazy('blog_posts')

class BlogPostDeleteView(LoginRequiredMixin, DeleteView):
    model = BlogPost
    template_name = 'blog_templates/delete_blog_post.html'
    context_object_name = 'post'
    success_url = reverse_lazy('blog_posts')

# Authentication views

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('blog_posts')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('blog_posts')
