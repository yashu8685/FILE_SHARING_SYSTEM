from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from files.models import UploadedFile
from django.db.models import Sum
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from .forms import EditProfileForm

from .forms import RegisterForm


def home(request):

    total_users = User.objects.count()

    total_files = UploadedFile.objects.count()

    total_downloads = UploadedFile.objects.aggregate(
        Sum("download_count")
    )["download_count__sum"] or 0

    context = {
        "total_users": total_users,
        "total_files": total_files,
        "total_downloads": total_downloads,
    }

    return render(request, "home.html", context)


def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")

    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def login_view(request):

    if request.method == "POST":

        form = AuthenticationForm(data=request.POST)

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            messages.success(
              request,
                f"Welcome back, {user.username}!"
                )

            return redirect("dashboard")

    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})



@login_required
def dashboard(request):

    files = UploadedFile.objects.filter(user=request.user)

    latest = files.order_by("-upload_date").first()

    total_files = files.count()

    storage = files.aggregate(
        Sum("file_size")
    )["file_size__sum"] or 0

    recent = files.order_by("-upload_date")[:5]

    context = {

    "total_files": total_files,

    "storage": round(storage / 1024, 2),

    "recent": recent,

    "latest": latest,

}

    return render(
        request,
        "dashboard.html",
        context
    )


def logout_view(request):
    logout(request)
    return redirect("home")




@login_required
def profile(request):

    return render(
        request,
        "profile.html"
    )


@login_required
def edit_profile(request):

    if request.method == "POST":

        form = EditProfileForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Profile updated successfully."
            )

            return redirect("profile")

    else:

        form = EditProfileForm(
            instance=request.user
        )

    return render(
        request,
        "edit_profile.html",
        {"form": form}
    )


@login_required
def change_password(request):

    if request.method == "POST":

        form = PasswordChangeForm(
            request.user,
            request.POST
        )

        if form.is_valid():

            user = form.save()

            update_session_auth_hash(
                request,
                user
            )

            messages.success(
                request,
                "Password changed successfully."
            )

            return redirect("profile")

    else:

        form = PasswordChangeForm(
            request.user
        )

    return render(
        request,
        "change_password.html",
        {"form": form}
    )




@staff_member_required
def admin_dashboard(request):

    total_users = User.objects.count()

    total_files = UploadedFile.objects.count()

    total_downloads = UploadedFile.objects.aggregate(
        Sum("download_count")
    )["download_count__sum"] or 0

    storage = UploadedFile.objects.aggregate(
        Sum("file_size")
    )["file_size__sum"] or 0

    top_files = UploadedFile.objects.order_by(
        "-download_count"
    )[:5]

    context = {

        "total_users": total_users,

        "total_files": total_files,

        "total_downloads": total_downloads,

        "storage": round(storage / 1024 / 1024, 2),

        "top_files": top_files,

    }

    return render(
        request,
        "admin_dashboard.html",
        context
    )


