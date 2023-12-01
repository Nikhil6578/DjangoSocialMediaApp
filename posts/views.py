from django.shortcuts import render, redirect, get_object_or_404
from mysocial.models import UserProfile, FriendRequest
from posts.form import PostForm
from posts.models import UserPost
from django.db.models import Q
from django.contrib.auth.decorators import login_required


@login_required
def upload_or_edit_post(request, post_id=None):
    userprofile = UserProfile.objects.get(user=request.user)
    if post_id:
        post = get_object_or_404(UserPost, id=post_id)
    else:
        post = None

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            updated_post = form.cleaned_data['post']
            updated_caption = form.cleaned_data['caption']

            # For editing an existing post
            if post:
                # Keep the existing post if no new file is provided
                post.post = updated_post
                post.caption = updated_caption
                post.save()
            else:
                # For creating a new post
                UserPost.objects.create(
                    userprofile=userprofile,
                    post=updated_post,
                    caption=updated_caption
                )

            return redirect('/posts/user_post/')

    else:
        form = PostForm(instance=post)

    template = 'user_post_upload.html'
    context = {'form': form, 'post': post}
    return render(request, template, context)


@login_required
def user_post_or_friend_post(request, request_id=None):
    user_profile = get_object_or_404(UserProfile, user_id=request.user.id)

    if not request_id:
        accepted_friend_ids = FriendRequest.objects.filter(
            (Q(from_user=user_profile) | Q(to_user=user_profile)) &
            Q(status='accepted')
        ).values_list('from_user__user_id', 'to_user__user_id')

        friend_ids = [friend_id for friendship in accepted_friend_ids
                      for friend_id in friendship]

        user_posts_and_friends_posts = UserPost.objects.filter(
            Q(userprofile__user_id=request.user.id) |
            Q(userprofile__user_id__in=friend_ids)
        ).order_by('-dop')

        return render(request, "user_post.html", {
            'user_post': user_profile.userpost_set.all(),
            'user_posts_and_friends_posts': user_posts_and_friends_posts
        })

    friend = get_object_or_404(UserProfile, user_id=request_id)
    return render(request, "user_friends_posts.html",
                  {'friend': friend}
                  )


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(UserPost, id=post_id)
    # Delete the post
    post.delete()
    # Redirect to a success page or any other appropriate page
    return redirect('/posts/user_post/')
