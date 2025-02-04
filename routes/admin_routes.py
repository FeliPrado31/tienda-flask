from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models import Producto, db, Detalle, Cliente, Pedido

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))

    productos = Producto.query.all()
    clientes = Cliente.query.all()

    return render_template('admin_dashboard.html', productos=productos, clientes=clientes)


@admin_bp.route('/cliente/facturas/<int:cliente_id>')
@login_required
def ver_facturas_cliente(cliente_id):
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))

    cliente = Cliente.query.get_or_404(cliente_id)

    pedidos = Pedido.query.filter_by(cliente_id=cliente.id).all()

    pedidos_con_detalles = []
    for pedido in pedidos:
        detalles = Detalle.query.filter_by(pedido_id=pedido.id).all()
        productos = [
            {
                'nombre': detalle.producto.nombre,
                'precio': detalle.producto.precio,
                'cantidad': detalle.cantidad
            }
            for detalle in detalles
        ]
        total = sum(producto['precio'] * producto['cantidad'] for producto in productos)
        pedidos_con_detalles.append({
            'id': pedido.id,
            'fecha_creacion': pedido.fecha_creacion,
            'estado': pedido.estado,
            'productos': productos,
            'total': total
        })
    return render_template('ver_facturas_cliente.html', cliente=cliente, pedidos=pedidos_con_detalles)

@admin_bp.route('/producto/crear', methods=['GET', 'POST'])
@login_required
def crear_producto():
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = float(request.form['precio'])
        nuevo_producto = Producto(nombre=nombre, precio=precio)
        db.session.add(nuevo_producto)
        db.session.commit()
        flash('Producto creado exitosamente.')
        return redirect(url_for('admin.dashboard'))
    return render_template('crear_producto.html')

@admin_bp.route('/producto/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_producto(id):
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))
    producto = Producto.query.get_or_404(id)
    if request.method == 'POST':
        producto.nombre = request.form['nombre']
        producto.precio = float(request.form['precio'])
        db.session.commit()
        flash('Producto actualizado exitosamente.')
        return redirect(url_for('admin.dashboard'))
    return render_template('editar_producto.html', producto=producto)

@admin_bp.route('/producto/eliminar/<int:id>')
@login_required
def eliminar_producto(id):
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))

    producto = Producto.query.get_or_404(id)

    detalles_asociados = Detalle.query.filter_by(producto_id=producto.id).all()

    for detalle in detalles_asociados:
        if detalle.pedido.estado == 'pendiente':
            flash('No se puede eliminar el producto porque está asociado a un pedido pendiente.')
            return redirect(url_for('admin.dashboard'))

    db.session.delete(producto)
    db.session.commit()
    flash('Producto eliminado exitosamente.')
    return redirect(url_for('admin.dashboard'))