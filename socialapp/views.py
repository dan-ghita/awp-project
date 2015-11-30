from django.shortcuts import render, redirect

from socialapp.models import UserPost, UserPostComment
from socialapp.forms import UserPostForm, UserPostCommentForm


def index(request):
    if request.method == 'GET':
        posts = UserPost.objects.order_by('-date_added')
        form = UserPostForm()
        context = {
            'posts': posts,
            'form': form,
        }
        return render(request, 'index.html', context)
    elif request.method == 'POST':
        form = UserPostForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            user_post = UserPost(text=text)
            user_post.save()
        return redirect('index')


def post_details(request, pk):
    if request.method == 'POST':
        form = UserPostCommentForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            comment = UserPostComment(text=text)
            comment.post_id = pk
            comment.save()

    post = UserPost.objects.get(pk=pk)
    comments = post.userpostcomment_set.all().order_by('-date_added')
    form = UserPostCommentForm()

    context = {'post': post, 'comments': comments, 'form': form}

    return render(request, 'post_details.html', context)
