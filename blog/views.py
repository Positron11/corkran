from .models import Post, Comment
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View


class PostListView(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
    ordering = ["-date"]
    paginate_by = 5

    def get_queryset(self):
        if self.request.method == 'GET':
            search_query = self.request.GET.get('search_box', "")
            return Post.objects.filter(Q(tags__name__in=[search_query]) | Q(title__icontains=search_query)).distinct().order_by("-date")
        else:
            return Post.objects.order_by("-date")


class UserPostListView(ListView):
    model = Post
    template_name = "blog/user_posts.html"
    context_object_name = "posts"
    ordering = ["-date"]
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        if self.request.method == 'GET':
            search_query = self.request.GET.get('search_box', "")
            return Post.objects.filter(author=user).filter(Q(tags__name__in=[search_query]) | Q(title__icontains=search_query)).distinct().order_by("-date")
        else:
            return Post.objects.filter(author=user).order_by("-date")


class PostView(DetailView):
    model = Post
    pass


class CommentView(CreateView):
    model = Comment
    fields = ["content"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post = self.get_object(Post.objects.all())
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.get_object(Post.objects.all()).pk})
    pass


class PostDetailView(View):
    def get(self, request, *args, **kwargs):
        view = PostView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs) :
        view = CommentView.as_view()
        return view(request, *args, **kwargs)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content", "tags"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "content", "tags"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.user or self.request.user == comment.post.author:
            return True
        else:
            return False

    def get_success_url(self):
        return reverse_lazy('post-detail', kwargs={'pk': self.get_object(Comment.objects.all()).post.pk})


def about(request):
    return render(request, "blog/about.html")

