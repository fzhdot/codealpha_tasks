from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem
from django.contrib import messages

# 1. Liste des produits
from django.db.models import Q

def product_list(request):
    category = request.GET.get('category')
    search_query = request.GET.get('search')
    
    products = Product.objects.all()
    
    # Filtrage par catégorie
    if category and category != 'all':
        products = products.filter(category=category)
    
    # Recherche par nom ou description (optionnel)
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Récupérer toutes les catégories disponibles pour les filtres
    categories = Product.objects.values_list('category', flat=True).distinct()
    
    context = {
        'products': products,
        'categories': categories,
        'current_category': category,
        'search_query': search_query,
    }
    
    return render(request, 'ecommerce/product_list.html', context)
# 2. Détails d'un produit
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'ecommerce/product_detail.html', {'product': product})

from django.shortcuts import get_object_or_404

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Initialiser le panier si inexistant
    if 'cart' not in request.session:
        request.session['cart'] = {}
    
    cart = request.session['cart']
    
    # Convertir les clés en string pour éviter les problèmes de type
    str_product_id = str(product_id)
    
    # Vérifier le stock avant d'ajouter
    if product.stock > cart.get(str_product_id, 0):
        cart[str_product_id] = cart.get(str_product_id, 0) + 1
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, f"{product.name} ajouté au panier")
    else:
        messages.error(request, f"Stock insuffisant pour {product.name}")
    
    return redirect('cart_view')

def cart_view(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    cart_count = 0

    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
            subtotal = product.price * quantity
            items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
            total += subtotal
            cart_count += quantity
        except (Product.DoesNotExist, ValueError):
            del cart[product_id]
            request.session.modified = True

    request.session['cart_count'] = cart_count

    return render(request, 'ecommerce/cart.html', {
        'items': items,
        'total': total,
        'cart_count': cart_count
    })


# 5. Passer la commande
@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    
    # Debug
    print("DEBUG - Contenu panier:", cart)
    
    if not cart:
        messages.info(request, 'Votre panier est vide.')
        return redirect('cart_view')
    
    # Nettoyer le panier AVANT de créer la commande
    valid_items = []
    for product_id, quantity in cart.items():
        try:
            product_id_int = int(product_id)
            if Product.objects.filter(id=product_id_int).exists():
                product = Product.objects.get(id=product_id_int)
                valid_items.append((product, int(quantity)))
            else:
                print(f"PRODUIT INTROUVABLE: ID {product_id_int}")
                
        except Exception as e:
            print(f"ERREUR: {e}")
    
    if not valid_items:
        messages.error(request, 'Aucun produit valide dans le panier.')
        request.session['cart'] = {}  # Vider le panier
        return redirect('product_list')
    
    # Créer la commande avec les produits valides uniquement
    order = Order.objects.create(user=request.user)
    
    for product, quantity in valid_items:
        OrderItem.objects.create(order=order, product=product, quantity=quantity)
    
    request.session['cart'] = {}
    
    return render(request, 'ecommerce/confirmation.html', {'order': order})
# 6. Voir les commandes de l'utilisateur
@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'ecommerce/order_list.html', {'orders': orders})
