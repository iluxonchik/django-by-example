from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm
from django.views.generic import ListView
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3 # page object is passed to view as "page_obj"
    template_name = 'blog/post/list.html'

def post_list(request, tag_slug=None):
    object_list = Post.published.all()

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3) # 3 posts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if page passed in GET is not an integer, deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page is out of range, deliver the last page
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', 
        {
            'posts':posts, # page to be displayed object 
            'page':page,
            'tag': tag,
        })
    
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published', publish__year=year, 
                                   publish__month=month, publish__day=day)
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    context = {'post':post, 'comments': comments}
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)  # if the form is not valid, it will be rendered with validation errors (below)
        if comment_form.is_valid():
            # Create a Comment object, but don't save it to the database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the newly created comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
            context["new_comment"] = new_comment
    else:
        comment_form = CommentForm()
        context["comment_form"] = comment_form

    # List of similiar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    # annotate() -> COUNT tags ... GROUP BY post.id
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4] 
    context["similar_posts"] = similar_posts
    
    return render(request, 'blog/post/detail.html', context)

def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    cd = None
    sent = False
    if request.method == "POST":
        # The form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            # NOTE: if using Gmail, it will rewrite the From and Reply-To headers
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        # Form was not submitted, so let's just display it
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent, 'cd':cd})