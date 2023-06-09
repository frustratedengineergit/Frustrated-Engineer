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
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from dashboard.views import dashboard



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
            'categories': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categories'].queryset = Category.objects.all()
        self.fields['tags'].queryset = Tag.objects.all()

class BlogPostCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog_templates/create_blog_post.html'
    success_url = reverse_lazy('blog_posts')

    def form_valid(self, form):
        form.instance.author = self.request.user

        image_file = self.request.FILES.get('image')
        if image_file:
            # Upload the image to Firebase Storage
            bucket = storage.bucket('frustratedengineer-9a5cc.appspot.com')
            filename = f"blogimages/{image_file.name}"
            blob = bucket.blob(filename)
            blob.upload_from_file(image_file)

            # Get the public URL of the uploaded image
            image_url = blob.public_url
            # Save the image URL to the form instance
            form.instance.image_url = image_url

        return super().form_valid(form)


class BlogPostUpdateView(LoginRequiredMixin, UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog_templates/update_blog_post.html'
    context_object_name = 'post'
    success_url = reverse_lazy('blog_posts')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user

        # Save the updated post
        post.save()

        # Handle the image file
        image_file = self.request.FILES.get('image')
        if image_file:
            # Get the bucket
            bucket = storage.bucket('frustratedengineer-9a5cc.appspot.com')

            # Delete the previous image
            previous_image_url = self.object.image_url
            if previous_image_url:
                try:
                    # Extract the filename from the URL
                    filename = previous_image_url.split('/')[-1]

                    # Delete the file from the bucket
                    blob = bucket.blob(filename)
                    blob.delete()
                except Exception as e:
                    # Handle the exception as per your requirement
                    pass
                
            # Upload the new image
            filename = f"blogimages/{image_file.name}"
            blob = bucket.blob(filename)
            blob.upload_from_file(image_file.file)

            # Get the public URL of the uploaded file
            image_url = blob.public_url
            post.image_url = image_url

        # Save the updated post with the image URL
        post.save()

        return super().form_valid(form)

class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog_templates/blog_post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        context['image_url'] = post.image_url if post.image_url else None
        context['comments'] = post.comments.all()
        return context

class BlogPostDeleteView(LoginRequiredMixin, DeleteView):
    model = BlogPost
    template_name = 'blog_templates/delete_blog_post.html'
    context_object_name = 'post'
    success_url = reverse_lazy('blog_posts')

    def delete(self, request, *args, **kwargs):
        post = self.get_object()

        # Delete the image from Firebase Storage when deleting the blog post
        image_url = post.image_url
        if image_url:
            bucket = storage.bucket('frustratedengineer-9a5cc.appspot.com')
            blob = bucket.blob(image_url)
            blob.delete()

        return super().delete(request, *args, **kwargs)


# Authentication views

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('dashboard')


@login_required
def comment_create(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        content = request.POST.get('content')
        Comment.objects.create(post=post, author=request.user, content=content)
    return redirect('blog_post_detail', pk=post.pk)

