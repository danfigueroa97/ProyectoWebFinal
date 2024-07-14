from django.shortcuts import render
from .models import Respuesta, Multimedia, UserList, Comentario
from .forms import RespuestaForm, NuevoUsuarioForm, MultimediaForm, ComentarioForm, UpdateUsuarioForm
from django.contrib.auth import login
import datetime
from django.contrib import messages
from django.shortcuts import redirect
from django.template import loader
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .forms import SearchForm
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required



# Create your views here.

def index(request):
    return render(request, 'index.html')

def peliculas(request):
    multimedia = Multimedia.objects.all()
    return render(request, 'peliculas.html',{
        'multimedia' : multimedia
    })

def series(request):
    multimedia = Multimedia.objects.all()
    return render(request, 'series.html',{
        'multimedia' : multimedia
    })

def inicio(request):
    multimedia = Multimedia.objects.all()
    return render(request, 'inicio.html',{
        'multimedia' : multimedia
    })

def registro(request):
    if request.method == "POST":
        form = NuevoUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registro Exitoso")
            return redirect('login')
        else:
            # Agregar esta parte para ver los errores del formulario
            for field, errors in form.errors.items():
                messages.error(request, f"{field}: {', '.join(errors)}")
    else:
        form = NuevoUsuarioForm()

    context = {"register_form": form}
    return render(request, "registration/registro.html", context)

def login_view(request):
    return render(request, 'registration/login.html')

def multimedia(request, idMultimedia):
    multimedia = Multimedia.objects.get(id=idMultimedia)
    return render(request, 'multimedia.html',{'multimedia':multimedia})

def verMultimedia(request, idMultimedia):
    multimedia = Multimedia.objects.get(id=idMultimedia)
    return render(request,'crud1/ver.html',{'multimedia':multimedia})

def crearMultimedia(request):
    if request.method == 'POST':
        form = MultimediaForm(request.POST, request.FILES)  
        if form.is_valid():
            form.save()
            return redirect('crud1')  
    else:
        form = MultimediaForm()
    return render(request, 'crud1/nuevo.html', {'form': form})

def listaMultimedia(request):
    multimedia = Multimedia.objects.all()
    return render(request, 'crud1/crud1.html',{
        'multimedia' : multimedia
    })

class updateMultimedia(UpdateView):
    template_name = 'crud1/update.html'
    model = Multimedia
    fields=['Nombre','Descripcion','Imagen','categoria','Link']

    def get_success_url(self):
        return reverse_lazy('crud1')


class deleteMultimedia(DeleteView):
    template_name ='crud1/borrar.html'
    model= Multimedia
    
    def get_success_url(self):
        return reverse_lazy('crud1')

def buscar_multimedia(request):
    form = SearchForm()
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Multimedia.objects.filter(Nombre__icontains=query)
    return render(request, 'buscar.html', {'form': form, 'results': results})

@login_required
def add_to_list(request, multimedia_id):
    multimedia = get_object_or_404(Multimedia, id=multimedia_id)
    UserList.objects.create(user=request.user, multimedia=multimedia)
    return redirect('mi_lista')

@login_required
def remove_from_list(request, multimedia_id):
    multimedia = get_object_or_404(Multimedia, id=multimedia_id)
    UserList.objects.filter(user=request.user, multimedia=multimedia).delete()
    return redirect('mi_lista')

@login_required
def mi_lista(request):
    lista = UserList.objects.filter(user=request.user)
    return render(request, 'mi_lista.html', {'lista': lista})

def multimedia(request, idMultimedia):
    multimedia = get_object_or_404(Multimedia, id=idMultimedia)
    comentarios = Comentario.objects.filter(multimedia=multimedia).order_by('-fecha_creacion')
    form = ComentarioForm()

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = request.user
            comentario.multimedia = multimedia
            comentario.save()
            return redirect('multimedia', idMultimedia=idMultimedia)

    return render(request, 'multimedia.html', {
        'multimedia': multimedia,
        'comentarios': comentarios,
        'form': form,
    })

