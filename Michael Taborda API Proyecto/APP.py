from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas

# Archivo de base de datos simple (JSON)
PRODUCTS_DB = 'data/products.json'
ORDERS_DB = 'data/orders.json'
USERS_DB = 'data/users.json'

# Crear directorio data si no existe
os.makedirs('data', exist_ok=True)

def init_database():
    """Inicializa la base de datos con datos de ejemplo"""
    # Productos de ejemplo
    sample_products = [
        {
            "id": 1,
            "nombre": "Laptop Gamer",
            "descripcion": "Laptop para gaming de alta gama",
            "precio": 1200.00,
            "categoria": "Tecnología",
            "stock": 15,
            "imagen": "laptop.jpg",
            "rating": 4.5
        },
        {
            "id": 2,
            "nombre": "Smartphone Android",
            "descripcion": "Teléfono inteligente con Android",
            "precio": 350.00,
            "categoria": "Tecnología",
            "stock": 30,
            "imagen": "smartphone.jpg",
            "rating": 4.2
        },
        {
            "id": 3,
            "nombre": "Auriculares Bluetooth",
            "descripcion": "Auriculares inalámbricos con cancelación de ruido",
            "precio": 89.99,
            "categoria": "Audio",
            "stock": 50,
            "imagen": "auriculares.jpg",
            "rating": 4.7
        },
        {
            "id": 4,
            "nombre": "Camiseta Básica",
            "descripcion": "Camiseta de algodón 100%",
            "precio": 15.99,
            "categoria": "Ropa",
            "stock": 100,
            "imagen": "camiseta.jpg",
            "rating": 4.0
        },
        {
            "id": 5,
            "nombre": "Zapatos Deportivos",
            "descripcion": "Zapatos para running y ejercicio",
            "precio": 65.50,
            "categoria": "Calzado",
            "stock": 25,
            "imagen": "zapatos.jpg",
            "rating": 4.3
        }
    ]
    
    # Guardar productos
    with open(PRODUCTS_DB, 'w', encoding='utf-8') as f:
        json.dump(sample_products, f, indent=2)
    
    # Inicializar órdenes vacías
    with open(ORDERS_DB, 'w', encoding='utf-8') as f:
        json.dump([], f, indent=2)
    
    # Inicializar usuarios vacíos
    with open(USERS_DB, 'w', encoding='utf-8') as f:
        json.dump([], f, indent=2)

def read_json(file_path):
    """Lee un archivo JSON y retorna los datos"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def write_json(file_path, data):
    """Escribe datos en un archivo JSON"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

@app.route('/')
def home():
    """Endpoint de bienvenida de la API"""
    return jsonify({
        "message": "🛒 Bienvenido a la API de Tienda Web",
        "version": "1.0.0",
        "endpoints": {
            "productos": {
                "listar": "GET /api/productos",
                "obtener": "GET /api/productos/<int:id>",
                "crear": "POST /api/productos",
                "actualizar": "PUT /api/productos/<int:id>",
                "eliminar": "DELETE /api/productos/<int:id>"
            },
            "pedidos": {
                "listar": "GET /api/pedidos",
                "crear": "POST /api/pedidos",
                "obtener": "GET /api/pedidos/<int:id>"
            },
            "usuarios": {
                "registro": "POST /api/usuarios/registro",
                "login": "POST /api/usuarios/login"
            }
        }
    })

# ==================== ENDPOINTS DE PRODUCTOS ====================

@app.route('/api/productos', methods=['GET'])
def get_productos():
    """
    Obtener todos los productos
    Query parameters opcionales: categoria, min_precio, max_precio
    """
    try:
        productos = read_json(PRODUCTS_DB)
        
        # Filtros opcionales
        categoria = request.args.get('categoria')
        min_precio = request.args.get('min_precio', type=float)
        max_precio = request.args.get('max_precio', type=float)
        
        productos_filtrados = productos
        
        if categoria:
            productos_filtrados = [p for p in productos_filtrados 
                                 if p['categoria'].lower() == categoria.lower()]
        
        if min_precio is not None:
            productos_filtrados = [p for p in productos_filtrados 
                                 if p['precio'] >= min_precio]
        
        if max_precio is not None:
            productos_filtrados = [p for p in productos_filtrados 
                                 if p['precio'] <= max_precio]
        
        return jsonify({
            "success": True,
            "count": len(productos_filtrados),
            "productos": productos_filtrados
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error al obtener productos: {str(e)}"
        }), 500

