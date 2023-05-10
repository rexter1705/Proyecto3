from django.shortcuts import redirect, render
from django.core.exceptions import ValidationError
from .forms import UploadFileForm, EditForm
from .models import UploadFile
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import render, HttpResponse





@login_required
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            doc=form.files.get('file')

            if not doc.name.endswith('.p2'):
                messages.error(request, 'El archivo debe tener la extensión .p2')
                return redirect('upload_file')

            arch=UploadFile.objects.create(file=doc) 

            h = open(arch.file.path,'r',encoding='utf-8')

            content=h.read()

            arch.text=content

            arch.save()
            messages.success(request, f"Se ha guardado exitosamente el documento!")
            return redirect('home')
    else:
        form = UploadFileForm()
        context = {
            'form':form,
        }
    return render(request, 'upload_file.html', context)


@login_required
def file_list(request):
    files = UploadFile.objects.all()

    return render(request, 'repositorio.html', {'files': files})


def edit(request, pk):
    file = get_object_or_404(UploadFile, pk=pk)

    if request.method == 'POST':
        form = EditForm(request.POST, instance=file)
        if form.is_valid():
            h = open(file.file.path,'w',encoding='utf-8')
            content=form.cleaned_data.get('text')
            h.write(content)
            file.text=content
            file.save()
            return redirect('repositorio')
    else:
        form = EditForm(instance=file)

    return render(request, 'edit.html', {'form': form})


