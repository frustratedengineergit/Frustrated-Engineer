from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import BlogPost, Comment, Category, Tag
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from markdownx.widgets import MarkdownxWidget

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
        }

    CATEGORIES_CHOICES = [
        ('category1', 'Category 1'),
        ('category2', 'Category 2'),
        ('category3', 'Category 3'),
        ('category4', 'Category 4'),
        ('category5', 'Category 5'),
    ]
    TAGS_CHOICES = [
        ('tag1', 'Tag 1'),
        ('tag2', 'Tag 2'),
        ('tag3', 'Tag 3'),
        ('tag4', 'Tag 4'),
        ('tag5', 'Tag 5'),
        ('tag6', 'Tag 6'),
    ]
    categories = forms.MultipleChoiceField(
        choices=CATEGORIES_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
    )
    tags = forms.MultipleChoiceField(
        choices=TAGS_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
    )


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
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


@login_required
def comment_create(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        content = request.POST.get('content')
        Comment.objects.create(post=post, author=request.user, content=content)
    return redirect('blog_post_detail', pk=post.pk)

