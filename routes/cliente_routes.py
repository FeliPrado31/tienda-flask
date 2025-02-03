from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user

from models import Cliente, db, Pedido, Producto, Detalle

cliente_bp = Blueprint('cliente', __name__)


@cliente_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'cliente':
        flash('Acceso no autorizado. Debes ser un cliente para acceder a esta página.')
        return redirect(url_for('auth.login'))

    cliente = Cliente.query.filter_by(user_id=current_user.id).first()
    if not cliente:
        flash('No se encontró un perfil de cliente asociado a este usuario.')
        return redirect(url_for('auth.login'))

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
        pedidos_con_detalles.append({
            'id': pedido.id,
            'fecha_creacion': pedido.fecha_creacion,
            'estado': pedido.estado,
            'productos': productos
        })
    return render_template('cliente_dashboard.html', pedidos=pedidos_con_detalles)


@cliente_bp.route('/pedido/crear', methods=['GET', 'POST'])
@login_required
def crear_pedido():
    if current_user.role != 'cliente':
        return redirect(url_for('auth.login'))

    productos = Producto.query.all()
    if request.method == 'POST':

        cliente = Cliente.query.filter_by(user_id=current_user.id).first()
        if not cliente:
            flash('No se encontró un perfil de cliente asociado a este usuario.')
            return redirect(url_for('auth.login'))


        nuevo_pedido = Pedido(cliente=cliente)
        db.session.add(nuevo_pedido)
        db.session.commit()


        productos_seleccionados = request.form.getlist('productos')
        for producto_id in productos_seleccionados:
            producto = Producto.query.get(int(producto_id))
            if producto:
                detalle = Detalle(pedido=nuevo_pedido, producto=producto, cantidad=1)
                db.session.add(detalle)

        db.session.commit()
        flash('Pedido creado exitosamente.')
        return redirect(url_for('cliente.dashboard'))

    return render_template('crear_pedido.html', productos=productos)