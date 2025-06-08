from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.middleware.csrf import get_token
from .models import Pelicula, PerfilUsuario
from .forms import RegistroForm, LoginForm, PeliculaForm

def home(request):
    """Vista principal del sitio"""
    if request.user.is_authenticated:
        peliculas_count = Pelicula.objects.filter(activa=True).count()
        username = request.user.first_name or request.user.username
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>CinemaMax</title>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background: #1a1a2e; color: white; }}
                .container {{ max-width: 800px; margin: 0 auto; text-align: center; }}
                .btn {{ background: #e94560; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin: 10px; display: inline-block; }}
                .btn:hover {{ background: #d63447; }}
                .btn-secondary {{ background: #6c757d; }}
                .btn-secondary:hover {{ background: #5a6268; }}
                h1 {{ color: #e94560; }}
                .user-info {{ background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🎬 CinemaMax</h1>
                
                <div class="user-info">
                    <h3>¡Bienvenido, {username}! 👋</h3>
                    <p>Sistema de Gestión de Cine</p>
                    <p>Tenemos <strong>{peliculas_count}</strong> películas disponibles</p>
                </div>
                
                <div>
                    <a href="/peliculas/" class="btn">📽️ Ver Películas</a>
                    <a href="/agregar-pelicula/" class="btn">➕ Agregar Película</a>
                    <a href="/admin/" class="btn">⚙️ Administración</a>
                </div>
                
                <div style="margin-top: 30px;">
                    <a href="/logout/" class="btn btn-secondary">🚪 Cerrar Sesión</a>
                </div>
                
                <hr style="margin: 30px 0;">
                <p><em>Evaluación Cloud TIE601 - Cinema Project</em></p>
            </div>
        </body>
        </html>
        """
        return HttpResponse(html)
    else:
        # Usuario no autenticado
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>CinemaMax - Bienvenido</title>
            <meta charset="UTF-8">
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #1a1a2e; color: white; }
                .container { max-width: 800px; margin: 0 auto; text-align: center; }
                .btn { background: #e94560; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin: 10px; display: inline-block; font-size: 16px; }
                .btn:hover { background: #d63447; }
                .btn-outline { background: transparent; border: 2px solid #e94560; }
                .btn-outline:hover { background: #e94560; }
                h1 { color: #e94560; font-size: 3em; margin-bottom: 20px; }
                .hero { background: rgba(255,255,255,0.1); padding: 40px; border-radius: 15px; margin: 30px 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🎬 CinemaMax</h1>
                
                <div class="hero">
                    <h2>¡Bienvenido al Sistema de Gestión de Cine!</h2>
                    <p>Gestiona películas, horarios y mucho más.</p>
                    <p>Para acceder al sistema, necesitas iniciar sesión.</p>
                </div>
                
                <div>
                    <a href="/login/" class="btn">🔑 Iniciar Sesión</a>
                    <a href="/registro/" class="btn btn-outline">📝 Crear Cuenta</a>
                </div>
                
                <hr style="margin: 30px 0;">
                <p><em>Evaluación Cloud TIE601 - Cinema Project</em></p>
            </div>
        </body>
        </html>
        """
        return HttpResponse(html)

def login_view(request):
    """Vista de inicio de sesión"""
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', '/')
                return redirect(next_url)
    else:
        form = LoginForm()
    
    # Obtener CSRF token
    csrf_token = get_token(request)
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Iniciar Sesión - CinemaMax</title>
        <meta charset="UTF-8">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {{ background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); min-height: 100vh; }}
            .card {{ background: rgba(255,255,255,0.1); border: none; }}
            .form-control {{ background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.3); color: white; }}
            .form-control:focus {{ background: rgba(255,255,255,0.2); border-color: #e94560; color: white; box-shadow: none; }}
            .form-control::placeholder {{ color: rgba(255,255,255,0.7); }}
            .btn-primary {{ background: #e94560; border-color: #e94560; }}
            .btn-primary:hover {{ background: #d63447; border-color: #d63447; }}
            h2 {{ color: #e94560; }}
            a {{ color: #e94560; }}
        </style>
    </head>
    <body class="text-white">
        <div class="container">
            <div class="row justify-content-center" style="margin-top: 100px;">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-body p-5">
                            <h2 class="text-center mb-4">🎬 CinemaMax</h2>
                            <h4 class="text-center mb-4">Iniciar Sesión</h4>
                            
                            <form method="post">
                                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                                
                                <div class="mb-3">
                                    <label class="form-label">Usuario</label>
                                    <input type="text" name="username" class="form-control" placeholder="Nombre de usuario" required>
                                </div>
                                
                                <div class="mb-3">
                                    <label class="form-label">Contraseña</label>
                                    <input type="password" name="password" class="form-control" placeholder="Contraseña" required>
                                </div>
                                
                                <div class="d-grid">
                                    <button type="submit" class="btn btn-primary btn-lg">🔑 Iniciar Sesión</button>
                                </div>
                            </form>
                            
                            <hr class="my-4">
                            <div class="text-center">
                                <p>¿No tienes cuenta? <a href="/registro/">Regístrate aquí</a></p>
                                <p><a href="/" style="color: #ccc;">← Volver al inicio</a></p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

def registro_view(request):
    """Vista de registro de usuario"""
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        # Crear usuario manualmente para simplificar
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        if password1 == password2 and len(password1) >= 8:
            from django.contrib.auth.models import User
            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1,
                    first_name=first_name,
                    last_name=last_name
                )
                login(request, user)
                return redirect('/')
            except:
                error_msg = "Error al crear usuario. El nombre de usuario ya existe."
        else:
            error_msg = "Las contraseñas no coinciden o son muy cortas (mínimo 8 caracteres)."
    else:
        error_msg = ""
    
    csrf_token = get_token(request)
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Registro - CinemaMax</title>
        <meta charset="UTF-8">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {{ background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); min-height: 100vh; }}
            .card {{ background: rgba(255,255,255,0.1); border: none; }}
            .form-control {{ background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.3); color: white; }}
            .form-control:focus {{ background: rgba(255,255,255,0.2); border-color: #e94560; color: white; box-shadow: none; }}
            .form-control::placeholder {{ color: rgba(255,255,255,0.7); }}
            .btn-primary {{ background: #e94560; border-color: #e94560; }}
            .btn-primary:hover {{ background: #d63447; border-color: #d63447; }}
            h2 {{ color: #e94560; }}
            a {{ color: #e94560; }}
        </style>
    </head>
    <body class="text-white">
        <div class="container">
            <div class="row justify-content-center" style="margin-top: 50px;">
                <div class="col-md-8">
                    <div class="card">
                        <div class="card-body p-5">
                            <h2 class="text-center mb-4">🎬 CinemaMax</h2>
                            <h4 class="text-center mb-4">Crear Cuenta</h4>
                            
                            {f'<div class="alert alert-danger">{error_msg}</div>' if error_msg else ''}
                            
                            <form method="post">
                                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                                
                                <div class="row">
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Nombre</label>
                                        <input type="text" name="first_name" class="form-control" placeholder="Nombre" required>
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Apellido</label>
                                        <input type="text" name="last_name" class="form-control" placeholder="Apellido" required>
                                    </div>
                                </div>
                                
                                <div class="mb-3">
                                    <label class="form-label">Usuario</label>
                                    <input type="text" name="username" class="form-control" placeholder="Nombre de usuario" required>
                                </div>
                                
                                <div class="mb-3">
                                    <label class="form-label">Email</label>
                                    <input type="email" name="email" class="form-control" placeholder="correo@ejemplo.com" required>
                                </div>
                                
                                <div class="row">
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Contraseña</label>
                                        <input type="password" name="password1" class="form-control" placeholder="Mínimo 8 caracteres" required>
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Confirmar Contraseña</label>
                                        <input type="password" name="password2" class="form-control" placeholder="Repetir contraseña" required>
                                    </div>
                                </div>
                                
                                <div class="d-grid">
                                    <button type="submit" class="btn btn-primary btn-lg">📝 Crear Cuenta</button>
                                </div>
                            </form>
                            
                            <hr class="my-4">
                            <div class="text-center">
                                <p>¿Ya tienes cuenta? <a href="/login/">Inicia sesión aquí</a></p>
                                <p><a href="/" style="color: #ccc;">← Volver al inicio</a></p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

@login_required
def logout_view(request):
    """Vista para cerrar sesión"""
    logout(request)
    return redirect('/')

@login_required
def lista_peliculas(request):
    """Vista para mostrar todas las películas - SOLO USUARIOS AUTENTICADOS"""
    peliculas = Pelicula.objects.filter(activa=True).order_by('-fecha_creacion')
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Películas - CinemaMax</title>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background: #1a1a2e; color: white; }}
            .container {{ max-width: 1200px; margin: 0 auto; }}
            .header {{ text-align: center; margin-bottom: 30px; }}
            .pelicula {{ background: rgba(255,255,255,0.1); padding: 20px; margin: 15px 0; border-radius: 10px; }}
            .titulo {{ color: #e94560; font-size: 1.5em; margin-bottom: 10px; }}
            .info {{ color: #ccc; margin: 5px 0; }}
            .precio {{ color: #4ecca3; font-weight: bold; font-size: 1.2em; }}
            .btn {{ background: #e94560; color: white; padding: 8px 15px; text-decoration: none; border-radius: 5px; margin: 5px; }}
            .btn:hover {{ background: #d63447; }}
            .btn-secondary {{ background: #6c757d; }}
            .user-bar {{ background: rgba(255,255,255,0.1); padding: 10px; border-radius: 5px; margin-bottom: 20px; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="user-bar">
                👤 {request.user.first_name or request.user.username} | 
                <a href="/" class="btn">🏠 Inicio</a>
                <a href="/agregar-pelicula/" class="btn">➕ Agregar</a>
                <a href="/admin/" class="btn">⚙️ Admin</a>
                <a href="/logout/" class="btn btn-secondary">🚪 Salir</a>
            </div>
            
            <div class="header">
                <h1 style="color: #e94560;">🎭 Cartelera de Películas</h1>
                <p>Total: {peliculas.count()} películas disponibles</p>
            </div>
    """
    
    if peliculas:
        for pelicula in peliculas:
            html += f"""
            <div class="pelicula">
                <div class="titulo">{pelicula.titulo}</div>
                <div class="info">👨‍🎬 Director: {pelicula.director}</div>
                <div class="info">📅 Año: {pelicula.año}</div>
                <div class="info">⏱️ Duración: {pelicula.duracion} minutos</div>
                <div class="info">📝 {pelicula.sinopsis[:200]}{'...' if len(pelicula.sinopsis) > 200 else ''}</div>
                <div class="precio">💰 Precio: ${pelicula.precio}</div>
                <div class="info" style="font-size: 0.9em; margin-top: 10px;">
                    Agregada por: {pelicula.creada_por.username} | {pelicula.fecha_creacion.strftime('%d/%m/%Y')}
                </div>
            </div>
            """
    else:
        html += """
        <div style="text-align: center; padding: 50px;">
            <h3>😔 No hay películas disponibles</h3>
            <p>¡Sé el primero en agregar una película!</p>
            <a href="/agregar-pelicula/" class="btn">➕ Agregar Primera Película</a>
        </div>
        """
    
    html += """
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

@login_required
def agregar_pelicula(request):
    """Vista para agregar nueva película - SOLO USUARIOS AUTENTICADOS"""
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        director = request.POST.get('director')
        año = request.POST.get('año')
        duracion = request.POST.get('duracion')
        sinopsis = request.POST.get('sinopsis')
        precio = request.POST.get('precio')
        activa = request.POST.get('activa') == 'on'
        
        try:
            pelicula = Pelicula.objects.create(
                titulo=titulo,
                director=director,
                año=int(año),
                duracion=int(duracion),
                sinopsis=sinopsis,
                precio=float(precio),
                activa=activa,
                creada_por=request.user
            )
            return redirect('/peliculas/')
        except:
            error_msg = "Error al guardar la película. Verifica los datos."
    else:
        error_msg = ""
    
    csrf_token = get_token(request)
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Agregar Película - CinemaMax</title>
        <meta charset="UTF-8">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {{ background: #1a1a2e; color: white; }}
            .card {{ background: rgba(255,255,255,0.1); border: none; }}
            .form-control {{ background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.3); color: white; }}
            .form-control:focus {{ background: rgba(255,255,255,0.2); border-color: #e94560; color: white; box-shadow: none; }}
            .form-control::placeholder {{ color: rgba(255,255,255,0.7); }}
            .btn-primary {{ background: #e94560; border-color: #e94560; }}
            .btn-primary:hover {{ background: #d63447; border-color: #d63447; }}
            h2 {{ color: #e94560; }}
        </style>
    </head>
    <body>
        <div class="container mt-5">
            <div class="row justify-content-center">
                <div class="col-md-8">
                    <div class="card">
                        <div class="card-body p-4">
                            <h2 class="text-center mb-4">🎬 Agregar Nueva Película</h2>
                            
                            {f'<div class="alert alert-danger">{error_msg}</div>' if error_msg else ''}
                            
                            <form method="post">
                                <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                                
                                <div class="row">
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Título</label>
                                        <input type="text" name="titulo" class="form-control" placeholder="Título de la película" required>
                                    </div>
                                    <div class="col-md-6 mb-3">
                                        <label class="form-label">Director</label>
                                        <input type="text" name="director" class="form-control" placeholder="Director" required>
                                    </div>
                                </div>
                                
                                <div class="row">
                                    <div class="col-md-4 mb-3">
                                        <label class="form-label">Año</label>
                                        <input type="number" name="año" class="form-control" placeholder="2024" min="1900" max="2030" required>
                                    </div>
                                    <div class="col-md-4 mb-3">
                                        <label class="form-label">Duración (min)</label>
                                        <input type="number" name="duracion" class="form-control" placeholder="120" min="1" required>
                                    </div>
                                    <div class="col-md-4 mb-3">
                                        <label class="form-label">Precio</label>
                                        <input type="number" name="precio" class="form-control" placeholder="12.50" step="0.01" min="0" required>
                                    </div>
                                </div>
                                
                                <div class="mb-3">
                                    <label class="form-label">Sinopsis</label>
                                    <textarea name="sinopsis" class="form-control" rows="4" placeholder="Descripción de la película..." required></textarea>
                                </div>
                                
                                <div class="mb-3 form-check">
                                    <input type="checkbox" name="activa" class="form-check-input" id="activa" checked>
                                    <label class="form-check-label" for="activa">Película activa</label>
                                </div>
                                
                                <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                                    <a href="/peliculas/" class="btn btn-secondary">Cancelar</a>
                                    <button type="submit" class="btn btn-primary">💾 Guardar Película</button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)