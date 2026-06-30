# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from .forms import UploadFileForm
# from .models import UploadedFile
# from django.shortcuts import get_object_or_404
# from django.http import FileResponse
# from django.db.models import Sum


# @login_required
# def upload_file(request):

#     if request.method == "POST":

#         form = UploadFileForm(request.POST, request.FILES)

#         if form.is_valid():

#             uploaded = form.save(commit=False)

#             uploaded.user = request.user
#             uploaded.original_name = request.FILES["file"].name
#             uploaded.file_size = request.FILES["file"].size

#             uploaded.save()

#             return redirect("myfiles")

#     else:

#         form = UploadFileForm()

#     return render(request, "upload.html", {"form": form})


# @login_required
# def my_files(request):

#     files = UploadedFile.objects.filter(user=request.user)

#     return render(request, "myfiles.html", {"files": files})






# @login_required
# def download_file(request, file_id):
#     uploaded_file = get_object_or_404(
#         UploadedFile,
#         id=file_id,
#         user=request.user
#     )

#     uploaded_file.download_count += 1
#     uploaded_file.save()

#     return FileResponse(
#         uploaded_file.file.open("rb"),
#         as_attachment=True,
#         filename=uploaded_file.original_name
#     )


# @login_required
# def delete_file(request, file_id):
#     uploaded_file = get_object_or_404(
#         UploadedFile,
#         id=file_id,
#         user=request.user
#     )

#     uploaded_file.file.delete()

#     uploaded_file.delete()

#     return redirect("myfiles")


# from django.db.models import Q

# @login_required
# def my_files(request):

#     search = request.GET.get("search", "")

#     files = UploadedFile.objects.filter(user=request.user)

#     if search:
#         files = files.filter(original_name__icontains=search)

#     for file in files:

#         name = file.original_name.lower()

#         if name.endswith(".pdf"):
#             file.icon = "📄"

#         elif name.endswith((".png", ".jpg", ".jpeg", ".gif")):
#             file.icon = "🖼️"

#         elif name.endswith((".doc", ".docx")):
#             file.icon = "📝"

#         elif name.endswith(".zip"):
#             file.icon = "📦"

#         elif name.endswith(".mp3"):
#             file.icon = "🎵"

#         elif name.endswith(".mp4"):
#             file.icon = "🎥"

#         else:
#             file.icon = "📁"

#     context = {
#         "files": files,
#         "search": search,
#     }

#     return render(request, "myfiles.html", context)




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.contrib import messages
from .forms import UploadFileForm
from .models import UploadedFile
from django.http import Http404

from django.core.mail import send_mail
from django.conf import settings

from django.http import HttpResponse
from django.utils import timezone

@login_required
def upload_file(request):

    if request.method == "POST":

        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():

            uploaded = form.save(commit=False)

            uploaded.user = request.user
            uploaded.original_name = request.FILES["file"].name
            uploaded.file_size = request.FILES["file"].size


            uploaded.save()

            messages.success(
                request,
                "File uploaded successfully!"
            )

            return redirect("myfiles")
            

    else:
        form = UploadFileForm()

    return render(request, "upload.html", {"form": form})


@login_required
def my_files(request):

    search = request.GET.get("search", "")

    files = UploadedFile.objects.filter(user=request.user)

    if search:
        files = files.filter(original_name__icontains=search)

    for file in files:

        name = file.original_name.lower()

        if name.endswith(".pdf"):
            file.icon = "📄"

        elif name.endswith((".png", ".jpg", ".jpeg", ".gif")):
            file.icon = "🖼️"

        elif name.endswith((".doc", ".docx")):
            file.icon = "📝"

        elif name.endswith(".zip"):
            file.icon = "📦"

        elif name.endswith(".mp3"):
            file.icon = "🎵"

        elif name.endswith(".mp4"):
            file.icon = "🎥"

        else:
            file.icon = "📁"

    context = {
        "files": files,
        "search": search,
    }

    return render(request, "myfiles.html", context)


@login_required
def download_file(request, file_id):

    uploaded_file = get_object_or_404(
        UploadedFile,
        id=file_id,
        user=request.user
    )

    uploaded_file.download_count += 1
    uploaded_file.save()

    return FileResponse(
        uploaded_file.file.open("rb"),
        as_attachment=True,
        filename=uploaded_file.original_name
    )


@login_required
def delete_file(request, file_id):

    uploaded_file = get_object_or_404(
        UploadedFile,
        id=file_id,
        user=request.user
    )

    uploaded_file.file.delete()

    uploaded_file.delete()

    messages.success(
    request,
    "File deleted successfully!"
    )

    return redirect("myfiles")



def share_file(request, token):

    uploaded_file = get_object_or_404(
        UploadedFile,
        share_token=token
    )

    # Check expiry
    if timezone.now() > uploaded_file.expiry_date:
        return HttpResponse(
            "<h2>This sharing link has expired.</h2>",
            status=403
        )

    # Send email
    if request.method == "POST" and "email" in request.POST:

        email = request.POST["email"]

        link = (
            f"{request.scheme}://"
            f"{request.get_host()}/share/"
            f"{uploaded_file.share_token}/"
        )

        send_mail(
            subject="File Shared With You",

            message=(
                f"Hello,\n\n"
                f"A file has been shared with you.\n\n"
                f"Download here:\n{link}\n\n"
                f"This link expires on:\n"
                f"{uploaded_file.expiry_date}"
            ),

            from_email=settings.DEFAULT_FROM_EMAIL,

            recipient_list=[email],

            fail_silently=False,
        )

        return render(
            request,
            "share_file.html",
            {
                "file": uploaded_file,
                "success": True,
            },
        )

    # Download file
    if request.method == "POST":

        uploaded_file.download_count += 1
        uploaded_file.save(update_fields=["download_count"])

        return FileResponse(
            uploaded_file.file.open("rb"),
            as_attachment=True,
            filename=uploaded_file.original_name
        )

    # Display share page
    return render(
        request,
        "share_file.html",
        {
            "file": uploaded_file,
        }
    )