@app.route('/api/productos/<int:producto_id>', methods=['GET'])
def get_producto(producto_id):
    """Obtener un producto específico por ID"""
    try:
        productos = read_json(PRODUCTS_DB)
        producto = next((p for p in productos if p['id'] == producto_id), None)
        
        if producto:
            return jsonify({
                "success": True,
                "producto": producto
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": "Producto no encontrado"
            }), 404
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error al obtener producto: {str(e)}"
        }), 500

@app.route('/api/productos', methods=['POST'])
def crear_producto():
    """Crear un nuevo producto"""
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        required_fields = ['nombre', 'precio', 'categoria', 'stock']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "success": False,
                    "error": f"Campo requerido faltante: {field}"
                }), 400
        
        productos = read_json(PRODUCTS_DB)
        
        # Generar nuevo ID
        nuevo_id = max([p['id'] for p in productos], default=0) + 1
        
        nuevo_producto = {
            "id": nuevo_id,
            "nombre": data['nombre'],
            "descripcion": data.get('descripcion', ''),
            "precio": float(data['precio']),
            "categoria": data['categoria'],
            "stock": int(data['stock']),
            "imagen": data.get('imagen', 'default.jpg'),
            "rating": data.get('rating', 0.0)
        }
        
        productos.append(nuevo_producto)
        write_json(PRODUCTS_DB, productos)
        
        return jsonify({
            "success": True,
            "message": "Producto creado exitosamente",
            "producto": nuevo_producto
        }), 201
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error al crear producto: {str(e)}"
        }), 500

@app.route('/api/productos/<int:producto_id>', methods=['PUT'])
def actualizar_producto(producto_id):
    """Actualizar un producto existente"""
    try:
        data = request.get_json()
        productos = read_json(PRODUCTS_DB)
        
        producto_index = next((i for i, p in enumerate(productos) 
                             if p['id'] == producto_id), None)
        
        if producto_index is None:
            return jsonify({
                "success": False,
                "error": "Producto no encontrado"
            }), 404
        
        # Actualizar campos permitidos
        campos_permitidos = ['nombre', 'descripcion', 'precio', 'categoria', 'stock', 'imagen', 'rating']
        for campo in campos_permitidos:
            if campo in data:
                productos[producto_index][campo] = data[campo]
        
        write_json(PRODUCTS_DB, productos)
        
        return jsonify({
            "success": True,
            "message": "Producto actualizado exitosamente",
            "producto": productos[producto_index]
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error al actualizar producto: {str(e)}"
        }), 500

@app.route('/api/productos/<int:producto_id>', methods=['DELETE'])
def eliminar_producto(producto_id):
    """Eliminar un producto"""
    try:
        productos = read_json(PRODUCTS_DB)
        productos_filtrados = [p for p in productos if p['id'] != producto_id]
        
        if len(productos_filtrados) == len(productos):
            return jsonify({
                "success": False,
                "error": "Producto no encontrado"
            }), 404
        
        write_json(PRODUCTS_DB, productos_filtrados)
        
        return jsonify({
            "success": True,
            "message": "Producto eliminado exitosamente"
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error al eliminar producto: {str(e)}"
        }), 500

# ==================== ENDPOINTS DE PEDIDOS ====================

@app.route('/api/pedidos', methods=['GET'])
def get_pedidos():
    """Obtener todos los pedidos"""
    try:
        pedidos = read_json(ORDERS_DB)
        return jsonify({
            "success": True,
            "count": len(pedidos),
            "pedidos": pedidos
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error al obtener pedidos: {str(e)}"
        }), 500

@app.route('/api/pedidos/<int:pedido_id>', methods=['GET'])
def get_pedido(pedido_id):
    """Obtener un pedido específico por ID"""
    try:
        pedidos = read_json(ORDERS_DB)
        pedido = next((p for p in pedidos if p['id'] == pedido_id), None)
        
        if pedido:
            return jsonify({
                "success": True,
                "pedido": pedido
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": "Pedido no encontrado"
            }), 404
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error al obtener pedido: {str(e)}"
        }), 500

