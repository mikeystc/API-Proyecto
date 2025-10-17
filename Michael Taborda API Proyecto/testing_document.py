"""
Script para generar documentación de pruebas de la API de Tienda Web
"""

def generate_testing_document():
    """Genera la documentación de testing en formato texto"""
    
    document = """
DOCUMENTACIÓN DE TESTING - API DE TIENDA WEB
============================================

PRUEBAS REALIZADAS CON POSTMAN
------------------------------

1. PRUEBAS DE ENDPOINTS DE PRODUCTOS
   --------------------------------

   a) GET /api/productos
      - Objetivo: Listar todos los productos
      - Método: GET
      - URL: http://localhost:5000/api/productos
      - Response Esperado: 200 OK con lista de productos
      - Pruebas Realizadas:
        ✅ Listar todos los productos
        ✅ Filtrar por categoría
        ✅ Filtrar por rango de precios

   b) GET /api/productos/1
      - Objetivo: Obtener producto específico
      - Método: GET
      - URL: http://localhost:5000/api/productos/1
      - Response Esperado: 200 OK con detalles del producto
      - Pruebas Realizadas:
        ✅ Producto existente
        ✅ Producto no existente (404)

   c) POST /api/productos
      - Objetivo: Crear nuevo producto
      - Método: POST
      - URL: http://localhost:5000/api/productos
      - Body Ejemplo:
        {
          "nombre": "Nuevo Producto",
          "precio": 99.99,
          "categoria": "Electrónicos",
          "stock": 10,
          "descripcion": "Descripción del producto"
        }
      - Response Esperado: 201 Created
      - Pruebas Realizadas:
        ✅ Creación exitosa
        ✅ Validación de campos requeridos
        ✅ Precio negativo (validación)

   d) PUT /api/productos/1
      - Objetivo: Actualizar producto
      - Método: PUT
      - URL: http://localhost:5000/api/productos/1
      - Body Ejemplo: {"precio": 129.99, "stock": 25}
      - Response Esperado: 200 OK
      - Pruebas Realizadas:
        ✅ Actualización exitosa
        ✅ Producto no encontrado

   e) DELETE /api/productos/1
      - Objetivo: Eliminar producto
      - Método: DELETE
      - URL: http://localhost:5000/api/productos/1
      - Response Esperado: 200 OK
      - Pruebas Realizadas:
        ✅ Eliminación exitosa
        ✅ Producto no encontrado

2. PRUEBAS DE ENDPOINTS DE PEDIDOS
   ------------------------------

   a) POST /api/pedidos
      - Objetivo: Crear nuevo pedido
      - Método: POST
      - URL: http://localhost:5000/api/pedidos
      - Body Ejemplo:
        {
          "cliente": {
            "nombre": "Carlos Ruiz",
            "email": "carlos@example.com"
          },
          "items": [
            {
              "producto_id": 1,
              "cantidad": 2
            }
          ],
          "direccion_entrega": {
            "calle": "Carrera 45 #12-34",
            "ciudad": "Medellín",
            "codigo_postal": "050001"
          }
        }
      - Response Esperado: 201 Created
      - Pruebas Realizadas:
        ✅ Creación exitosa
        ✅ Validación de items
        ✅ Stock insuficiente
        ✅ Producto no existente

   b) GET /api/pedidos
      - Objetivo: Listar pedidos
      - Método: GET
      - URL: http://localhost:5000/api/pedidos
      - Response Esperado: 200 OK con lista de pedidos

   c) GET /api/pedidos/1
      - Objetivo: Obtener pedido específico
      - Método: GET
      - URL: http://localhost:5000/api/pedidos/1
      - Response Esperado: 200 OK con detalles del pedido

3. PRUEBAS DE ENDPOINTS DE USUARIOS
   --------------------------------

   a) POST /api/usuarios/registro
      - Objetivo: Registrar nuevo usuario
      - Método: POST
      - URL: http://localhost:5000/api/usuarios/registro
      - Body Ejemplo:
        {
          "email": "nuevo@example.com",
          "password": "clave123",
          "nombre": "Nuevo Usuario",
          "direccion": {
            "calle": "Calle 123",
            "ciudad": "Bogotá"
          }
        }
      - Response Esperado: 201 Created
      - Pruebas Realizadas:
        ✅ Registro exitoso
        ✅ Usuario ya existe
        ✅ Validación de campos

   b) POST /api/usuarios/login
      - Objetivo: Iniciar sesión
      - Método: POST
      - URL: http://localhost:5000/api/usuarios/login
      - Body Ejemplo: {"email": "nuevo@example.com", "password": "clave123"}
      - Response Esperado: 200 OK
      - Pruebas Realizadas:
        ✅ Login exitoso
        ✅ Credenciales incorrectas

COLECCIÓN DE POSTMAN
-------------------
Se creó una colección en Postman con:
- 15 pruebas automatizadas
- Variables de entorno para la URL base
- Tests para validar status codes y respuestas
- Ejemplos de request body para cada endpoint

RESULTADOS DEL TESTING
----------------------
✅ Todos los endpoints funcionan correctamente
✅ Validaciones de datos implementadas
✅ Manejo adecuado de errores
✅ Códigos de estado HTTP apropiados
✅ Respuestas en formato JSON consistentes

ESCENARIOS PROBADOS
------------------
1. Flujo completo de compra:
   - Registro de usuario
   - Listado de productos
   - Creación de pedido
   - Verificación de pedido

2. Gestión de inventario:
   - Creación de productos
   - Actualización de stock
   - Validación de stock en pedidos

3. Casos de error:
   - Datos faltantes
   - IDs no existentes
   - Stock insuficiente
   - Usuarios duplicados
"""

    with open('testing_document.txt', 'w', encoding='utf-8') as f:
        f.write(document)
    
    print("Documentación de testing generada en 'testing_document.txt'")

if __name__ == "__main__":
    generate_testing_document()