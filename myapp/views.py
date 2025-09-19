from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ClienteForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Cliente, Isla,IslaPremium, Postre, MesaDulcePremium, Extra, Show, EleccionFinDeFiesta,Cantidades, EleccionRecepcion,Telefono, BarraTragos

# Create your views here.
def login_view(request):
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # 🔹 Crear perfil si no existe ANTES de loguear
            PerfilUsuario.objects.get_or_create(user=user)

            login(request, user)
            return redirect("inicio")

        else:
            messages.error(request, "Usuario o contraseña incorrectos")

    return render(request, "login.html")


# -------------------------------
# LOGOUT
# -------------------------------
def logout_view(request):
    logout(request)
    return redirect("login")


# -------------------------------
# LISTA DE CLIENTES
# -------------------------------
@login_required
def lista_clientes(request):
    clientes = Cliente.objects.all()

    # 🔹 Evitar errores si user no tiene perfil
    perfil = getattr(request.user, "perfilusuario", None)

    return render(request, 'lista.html', {
        'clientes': clientes,
        'perfil': perfil
    })


# -------------------------------
# CREAR CLIENTE
# -------------------------------

# -------------------------------
# EDITAR CLIENTE
# -------------------------------
@login_required
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    mensaje = ""

    if request.method == "POST":
        nombre = request.POST.get("nombre")
        dni = request.POST.get("dni")
        # Actualizar campos si se enviaron
        if nombre: cliente.nombre = nombre
        if dni: cliente.dni = dni
        cliente.save()
        mensaje = "Cliente actualizado correctamente"

    return render(request, "editar_cliente.html", {
        "cliente": cliente,
        "mensaje": mensaje
    })

from .models import Cliente, Plan, EleccionBebidas, EleccionVinos, EleccionChoperas

# ===== Planes =====
PLANES_POSIBLES = ["Plan Plata", "Plan Oro Viejo", "ALL INCLUSIVE", "Plan Oro Nuevo"]

