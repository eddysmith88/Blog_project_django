from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from theblog.models import Post, Category, Comment, Profile
from .forms import PostForm, EditForm, CommentForm
from django.http import HttpResponseRedirect
from django.db.models import Q


def LikeView(request, pk):
    """
    View for liking posts
    :param request:
    :param pk:
    :return:
    """
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('article_detail', args=[str(pk)]))


class HomeView(ListView):  # Список постів
    """
    View for home page
    """
    model = Post
    template_name = 'home.html'
    ordering = ['-post_date'] # сортування по даті публікації
    # ordering = ['-id'] # Сортування постів, на початку з останнього доданого айдішнік джанго створив сам

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context['cat_menu'] = cat_menu
        return context


class ArticleDetail(DetailView):  # Детальний опис постів
    """
    View for detail of post
    """
    model = Post
    template_name = 'article_detail.html'

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(ArticleDetail, self).get_context_data(**kwargs)
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes() # вьюшка витягує кількість лайків
        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True
        context['cat_menu'] = cat_menu
        context['total_likes'] = total_likes
        context['liked'] = liked
        return context


class AddPostView(CreateView): # Додавання посту
    """
    Add post view
    """
    model = Post
    form_class = PostForm   # Застосовуємо форму яка тепер витягує всі поля через форму і підключає стилізацію
    template_name = 'add_post.html'


class AddCommentView(CreateView): # Додавання коменту для посту
    """
    Add comment to post
    """
    model = Comment
    form_class = CommentForm   # Застосовуємо форму яка тепер витягує всі поля через форму і підключає стилізацію
    template_name = 'add_comment.html'

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)
    success_url = reverse_lazy('home')


class AddCategoryView(CreateView):
    """
    Add category to post
    """
    model = Category
    template_name = 'add_category.html'
    fields = '__all__'


class UpdatePostView(UpdateView): # редагування постів через форму EditForm, без поля author
    """
    Update post view
    """
    model = Post
    form_class = EditForm
    template_name = 'update_post.html'


class DeletePostView(DeleteView):
    """
    Delete post view
    """
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')


def CategoryView(request, cats):
    """
    Replace space symbol to -
    :param request:
    :param cats:
    :return:
    """
    category_posts = Post.objects.filter(category=cats.replace('-', ' '))
    return render(request, 'categories.html', {'cats': cats.title().replace('-', ' '), 'category_posts': category_posts})


def CategoryListView(request):
    """
    Category list view
    :param request:
    :return:
    """
    cat_menu_list = Category.objects.all()
    return render(request, 'category_list.html', {'cat_menu_list': cat_menu_list})


def post_list(request):
    """
    Search view. With django module Q, make many options for search
    :param request:
    :return:
    """
    search_query = request.GET.get('search', '')
    if search_query:
        posts = Post.objects.filter(Q(category__icontains=search_query) | Q(title__icontains=search_query))
    else:
        posts = Post.objects.all()
    return render(request, 'search.html', {'posts': posts})