@login_required
def borrar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    # Verificar si el usuario tiene permisos para borrar el comentario (opcional)
    if request.user == comentario.usuario or request.user.is_superuser:
        if request.method == 'POST':
            comentario.delete()
            return redirect('multimedia', idMultimedia=comentario.multimedia.id)
    return redirect('inicio')  # Redirigir a donde sea apropiado después de borrar el comentario

#crud2

# Vista para listar todas las respuestas
def crud2(request):
    comentarios = Comentario.objects.all()
    respuestas = Respuesta.objects.all()
    if not respuestas:
        return HttpResponseNotFound('No hay respuestas disponibles.')
    
    return render(request, 'crud2/crud2.html', {'comentarios': comentarios})


# Vista para agregar una nueva respuesta
def agregar_respuesta(request, comentario_id):
    comentario = get_object_or_404(Comentario, pk=comentario_id)
    multimedia = comentario.multimedia
    if request.method == 'POST':
        form = RespuestaForm(request.POST)
        if form.is_valid():
            respuesta = form.save(commit=False)
            respuesta.comentario = comentario
            respuesta.multimedia = multimedia
            respuesta.save()
            return redirect('crud2')  # Redirigir a la lista de comentarios y respuestas
    else:
        form = RespuestaForm()
    
    return render(request, 'crud2/agregar_respuesta.html', {'form': form})

# Vista para ver los detalles de una respuesta
def ver_respuesta(request, pk):
    respuesta = get_object_or_404(Respuesta, pk=pk)
    return render(request, 'crud2/ver_respuesta.html', {'respuesta': respuesta})


# Vista para actualizar una respuesta existente
def update_respuesta(request, pk):
    respuesta = get_object_or_404(Respuesta, pk=pk)
    if request.method == "POST":
        form = RespuestaForm(request.POST, instance=respuesta)
        if form.is_valid():
            form.save()
            return redirect('crud2')  # Redirigir a la lista de comentarios y respuestas
    else:
        form = RespuestaForm(instance=respuesta)
    return render(request, 'crud2/update_respuesta.html', {'form': form})


# Vista para borrar una respuesta
def borrar_respuesta(request, pk):
    print(f"Intentando borrar respuesta con pk: {pk}")
    respuesta = get_object_or_404(Respuesta, pk=pk)
    if request.method == "POST":
        respuesta.delete()
        return redirect('crud2')  # Redirigir a la lista de comentarios y respuestas
    return render(request, 'crud2/borrar_respuesta.html', {'respuesta': respuesta})

#fincrud2


#crud3
def registro(request):
    if request.method == "POST":
        form = NuevoUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registro Exitoso")
            return redirect('login')
        else:
            # Agregar esta parte para ver los errores del formulario
            for field, errors in form.errors.items():
                messages.error(request, f"{field}: {', '.join(errors)}")
    else:
        form = NuevoUsuarioForm()

    context = {"register_form": form}
    return render(request, "registration/registro.html", context)

def verUser(request):
    usuarios = User.objects.all()
    return render(request, 'crud3/listaUser.html', {'usuarios': usuarios})

def detallesUser(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    return render(request, 'crud3/detallesUser.html', {'usuario': usuario})

def updateUser(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        form = UpdateUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario actualizado con éxito")
            return redirect('detallesUser', user_id=usuario.id)
        else:
            messages.error(request, "No se pudo actualizar el usuario. Por favor, revisa el formulario.")
    else:
        form = UpdateUsuarioForm(instance=usuario)

    return render(request, 'crud3/updateUser.html', {'form': form})

def deleteUser(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        usuario.delete()
        messages.success(request, "Usuario eliminado con éxito")
        return redirect('verUser')


    return render(request, 'crud3/deleteUser.html', {'usuario': usuario})

#fin crud3