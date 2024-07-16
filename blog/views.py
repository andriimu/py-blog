from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.views.generic.detail import DetailView
from django.contrib.auth import get_user_model
from django.utils.functional import SimpleLazyObject

from.forms import CommentaryForm
from .models import (
    Post
)

user = get_user_model()

def index(request):
    posts = Post.objects.all().order_by('created_time')
   
    paginator = Paginator(posts, 5)  # Show 5 posts per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        
        'page_obj': page_obj,
    }
    return render(request, 'blog/index.html', context)

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.commentaries.all()
        if self.request.user.is_authenticated:
            context['form'] = CommentaryForm() 
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.is_authenticated:
            return redirect('login') 
        form = CommentaryForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.user = request.user
            comment.save()
            return redirect('blog:post-detail', pk=self.object.pk)
        return self.render_to_response(self.get_context_data(form=form))
    

