# games/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from decimal import Decimal

from .models import Game, Cart, CartItem

def browse_view(request):
    """
    Renders the browse page with a list of all games.
    """
    games = Game.objects.all()
    return render(request, 'games/game_list.html', {'games': games})

def game_detail_view(request, game_id):
    """
    Renders the details page for a specific game.
    """
    game = get_object_or_404(Game, id=game_id)
    return render(request, 'games/game_detail.html', {'game': game})

@login_required
def cart_view(request):
    """
    Renders the cart page with cart items and totals.
    """
    cart = None
    cart_items = []
    subtotal = Decimal('0.00')
    gst_amount = Decimal('0.00')
    grand_total = Decimal('0.00')

    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)
            subtotal = sum(item.game.price for item in cart_items)
            gst_amount = subtotal * Decimal('0.18')
            grand_total = subtotal + gst_amount
        except Cart.DoesNotExist:
            pass

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'gst_amount': gst_amount,
        'grand_total': grand_total
    }
    return render(request, 'games/cart.html', context)

@login_required
def add_to_cart(request, game_id):
    """
    Adds a game to the user's shopping cart.
    """
    if request.method == 'POST':
        game = get_object_or_404(Game, id=game_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, game=game)
        return redirect('games:cart')
    return redirect('games:browse')

@login_required
def remove_from_cart(request, item_id):
    """
    Removes a game from the user's shopping cart.
    """
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id)
        if cart_item.cart.user == request.user:
            cart_item.delete()
        return redirect('games:cart')
    return redirect('games:cart')

@login_required
def checkout_view(request):
    """
    Renders the checkout page.
    """
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    subtotal = sum(item.game.price for item in cart_items)
    gst_amount = subtotal * Decimal('0.18')
    grand_total = subtotal + gst_amount

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'gst_amount': gst_amount,
        'grand_total': grand_total,
    }
    return render(request, 'games/checkout.html', context)

@login_required
def checkout_complete_view(request):
    """
    Handles order completion and redirects to the invoice page.
    """
    if request.method == 'POST':
        cart = get_object_or_404(Cart, user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
        
        request.session['invoice_data'] = {
            'items': [
                {'title': item.game.title, 'price': str(item.game.price)}
                for item in cart_items
            ],
            'subtotal': str(sum(item.game.price for item in cart_items)),
            'gst_amount': str(sum(item.game.price for item in cart_items) * Decimal('0.18')),
            'grand_total': str(sum(item.game.price for item in cart_items) + (sum(item.game.price for item in cart_items) * Decimal('0.18'))),
        }
        
        cart_items.delete()
        cart.delete()
        
        return redirect('games:invoice_view')
    
    return redirect('page:home')


@login_required
def invoice_view(request):
    """
    Renders the invoice page from session data.
    """
    invoice_data = request.session.get('invoice_data')
    if not invoice_data:
        # Redirect if no invoice data exists
        return redirect('page:home')
    
    # Convert string prices back to Decimal for calculations
    items = [{'title': item['title'], 'price': Decimal(item['price'])} for item in invoice_data['items']]
    subtotal = Decimal(invoice_data['subtotal'])
    gst_amount = Decimal(invoice_data['gst_amount'])
    grand_total = Decimal(invoice_data['grand_total'])

    context = {
        'invoice_data': {
            'items': items,
            'subtotal': subtotal,
            'gst_amount': gst_amount,
            'grand_total': grand_total,
        },
        'user': request.user,
    }
    
    return render(request, 'games/invoice.html', context)


@login_required
def download_invoice_view(request):
    """
    Generates and downloads a PDF invoice using the session data.
    """
    invoice_data = request.session.get('invoice_data')
    if not invoice_data:
        return redirect('page:home')
        
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    p.setFillColorRGB(0, 0, 0)
    p.setFont("Helvetica-Bold", 24)
    p.drawString(400, 750, "INVOICE")
    
    p.setFont("Helvetica", 12)
    p.drawString(100, 730, f"Billed To: {request.user.username}")
    p.drawString(100, 715, "Thank you for your purchase!")

    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, 680, "Game Title")
    p.drawString(400, 680, "Price")
    p.line(100, 675, 500, 675)

    y_position = 660
    p.setFont("Helvetica", 12)
    items = [{'title': item['title'], 'price': Decimal(item['price'])} for item in invoice_data['items']]
    for item in items:
        p.drawString(100, y_position, item['title'])
        p.drawString(400, y_position, f"₹{item['price']:.2f}")
        y_position -= 20
    p.line(100, y_position, 500, y_position)

    p.setFont("Helvetica-Bold", 12)
    y_position -= 20
    p.drawString(300, y_position, "Subtotal:")
    p.drawString(400, y_position, f"₹{Decimal(invoice_data['subtotal']):.2f}")
    y_position -= 20
    p.drawString(300, y_position, "GST (18%):")
    p.drawString(400, y_position, f"₹{Decimal(invoice_data['gst_amount']):.2f}")
    y_position -= 20
    p.drawString(300, y_position, "Grand Total:")
    p.drawString(400, y_position, f"₹{Decimal(invoice_data['grand_total']):.2f}")
    p.line(300, y_position - 5, 500, y_position - 5)

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
    return response

def discussions_view(request):
    """
    Renders the discussions page.
    """
    return render(request, 'games/discussions.html')
