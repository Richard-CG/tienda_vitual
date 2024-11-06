import streamlit as st
import pandas as pd
from google.cloud import firestore
from google.oauth2 import service_account
import json
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)
print(key_dict)
db = firestore.Client(credentials=creds, project="tienda-virtual")
product_ref = db.collection("productos")

# Campos de producto
FIELDS = ["codigo", "nombre", "precio", "existencias", "stock_minimo", "stock_maximo"]

# Función para crear un producto
def create_product(data):
    product_ref.document(data["codigo"]).set(data)

# Función para obtener todos los productos
def get_all_products():
    return [doc.to_dict() for doc in product_ref.stream()]

# Función para buscar un producto por código
def get_product_by_code(code):
    doc = product_ref.document(code).get()
    return doc.to_dict() if doc.exists else None

# Función para actualizar un producto
def update_product(code, data):
    product_ref.document(code).update(data)

# Función para eliminar un producto
def delete_product(code):
    product_ref.document(code).delete()

# Interfaz de Streamlit
st.sidebar.title("Gestión de Productos")

# Selección de operación
option = st.sidebar.selectbox("Seleccione una operación", ["Crear", "Leer todos", "Buscar", "Actualizar", "Eliminar"])

if option == "Crear":
    st.title("Crear Producto")
    data = {field: st.text_input(field.capitalize()) for field in FIELDS}
    if st.button("Crear Producto"):
        try:
            create_product(data)
            st.success("Producto creado exitosamente")
        except Exception as e:
            st.error(f"Error al crear producto: {e}")

elif option == "Leer todos":
    st.title("Todos los Productos")
    products = get_all_products()
    if products:
        st.write(products)
    else:
        st.write("No hay productos registrados.")

elif option == "Buscar":
    st.title("Buscar Producto")
    code = st.text_input("Código del Producto")
    if st.button("Buscar"):
        product = get_product_by_code(code)
        if product:
            st.write(product)
        else:
            st.warning("Producto no encontrado")

elif option == "Actualizar":
    st.title("Actualizar Producto")
    code = st.text_input("Código del Producto a Actualizar")
    product = get_product_by_code(code) if code else None
    if product:
        data = {field: st.text_input(field.capitalize(), product[field]) for field in FIELDS}
        if st.button("Actualizar Producto"):
            try:
                update_product(code, data)
                st.success("Producto actualizado exitosamente")
            except Exception as e:
                st.error(f"Error al actualizar producto: {e}")
    else:
        st.warning("Producto no encontrado")

elif option == "Eliminar":
    st.title("Eliminar Producto")
    code = st.text_input("Código del Producto a Eliminar")
    if st.button("Eliminar Producto"):
        try:
            delete_product(code)
            st.success("Producto eliminado exitosamente")
        except Exception as e:
            st.error(f"Error al eliminar producto: {e}")
