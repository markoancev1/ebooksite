from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from modulebook.forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.encoding import force_text
from .token_generator import account_activation_token
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.utils import translation
from django.urls import reverse
# Create your views here.

from .forms import EbookForm, CommentForm
from .models import Ebook, Profile, Comment


class Home(TemplateView):
    template_name = 'home.html'


@user_passes_test(lambda u: u.is_superuser)
def upload_book(request):
    if request.method == 'POST':
        form = EbookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = EbookForm()
    return render(request, 'upload_book.html', {
        'form': form
    })


def book_list(request):
    books = Ebook.objects.all()
    # translation.activate('mk').request.LANGUAGE_CODE = translation.get.language()
    query = request.GET.get("q")
    if query:
        books = books.filter(Q(ebook_title__icontains=query)).distinct()

    page = request.GET.get('page', 1)

    paginator = Paginator(books, 2)

    try:
        ebooks = paginator.page(page)
    except PageNotAnInteger:
        ebooks = paginator.page(1)
    except EmptyPage:
        ebooks = paginator.page(paginator.num_pages)
    return render(request, 'book_list.html', {
        'books': ebooks,
    })


@user_passes_test(lambda u: u.is_superuser)
def delete_book(request, pk):
    if request.method == 'POST':
        book = Ebook.objects.get(pk=pk)
        book.delete()
    return redirect('book_list')


def detail_view(request, pk):
    book = get_object_or_404(Ebook, pk=pk)

    comments = book.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = book
            new_comment.name = request.user
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    likes_connected = get_object_or_404(Ebook, id=pk)
    liked = False
    if likes_connected.likes.filter(id=request.user.id).exists():
        liked = True
    return render(request, "book_detail.html", {
        "book": book,
        'number_of_likes': likes_connected.number_of_likes(),
        'book_is_liked': liked,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form
    })


def update_book(request, pk):
    context = {}
    obj = get_object_or_404(Ebook, id=pk)

    if request.FILES:
        form = EbookForm(request.POST, request.FILES or None, instance=obj)
    else:
        form = EbookForm(request.POST or None, instance=obj)

    if form.is_valid():
        form.save()
        return redirect('book_list')

    context["form"] = form

    return render(request, "book_update.html", context)


def register_request(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Activate Your Account'
            message = render_to_string('user/activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': force_text(urlsafe_base64_encode(force_bytes(user.pk))),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            return HttpResponse('We have sent you an email, please confirm your email address to complete registration')
    else:
        form = SignUpForm
    return render(request=request, template_name="user/signup.html", context={"register_form": form})


def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Your account has been activate successfully')
    else:
        return HttpResponse('Activation link is invalid!')


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("book_list")
    form = AuthenticationForm()
    return render(request=request, template_name="user/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("book_list")


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="user/password_reset.html",
                  context={"password_reset_form": password_reset_form})


@login_required
def profile(request):
    Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'user/profile.html', context)


def book_like(request, pk):
    post = get_object_or_404(Ebook, id=request.POST.get('book_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('detail_book', args=[str(pk)]))


@user_passes_test(lambda u: u.is_superuser)
def delete_comment(request, pk):
    if request.method == 'POST':
        book = get_object_or_404(Comment, pk=pk)
        book.delete()
    return redirect('detail_book', pk=book.post_id)