@login_required
def elegir_plan(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.method == 'POST':
        plan_seleccionado = request.POST.get('plan')

        # Borrar plan anterior
        cliente.plan.all().delete()

        # Guardar nuevo plan
        Plan.objects.create(cliente=cliente, nombre=plan_seleccionado)

        # Redirigir al siguiente paso (bebidas)
        return redirect('elegir_bebidas', cliente_id=cliente.id)

    # Obtener el plan previamente seleccionado
    plan_elegido = cliente.plan.values_list('nombre', flat=True).first()  # solo uno

    return render(request, 'elegir_plan.html', {
        'cliente': cliente,
        'planes_posibles': PLANES_POSIBLES,
        'plan_elegido': plan_elegido,
    })



# ===== Bebidas / Vinos / Choperas =====
BEBIDAS_POSIBLES = ["Primera Lineas", "Segunda Linea"]
VINOS_POSIBLES = ["Primera Lineas", "Segunda Linea "]
CHOPERAS_SABORES = ["Sin Chopera", "Chopera 30", "Chopera 40", "Chopera 50", "Otro"]

@login_required
def elegir_bebidas(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.method == 'POST':
        # Bebidas
        bebida_seleccionada = request.POST.get('bebidas')

        # Vinos
        vino_seleccionado = request.POST.get('vinos')
        observacion_vinos = request.POST.get('observacion_vinos', '').strip()

        # Choperas
        chopera_seleccionada = request.POST.get('choperas')
        otro_sabor = request.POST.get('otro_sabor', '').strip()
        observacion_choperas = request.POST.get('observacion_choperas', '').strip()

        # Limpiar elecciones anteriores
        cliente.bebidas.all().delete()
        cliente.vinos.all().delete()
        cliente.choperas.all().delete()

        # Guardar Bebida
        if bebida_seleccionada:
            EleccionBebidas.objects.create(cliente=cliente, nombre=bebida_seleccionada)

        # Guardar Vino
        if vino_seleccionado:
            EleccionVinos.objects.create(
                cliente=cliente,
                nombre=vino_seleccionado,
                observacion=observacion_vinos if observacion_vinos else None
            )

        # Guardar Chopera
        if chopera_seleccionada:
            sabor_final = chopera_seleccionada
            if chopera_seleccionada.lower() == "otro" and otro_sabor:
                sabor_final = otro_sabor

            EleccionChoperas.objects.create(
                cliente=cliente,
                sabor=sabor_final,
                observacion=observacion_choperas if observacion_choperas else None
            )

        return redirect('elegir_islas', cliente_id=cliente.id)

    # Selecciones previas
    bebida_prev = cliente.bebidas.first()
    vino_prev = cliente.vinos.first()
    chopera_prev = cliente.choperas.first()
    otro_chopera_prev = None
    if chopera_prev:
        if chopera_prev.sabor not in CHOPERAS_SABORES:
            otro_chopera_prev = chopera_prev.sabor

    return render(request, 'elegir_bebidas.html', {
        'cliente': cliente,
        'bebidas_posibles': BEBIDAS_POSIBLES,
        'vinos_posibles': VINOS_POSIBLES,
        'choperas_posibles': CHOPERAS_SABORES,
        'bebida_prev': bebida_prev.nombre if bebida_prev else None,
        'vino_prev': vino_prev.nombre if vino_prev else None,
        'observacion_vinos_prev': vino_prev.observacion if vino_prev else '',
        'chopera_prev': chopera_prev.sabor if chopera_prev else None,
        'otro_chopera_prev': otro_chopera_prev,
        'observacion_chopera_prev': chopera_prev.observacion if chopera_prev else '',
    })
from datetime import datetime

from datetime import datetime
from .models import Cliente

@login_required
def crear_cliente(request):
    salon = [
        "Varela", "Varela II", "Berazategui", "Monteverde", "París",
        "Dream's", "Melody", "Luxor", "Bernal", "Sol Fest",
        "Clahe", "Onix", "Auguri", "Dominico II", "Gala", "Sarandí II",
        "Garufa", "Lomas", "Temperley", "Clahe Escalada", "Piñeyro", "Monte Grande",
    ]

    if request.method == 'POST':
        dni = request.POST.get('dni')
        nombre = request.POST.get('nombre')
        fecha_evento_str = request.POST.get('fecha_evento')  # viene en formato YYYY-MM-DD
        horario_evento_str = request.POST.get('horario')
        tipo_evento = request.POST.get('tipo_evento')
        salon_seleccionado = request.POST.get('salon')

        # Convertir fecha a objeto date
        try:
            fecha_evento = datetime.strptime(fecha_evento_str, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "Formato de fecha inválido. Usa AAAA-MM-DD.")
            return render(request, 'crear.html', {
                'dni': dni,
                'nombre': nombre,
                'fecha_evento': fecha_evento_str,
                'tipo_evento': tipo_evento,
                'horario': horario_evento_str,
                'salon': salon,
                'salon_seleccionado': salon_seleccionado,
            })

        # Convertir horario a objeto time
        try:
            horario_evento = datetime.strptime(horario_evento_str, "%H:%M").time()
        except ValueError:
            messages.error(request, "Formato de horario inválido. Usa HH:MM en 24h.")
            return render(request, 'crear.html', {
                'dni': dni,
                'nombre': nombre,
                'fecha_evento': fecha_evento_str,
                'tipo_evento': tipo_evento,
                'horario': horario_evento_str,
                'salon': salon,
                'salon_seleccionado': salon_seleccionado,
            })

       

        # Guardar cliente
        cliente = Cliente(
            dni=dni,
            nombre=nombre,
            fecha_evento=fecha_evento,
            horario_evento=horario_evento,
            tipo_evento=tipo_evento,
            salon=salon_seleccionado,
        )
        cliente.save()

        return redirect('agregar_telefonos', cliente_id=cliente.id)

    return render(request, 'crear.html', {
        'salon': salon
    })
@login_required
def agregar_telefonos(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    telefono, created = Telefono.objects.get_or_create(cliente=cliente)

    if request.method == 'POST':
        telefono.numero1 = request.POST.get('numero1')
        telefono.numero2 = request.POST.get('numero2')
        telefono.save()
        return redirect('elegir_plan', cliente_id=cliente.id)

    return render(request, 'agregar_telefonos.html', {
        'cliente': cliente,
        'numero1': telefono.numero1,
        'numero2': telefono.numero2,
    })

ISLAS_POSIBLES = [
    "Isla Italiana",
    "Isla Criolla",
    "Isla Mexicana",
    # agregá todas las opciones que quieras
]
@login_required
def elegir_islas(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.method == 'POST':
        islas_seleccionadas = request.POST.getlist('islas')  # lista de nombres de islas

        # Borrar anteriores
        cliente.islas.all().delete()

        for nombre_isla in islas_seleccionadas:
            Isla.objects.create(cliente=cliente, nombre=nombre_isla)

        return redirect('elegir_islas_premium', cliente_id=cliente.id)

    # Obtener nombres de islas previamente seleccionadas
    islas_elegidas = cliente.islas.values_list('nombre', flat=True)

    return render(request, 'elegir_islas.html', {
        'cliente': cliente,
        'islas_posibles': ISLAS_POSIBLES,
        'islas_elegidas': islas_elegidas,  # ← le pasás las seleccionadas
    })

ISLAS_PREMIUM_POSIBLES = [
    "Isla Campestre",
    "Isla Cheddar",
    "Isla Japonesa",
    "Isla de Mar",
    "Isla Teen",
    "Isla de Pastas",
]

@login_required
def elegir_islas_premium(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.method == 'POST':
        islas_premium_seleccionadas = request.POST.getlist('islas_premium')

        # Borrar previas elecciones de Islas Premium para ese cliente
        cliente.islas_premium.all().delete()

        for nombre in islas_premium_seleccionadas:
            IslaPremium.objects.create(cliente=cliente, nombre=nombre)

        return redirect('elegir_barra_tragos', cliente_id=cliente.id)

    # Obtener las islas premium ya elegidas
    islas_premium_elegidas = list(cliente.islas_premium.values_list('nombre', flat=True))

    return render(request, 'elegir_islas_premium.html', {
        'cliente': cliente,
        'islas_premium_posibles': ISLAS_PREMIUM_POSIBLES,
        'islas_premium_elegidas': islas_premium_elegidas,
    })
    
@login_required
def elegir_cantidades(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    # Obtener la cantidad actual si existe
    cantidad_actual = cliente.cantidades.first().cantidad if cliente.cantidades.exists() else 0

    if request.method == 'POST':
        cantidad_valor = int(request.POST.get('cantidad', 0))

        # Borrar la cantidad anterior y guardar la nueva
        cliente.cantidades.all().delete()
        Cantidades.objects.create(cliente=cliente, cantidad=cantidad_valor)

        return redirect('elegir_plan', cliente_id=cliente.id)

    return render(request, 'elegir_cantidad.html', {
        'cliente': cliente,
        'cantidad_actual': cantidad_actual,
    })
    
    
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.db import OperationalError
import time
from .models import Cliente, Eleccion_Platos

# Lista de platos con variantes opcionales
PLATOS_PRINCIPALES = [
    {
        "nombre": "Milanesa napolitana",
        "opciones": {
            "Carne": ["Ternera", "Pollo"],
            "acompanamiento": ["Ensalada rusa", "Papas españolas", "Papas rústicas", "Arroz primavera"]
        }
    },
    {
        "nombre": "Pollo al verdeo",
        "opciones": {
            "acompanamiento": ["Papas españolas", "Papas rústicas"]
        }
    },
    {
        "nombre": "Pastas",
        "opciones": {
            "tipo_pasta": ["Ñoquis", "Ravioles", "Fideos caseros"],
            "salsa": ["Boloñesa", "Salsa blanca", "Salsa roja"]
        }
    },
    {
        "nombre": "Carré de cerdo / Bondiola",
        "opciones": {
            "guarnicion": ["Puré batata", "Puré papa", "Puré calabaza", "Puré mixto"]
        }
    },
    {
        "nombre": "Corte de ternera",
        "opciones": {
            "acompanamiento": ["Papas españolas", "Papas rústicas", "Arroz primavera"]
        }
    },
]

PLATOS_INFANTILES = [
    {"nombre": "Milanesa ", "opciones": {"acompanamiento": ["Papas fritas", "Puré"]}},
    {"nombre": "Cheeseburger con papas fritas",  "opciones": None},
    {"nombre": "Medallón de pollo crispy con papas fritas", "opciones": None},
    {"nombre": "Nuggets con papas fritas", "opciones": None},
]

@login_required
def elegir_platos(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    eleccion, _ = Eleccion_Platos.objects.get_or_create(cliente=cliente)

    if request.method == 'POST':
        # --- Plato principal ---
        plato_principal = request.POST.get('plato_principal', '')
        opciones_principal = []

        plato_def = next((p for p in PLATOS_PRINCIPALES if p["nombre"] == plato_principal), None)
        if plato_def:
            for opcion_key in plato_def["opciones"].keys():
                field_name = f"op_{opcion_key}"
                if field_name in request.POST:
                    opciones_principal.append(f"{opcion_key}: {request.POST[field_name]}")

        plato_principal_completo = f"{plato_principal} ({', '.join(opciones_principal)})" if opciones_principal else plato_principal

        # --- Plato infantil ---
        plato_infantil = request.POST.get('plato_infantil', '')
        opciones_infantil = []

        plato_inf_def = next((p for p in PLATOS_INFANTILES if p["nombre"] == plato_infantil), None)
        if plato_inf_def and plato_inf_def["opciones"]:
            for opcion_key in plato_inf_def["opciones"].keys():
                field_name = f"op_inf_{opcion_key}"
                if field_name in request.POST:
                    opciones_infantil.append(f"{opcion_key}: {request.POST[field_name]}")

        plato_infantil_completo = f"{plato_infantil} ({', '.join(opciones_infantil)})" if opciones_infantil else plato_infantil

        # --- Otros campos ---
        aclaraciones = request.POST.get('aclaraciones', '').strip()
        num_adultos = request.POST.get('num_adultos')
        num_ninos = request.POST.get('num_ninos')

        # Guardar datos
        eleccion.plato_principal = plato_principal_completo or None
        eleccion.plato_infantil = plato_infantil_completo or None
        eleccion.aclaraciones_alimentarias = aclaraciones
        eleccion.num_adultos = int(num_adultos) if num_adultos else None
        eleccion.num_ninos = int(num_ninos) if num_ninos else None

        # Guardado seguro con reintentos
        for _ in range(5):
            try:
                eleccion.save()
                break
            except OperationalError:
                time.sleep(0.1)

        return redirect('elegir_postres', cliente_id=cliente.id)

    # --- Preparar opciones seleccionadas ---
    opciones_seleccionadas = {}
    main_name = ''
    if eleccion.plato_principal:
        if '(' in eleccion.plato_principal:
            main_name, opts = eleccion.plato_principal.split('(', 1)
            main_name = main_name.strip()
            opts = opts.rstrip(')')
            for opt in opts.split(','):
                key, val = opt.split(':', 1)
                opciones_seleccionadas[key.strip()] = val.strip()
        else:
            main_name = eleccion.plato_principal

    opciones_infantiles_seleccionadas = {}
    inf_name = ''
    if eleccion.plato_infantil:
        if '(' in eleccion.plato_infantil:
            inf_name, opts = eleccion.plato_infantil.split('(', 1)
            inf_name = inf_name.strip()
            opts = opts.rstrip(')')
            for opt in opts.split(','):
                key, val = opt.split(':', 1)
                opciones_infantiles_seleccionadas[key.strip()] = val.strip()
        else:
            inf_name = eleccion.plato_infantil

    context = {
        'cliente': cliente,
        'platos_principales': PLATOS_PRINCIPALES,
        'platos_infantiles': PLATOS_INFANTILES,
        'elegido_principal': main_name,
        'elegido_infantil': inf_name,
        'opciones_seleccionadas': opciones_seleccionadas,
        'opciones_infantiles_seleccionadas': opciones_infantiles_seleccionadas,
        'aclaraciones': eleccion.aclaraciones_alimentarias,
        'num_adultos': eleccion.num_adultos,
        'num_ninos': eleccion.num_ninos,
    }
    return render(request, 'elegir_platos.html', context)
    
POSTRES_POSIBLES = [
    "Copa helada",
    "Coctel de frutas",
    "Flan con crema o dulce de leche",
    "Brownie con helado",
    "Shot de mousse",
    "Durazno con crema",
]
@login_required
def elegir_postres(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.method == 'POST':
        postres_seleccionados = request.POST.getlist('postres')

        # ✅ IMPORTANTE: borramos los anteriores solo del cliente actual
        cliente.postres.all().delete()

        for nombre in postres_seleccionados:
            Postre.objects.create(cliente=cliente, nombre=nombre)

        return redirect('elegir_mesa_dulce_premium', cliente_id=cliente.id)

    # 🟢 Seleccionamos los nombres de postres que ya eligió este cliente
    postres_ya_elegidos = cliente.postres.values_list('nombre', flat=True)

    return render(request, 'elegir_postres.html', {
        'cliente': cliente,
        'postres_posibles': POSTRES_POSIBLES,
        'postres_seleccionados': postres_ya_elegidos,
    })


MESA_DULCE_PREMIUM_POSIBLES = [
    "Isla Dulce",
    "Isla Cascada de Chocolate",
    "Isla de Tentaciones Dulces",
    "Café y Té",
]
@login_required
def elegir_mesa_dulce_premium(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.method == 'POST':
        opciones_seleccionadas = request.POST.getlist('mesa_dulce_premium')

        # Borrar anteriores
        cliente.mesa_dulce_premium.all().delete()

        # Guardar nuevas
        for nombre in opciones_seleccionadas:
            MesaDulcePremium.objects.create(cliente=cliente, nombre=nombre)

        return redirect('elegir_extras', cliente_id=cliente.id)

    # Acá recuperamos lo que ya tenía seleccionado
    seleccionadas = cliente.mesa_dulce_premium.values_list('nombre', flat=True)

    return render(request, 'elegir_mesa_dulce_premium.html', {
        'cliente': cliente,
        'mesa_dulce_premium_posibles': MESA_DULCE_PREMIUM_POSIBLES,
        'seleccionadas': list(seleccionadas)
    })

EXTRAS_POSIBLES = [
    "Stand de golosinas",
    "Pochoclos y copos de azúcar",
    "Arco de globos",
    "Medio arco",
    "Invitacion digital",
    "Filmación",
    "Set de baño",
    "chispas frías",  # <--- detalle extra también
    "Plataforma 360",
    "Stand glitter",
    "Stand de tatuajes",
    "Torta",
    "Shimer",
    "Book + libro de firmas",
    "Banner personalizado",
    "Video cronológico",
    "Peinado + maquillaje",
    "letras luminosas",  # <--- detalle extra
    "Cotillón flúor",
    "Espejo mágico",
    "15 rosas",
    "Fotografía",
    "Robot led",
    "Barra de jugos frutales",
    "Capa led (carioca)",
    "Lanza papelitos",
    "Ambientación mesa candy",
    "Reportaje (1 hora)",
]

@login_required
def elegir_extras(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.method == 'POST':
        extras_seleccionados = request.POST.getlist('extras')
        detalle_letras = request.POST.get('detalle_letras', '').strip()
        detalle_chispas = request.POST.get('detalle_chispas', '').strip()
        detalle_arco = request.POST.get('detalle_arco', '').strip()  # << nuevo campo

        todos_los_extras = extras_seleccionados.copy()

        # Detalle para "4 letras luminosas"
        if "4 letras luminosas" in extras_seleccionados and detalle_letras:
            todos_los_extras = [
                f"4 letras luminosas ({detalle_letras})" if e == "4 letras luminosas" else e
                for e in todos_los_extras
            ]

        # Detalle para "chispas frías"
        if "chispas frías" in extras_seleccionados and detalle_chispas:
            todos_los_extras = [
                f"chispas frías ({detalle_chispas})" if e == "chispas frías" else e
                for e in todos_los_extras
            ]

        # Detalle para "Arco de globos"
        if "Arco de globos" in extras_seleccionados and detalle_arco:
            todos_los_extras = [
                f"Arco de globos ({detalle_arco})" if e == "Arco de globos" else e
                for e in todos_los_extras
            ]

        extras_final = " | ".join(todos_los_extras) if todos_los_extras else ""

        cliente.extras.all().delete()
        if extras_final:
            Extra.objects.create(cliente=cliente, nombre=extras_final)

        return redirect('elegir_shows', cliente_id=cliente.id)

    # --- Cargar lo que ya estaba elegido ---
    extras_ya_elegidos_str = cliente.extras.values_list('nombre', flat=True).first() or ""
    extras_ya_elegidos = [x.strip() for x in extras_ya_elegidos_str.split('|')]

    detalle_letras_ya = ""
    detalle_chispas_ya = ""
    detalle_arco_ya = ""
    import re
    for ex in extras_ya_elegidos:
        if ex.startswith("4 letras luminosas"):
            match = re.search(r"\((.*)\)", ex)
            if match:
                detalle_letras_ya = match.group(1)
        elif ex.startswith("chispas frías"):
            match = re.search(r"\((.*)\)", ex)
            if match:
                detalle_chispas_ya = match.group(1)
        elif ex.startswith("Arco de globos"):
            match = re.search(r"\((.*)\)", ex)
            if match:
                detalle_arco_ya = match.group(1)

    return render(request, 'elegir_extras.html', {
        'cliente': cliente,
        'extras_posibles': EXTRAS_POSIBLES,
        'extras_ya_elegidos': extras_ya_elegidos,
        'detalle_letras_ya': detalle_letras_ya,
        'detalle_chispas_ya': detalle_chispas_ya,
        'detalle_arco_ya': detalle_arco_ya,  # pasar al template
    })


    
SHOWS_POSIBLES = [
    "Túnel 3D",
    "Saxofonista",
    "Zancos",
    "Mariachis",
    "Humorístico",
    "Transformista",
    "Malabarista",
    "Lanza llamas",
    "Personaje interno",
    "Personaje externo",
    "Reportaje",
    "Parejas de baile",
    "Plataforma",
    "Show láser",
    "Mago",
    "Imitador",
]

@login_required
def elegir_shows(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    # Shows que requieren detalle
    shows_con_detalle = [
       
        "Personaje interno",
        "Personaje externo",
    ]

    # Tuplas (show, safe_name) para el template
    shows_con_detalle_tpl = [
        (show, show.replace(" ", "_").replace("(", "").replace(")", ""))
        for show in shows_con_detalle
    ]

    if request.method == 'POST':
        shows_seleccionados = request.POST.getlist('shows')

        detalles_personajes = {}
        for show, safe_name in shows_con_detalle_tpl:
            detalle = request.POST.get(f'detalle_{safe_name}', '').strip()
            if detalle:
                detalles_personajes[show] = detalle

        cliente.shows.all().delete()
        for nombre in shows_seleccionados:
            if nombre in detalles_personajes:
                Show.objects.create(
                    cliente=cliente,
                    nombre=f"{nombre} ({detalles_personajes[nombre]})"
                )
            else:
                Show.objects.create(cliente=cliente, nombre=nombre)

        return redirect('elegir_recepcion', cliente_id=cliente.id)

    # Shows ya elegidos
    shows_ya_elegidos = cliente.shows.values_list('nombre', flat=True)

    # Extraer detalles previamente guardados
    detalles_guardados = {}
    import re
    for s in shows_ya_elegidos:
        for show, safe_name in shows_con_detalle_tpl:
            if s.startswith(show):
                match = re.search(r'\((.*)\)', s)
                if match:
                    detalles_guardados[show] = match.group(1)

    return render(request, 'elegir_shows.html', {
        'cliente': cliente,
        'shows_posibles': SHOWS_POSIBLES,
        'shows_ya_elegidos': list(shows_ya_elegidos),
        'shows_con_detalle_tpl': shows_con_detalle_tpl,
        'detalles_guardados': detalles_guardados,
    })
    
FINES_DE_FIESTA_POSIBLES = [
    "Café con medialunas de manteca",
    "Festival de pizzas",
    "Tostados de JyQ con jugo de naranja",
    "Súper panchos con papas pay",
    "Desayuno criollo: tortafritas con mate cocido",
]
@login_required
def elegir_fin_de_fiesta(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.method == 'POST':
        nombre = request.POST.get('fin_de_fiesta')

        EleccionFinDeFiesta.objects.update_or_create(
            cliente=cliente,
            defaults={'nombre': nombre}
        )

        return redirect('resumen_cliente', cliente_id=cliente.id)

    # Obtener elección previa si existe
    eleccion_previa = EleccionFinDeFiesta.objects.filter(cliente=cliente).first()
    nombre_preseleccionado = eleccion_previa.nombre if eleccion_previa else ""

    return render(request, 'elegir_fin_de_fiesta.html', {
        'cliente': cliente,
        'fines_de_fiesta': FINES_DE_FIESTA_POSIBLES,
        'fin_de_fiesta_elegido': nombre_preseleccionado,
    })


@login_required
def elegir_recepcion(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    RECEPCION_CATEGORIAS = {
        "Recepción básica": [
            "Empanadas de copetín",
            "Figazas de pollo al verdeo",
            "Mini pebetes surtidos",
            "Arrollados de pionono",
            "Pinchos de tomate y muzzarella"
        ],
        "Recepción completa": [
            "Empanadas de copetín",
            "Figazas de pollo al verdeo",
            "Mini arrollados de pionono",
            "Mini sandwich de miga",
            "Brocheta de tomate y muzzarella",
            "Mini pebetes surtidos",
            "Albóndiguitas",
            "Finger fríos y calientes",
            "Niditos de masa hojaldrada",
            "Grisines saborizados",
            "Tarteletas",
            "Bollos de espinaca",
            "Salchichitas"
        ],
        "Recepción intermedia": [
            "Empanadas de copetín",
            "Figazas de pollo al verdeo",
            "Mini pebetes surtidos",
            "Arrollados de pionono",
            "Pinchos de tomate y muzzarella",
            "Finger fríos y calientes",
            "Mil hojas de papa",
            "Albóndiguitas",
            "Bollos de acelga"
        ]
    }

    # Recuperar la categoría anterior (si existe)
    elecciones_previas = list(cliente.recepcion.values_list('item', flat=True))
    categoria_seleccionada = None
    for cat, items in RECEPCION_CATEGORIAS.items():
        if all(i in elecciones_previas for i in items):
            categoria_seleccionada = cat
            break

    if request.method == "POST":
        nueva_categoria = request.POST.get("categoria_recepcion")
        items_nuevos = RECEPCION_CATEGORIAS.get(nueva_categoria, [])

        # Borrar todos los ítems anteriores
        cliente.recepcion.all().delete()

        # Guardar solo los items seleccionados
        seleccionados = request.POST.getlist("items_seleccionados")
        for item in seleccionados:
            EleccionRecepcion.objects.create(
                cliente=cliente,
                item=item,
                cantidad=1,
                observacion=""
            )

        return redirect("elegir_fin_de_fiesta", cliente_id=cliente.id)

    return render(request, "elegir_recepcion.html", {
        "cliente": cliente,
        "categorias": RECEPCION_CATEGORIAS,
        "categoria_seleccionada": categoria_seleccionada,
    })

@login_required
def resumen_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    # Verificar perfil del usuario
    perfil = getattr(request.user, 'perfilusuario', None)
    mostrar_botones = request.user.is_superuser or (perfil and perfil.tipo != 'limitado')

    # Última elección de platos del nuevo modelo
    eleccion_platos = cliente.elecciones.last()

    # Recepción
    recepcion_items = cliente.recepcion.all() if hasattr(cliente, 'recepcion') else []

    # Cantidad de personas
    num_adultos = eleccion_platos.num_adultos if eleccion_platos else None
    num_ninos = eleccion_platos.num_ninos if eleccion_platos else None
    cantidad_personas = (num_adultos or 0) + (num_ninos or 0) if (num_adultos or num_ninos) else None

    # Barra de tragos
    barra_tragos = cliente.barra_tragos.first()
    duracion_barra = barra_tragos.duracion if barra_tragos else None

    # Teléfonos
    telefono = cliente.telefonos.first() if hasattr(cliente, 'telefonos') else None

    # Plan
    plan = cliente.plan.first() if hasattr(cliente, 'plan') else None

    # Bebidas
    bebidas = cliente.bebidas.all() if hasattr(cliente, 'bebidas') else []
    vinos = cliente.vinos.all() if hasattr(cliente, 'vinos') else []
    choperas = cliente.choperas.all() if hasattr(cliente, 'choperas') else []

    return render(request, 'resumen_cliente.html', {
        'cliente': cliente,
        'plan': plan,
        'bebidas': bebidas,
        'vinos': vinos,
        'choperas': choperas,
        'islas': cliente.islas.all() if hasattr(cliente, 'islas') else [],
        'islas_premium': cliente.islas_premium.all() if hasattr(cliente, 'islas_premium') else [],
        'postres': cliente.postres.all() if hasattr(cliente, 'postres') else [],
        'mesa_dulce': cliente.mesa_dulce_premium.all() if hasattr(cliente, 'mesa_dulce_premium') else [],
        'extras': cliente.extras.all() if hasattr(cliente, 'extras') else [],
        'shows': cliente.shows.all() if hasattr(cliente, 'shows') else [],
        'fin_de_fiesta': getattr(cliente, 'fin_de_fiesta', None),
        'elegir_platos': eleccion_platos,
        'recepcion_items': recepcion_items,
        'cantidad_personas': cantidad_personas,
        'barra_tragos': duracion_barra,
        'telefono': telefono,
        'num_adultos': num_adultos,
        'num_ninos': num_ninos,
        'mostrar_botones': mostrar_botones,  # pasamos al template
    })
    
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Cliente, PerfilUsuario


@login_required
def buscar_o_crear_cliente(request):
    # Obtener perfil del usuario
    perfil = getattr(request.user, 'perfilusuario', None)
    # Determinar si se muestran los botones (crear cliente) según tipo de usuario
    mostrar_botones = request.user.is_superuser or (perfil and perfil.tipo != 'limitado')

    mensaje = ''
    clientes_encontrados = None  # No mostrar nada antes de buscar

    # Lista de salones
    lista_salones = [
        "Varela", "Varela II", "Berazategui", "Monteverde", "París",
        "Dream's", "Melody", "Luxor", "Bernal", "Sol Fest",
        "Clahe", "Onix", "Auguri", "Dominico II", "Gala", "Sarandí II",
        "Garufa", "Lomas", "Temperley", "Clahe Escalada", "Piñeyro", "Monte Grande"
    ]

    # Obtener filtros desde GET
    dni = request.GET.get('dni', '').strip()
    salon = request.GET.get('salon', '').strip()
    fecha_evento = request.GET.get('fecha_evento', '').strip()

    if dni or salon or fecha_evento:
        clientes_encontrados = Cliente.objects.all()

        if dni:
            clientes_encontrados = clientes_encontrados.filter(dni__icontains=dni)
        if salon:
            clientes_encontrados = clientes_encontrados.filter(salon=salon)
        if fecha_evento:
            clientes_encontrados = clientes_encontrados.filter(fecha_evento=fecha_evento)

        if not clientes_encontrados.exists():
            mensaje = "No se encontraron clientes con los filtros aplicados."

    return render(request, 'inicio.html', {
        'mostrar_botones': mostrar_botones,  # se pasa al template
        'mensaje': mensaje,
        'clientes_encontrados': clientes_encontrados,
        'salones': lista_salones,
        'filtros': {'dni': dni, 'salon': salon, 'fecha_evento': fecha_evento}
    })

@login_required
def seleccionar_cliente_para_editar(request):
    if request.method == 'POST':
        dni = request.POST.get('cliente_dni')  # lo que mandás desde el input

        try:
            cliente = Cliente.objects.get(dni=dni)
            return redirect('editar_cliente', cliente_id=cliente.id)
        except Cliente.DoesNotExist:
            return render(request, 'seleccionar_cliente_para_editar.html', {
                'error': 'Cliente no encontrado.'
            })

    return render(request, 'seleccionar_cliente_para_editar.html')
    
@login_required
def editar_cliente(request, cliente_id):
    # Podés borrar o no las elecciones previas, según lo que necesites
    return redirect('agregar_telefonos', cliente_id=cliente_id)


BARRA_TRAGOS_POSIBLES = [
    "sin barra",
    "3 horas",
    "6 horas",
    "All inclisive",
]
@login_required
def elegir_barra_tragos(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.method == 'POST':
        duracion_seleccionada = request.POST.get('barra_tragos')

        # ✅ Eliminamos cualquier barra anterior del cliente
        cliente.barra_tragos.all().delete()

        # ✅ Guardamos la nueva
        if duracion_seleccionada:
            BarraTragos.objects.create(cliente=cliente, duracion=duracion_seleccionada)

        return redirect('elegir_platos', cliente_id=cliente.id)  # 👉 redirige al paso que necesites

    # 🟢 Si ya tiene algo guardado, lo traemos
    barra_actual = cliente.barra_tragos.first()
    duracion_previa = barra_actual.duracion if barra_actual else None

    return render(request, 'elegir_barra_tragos.html', {
        'cliente': cliente,
        'barra_tragos_posibles': BARRA_TRAGOS_POSIBLES,
        'duracion_previa': duracion_previa,
    })