@app.route('/api/pedidos', methods=['POST'])
def crear_pedido():
    """Crear un nuevo pedido"""
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        if 'items' not in data or not data['items']:
            return jsonify({
                "success": False,
                "error": "El pedido debe contener al menos un item"
            }), 400
        
        pedidos = read_json(ORDERS_DB)
        productos = read_json(PRODUCTS_DB)
        
        # Generar nuevo ID
        nuevo_id = max([p['id'] for p in pedidos], default=0) + 1
        
        # Validar stock y calcular total
        total = 0
        items_validados = []
        
        for item in data['items']:
            producto = next((p for p in productos if p['id'] == item['producto_id']), None)
            if not producto:
                return jsonify({
                    "success": False,
                    "error": f"Producto con ID {item['producto_id']} no encontrado"
                }), 404
            
            if producto['stock'] < item['cantidad']:
                return jsonify({
                    "success": False,
                    "error": f"Stock insuficiente para {producto['nombre']}"
                }), 400
            
            subtotal = producto['precio'] * item['cantidad']
            total += subtotal
            
            items_validados.append({
                "producto_id": item['producto_id'],
                "nombre": producto['nombre'],
                "precio_unitario": producto['precio'],
                "cantidad": item['cantidad'],
                "subtotal": subtotal
            })
        
        nuevo_pedido = {
            "id": nuevo_id,
            "cliente": data.get('cliente', {}),
            "items": items_validados,
            "total": total,
            "estado": "pendiente",
            "fecha_creacion": datetime.now().isoformat(),
            "direccion_entrega": data.get('direccion_entrega', {})
        }
        
        pedidos.append(nuevo_pedido)
        write_json(ORDERS_DB, pedidos)
        
        return jsonify({
            "success": True,
            "message": "Pedido creado exitosamente",
            "pedido": nuevo_pedido
        }), 201
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error al crear pedido: {str(e)}"
        }), 500

# ==================== ENDPOINTS DE USUARIOS ====================

@app.route('/api/usuarios/registro', methods=['POST'])
def registrar_usuario():
    """Registrar un nuevo usuario"""
    try:
        data = request.get_json()
        
        required_fields = ['email', 'password', 'nombre']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "success": False,
                    "error": f"Campo requerido faltante: {field}"
                }), 400
        
        usuarios = read_json(USERS_DB)
        
        # Verificar si el usuario ya existe
        if any(u['email'] == data['email'] for u in usuarios):
            return jsonify({
                "success": False,
                "error": "El usuario ya existe"
            }), 409
        
        nuevo_usuario = {
            "id": len(usuarios) + 1,
            "email": data['email'],
            "password": data['password'],  # En producción, esto debería estar hasheado
            "nombre": data['nombre'],
            "direccion": data.get('direccion', {}),
            "fecha_registro": datetime.now().isoformat()
        }
        
        usuarios.append(nuevo_usuario)
        write_json(USERS_DB, usuarios)
        
        return jsonify({
            "success": True,
            "message": "Usuario registrado exitosamente",
            "usuario": {
                "id": nuevo_usuario['id'],
                "email": nuevo_usuario['email'],
                "nombre": nuevo_usuario['nombre']
            }
        }), 201
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error al registrar usuario: {str(e)}"
        }), 500

@app.route('/api/usuarios/login', methods=['POST'])
def login_usuario():
    """Iniciar sesión de usuario"""
    try:
        data = request.get_json()
        
        if 'email' not in data or 'password' not in data:
            return jsonify({
                "success": False,
                "error": "Email y password son requeridos"
            }), 400
        
        usuarios = read_json(USERS_DB)
        usuario = next((u for u in usuarios 
                       if u['email'] == data['email'] and u['password'] == data['password']), None)
        
        if usuario:
            return jsonify({
                "success": True,
                "message": "Login exitoso",
                "usuario": {
                    "id": usuario['id'],
                    "email": usuario['email'],
                    "nombre": usuario['nombre']
                }
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": "Credenciales inválidas"
            }), 401
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error en el login: {str(e)}"
        }), 500

if __name__ == '__main__':
    # Inicializar base de datos con datos de ejemplo
    init_database()
    print("🛒 Base de datos de tienda inicializada correctamente")
    print("📦 Productos de ejemplo cargados")
    print("🚀 Servidor iniciando en http://localhost:5000")
    print("\nEndpoints disponibles:")
    print("GET  /api/productos     - Listar productos")
    print("GET  /api/productos/:id - Obtener producto específico")
    print("POST /api/productos     - Crear nuevo producto")
    print("PUT  /api/productos/:id - Actualizar producto")
    print("DELETE /api/productos/:id - Eliminar producto")
    print("POST /api/pedidos       - Crear nuevo pedido")
    print("POST /api/usuarios/registro - Registrar usuario")
    print("POST /api/usuarios/login - Login de usuario")
    
    app.run(debug=True, host='0.0.0.0', port=5000)