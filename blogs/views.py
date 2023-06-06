from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import BlogPost, Comment
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from markdownx.widgets import MarkdownxWidget
from .models import Category, Tag


@login_required
def blog_posts(request):
    posts = BlogPost.objects.all()
    paginator = Paginator(posts, 10)  # Set the number of posts to display per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog_templates/blog_post.html', {'page_obj': page_obj})


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'categories', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': MarkdownxWidget(attrs={'class': 'form-control'}),
            'categories': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'tags': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }


class BlogPostCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog_templates/create_blog_post.html'
    success_url = reverse_lazy('blog_posts')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogPostDetailView(LoginRequiredMixin, DetailView):
    model = BlogPost
    template_name = 'blog_templates/blog_post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comment_set.all()
        return context


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

@login_required
def logout_view(request):
    logout(request)
    return redirect('blog_posts')


@login_required
def comment_create(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        content = request.POST.get('content')
        Comment.objects.create(post=post, author=request.user, content=content)
    return redirect('blog_post_detail', pk=post.pk)
