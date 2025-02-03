from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models import Producto, db, Detalle

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))
    productos = Producto.query.all()
    return render_template('admin_dashboard.html', productos=productos)

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