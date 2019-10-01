# Inbuilt system imports
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.views import generic
# User created Imports
from .forms import PostsForm
from .models import blog_posts
# Check requirements.txt for this feature
from braces.views import SelectRelatedMixin
from user_accounts.models import UserProfile


# Create your views here.

# Listing the proposals
def post_list(request, template_name='proposals/post_list.html'):
    posts = blog_posts.objects.all()
    data = {}
    data['object_list'] = posts
    return render(request, template_name, data)


# Creating a proposal only by a company
def post_create(request, template_name='proposals/post_form.html'):
    a=User.objects.get(username=request.user.username)
    form = PostsForm(request.POST or None,initial={'name':a})
    if form.is_valid():
        form.save()
        return redirect('proposals:post_list')
    return render(request, template_name, {'form': form})

# Changing the details of a proposal
def post_update(request, pk, template_name='proposals/post_form.html'):
    post = get_object_or_404(blog_posts, pk=pk)
    form = PostsForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('proposals:post_list')
    return render(request, template_name, {'form': form})

# Deleting a proposal
def post_delete(request, pk, template_name='proposals/post_delete.html'):
    post = get_object_or_404(blog_posts, pk=pk)
    if request.method=='POST':
        post.delete()
        return redirect('proposals:post_list')
    return render(request, template_name, {'object': post})


# Joining or leaving an event
class SingleGroup(generic.DetailView):
    model = blog_posts
    template_name = 'proposals/post_joining.html'

# Displaying usser posts
class UserPosts(generic.ListView):
    model = blog_posts
    select_related = ('user')
    template_name = "proposals/user_post_list.html"
    def get_queryset(self):
        try:
            self.post_list = blog_posts.objects.all()
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_list"] = self.post_list
        return context

# Adding user to the list of attendees
class JoinGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("proposals:post_joining",kwargs={'pk':self.kwargs.get('pk')})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(blog_posts,pk=self.kwargs.get('pk'))
        attendee = User.objects.get(username=request.user)

        try:
            group.attendees.add(attendee)

        except IntegrityError:
            messages.warning(self.request,("Warning, already a member of {}".format(group.InitiativeTitle)))

        else:
            messages.success(self.request,"You are now a member of the {} group.".format(group.InitiativeTitle))

        return super().get(request, *args, **kwargs)

# Removing user from the list of attendees
class LeaveGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("proposals:post_joining",kwargs={'pk':self.kwargs.get('pk')})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(blog_posts,pk=self.kwargs.get('pk'))
        attendee = User.objects.get(username=request.user)
        try:
            group.attendees.remove(attendee)
        except:
            messages.warning(
                self.request,
                "You can't leave this group because you aren't in it."
            )

        else:
            messages.success(
                self.request,
                "You have successfully left this group."
            )
        return super().get(request, *args, **kwargs)
        
# Create proposal option only seen by company
def post_join(request, pk, template_name= 'proposals/post_join.html'):
    Company = 'company'
    new_lists = UserProfile.objects.filter(category= Company)
    lists = {}
    lists['company_list'] = new_lists
    i = 1
    if request.method=='POST':
        return redirect('proposals:post_join')
    return render(request, template_name , lists)


class AttendeesList(generic.DetailView):
    model = blog_posts
    template_name = 'proposals/name_attendees.html'

class AttendeesInfo(generic.DetailView):
    model = UserProfile
    template_name = 'proposals/attendees_info.html'

    def get_queryset(self):
        try:
            self.attendees_list = UserProfile.objects.filter(id=self.kwargs.get("pk"))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.attendees_list

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['attendees_list'] = self.attendees_list
        return context



def see_attending(request, template_name='proposals/see_attending.html'):
    posts = blog_posts.objects.all()
    data = {}
    data['new_list'] = posts
    return render(request, template_name, data)

