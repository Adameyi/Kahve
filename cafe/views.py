
#Django imports
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django.views import generic
from django.urls import reverse
from django.template import loader
from django.db.models import Q
from django.http import JsonResponse

import time
import sys

#Local imports
from .models import Product
from .forms import ProductForm

#HTTP ERROR PAGES
def handler404(request, exception):
    # Customize the error message based on the exception
    error_message = str(exception) if exception else "Page not found"

    # Render the 404.html template with the error message
    return render(request, '404.html', {'error_message': error_message}, status=404)

def index(request):
    is_index_page = (request.path == '/cafe/') 
    
    # List for all Product Items
    products = Product.objects.all()
    coffees = Product.objects.filter(category=Product.COFFEE)
    teas = Product.objects.filter(category=Product.TEA)
    milkshakes = Product.objects.filter(category=Product.MILKSHAKE)
    smoothies = Product.objects.filter(category=Product.SMOOTHIE)
    drink_choices = Product.DRINK_CHOICES
    product_count = products.count()

    #Retrieve products in cart
    products_in_cart = get_products_in_cart(request)

    # Create a dictionary to map categories to their respective product lists
    category_products = {}
    for category_display, _ in Product.DRINK_CHOICES:
        category_products[category_display] = products.filter(category=category_display)

    context = {
        'is_index_page': is_index_page,
        
        'products_list': products,
        'coffees': coffees,
        'teas': teas,
        'milkshakes': milkshakes,
        'smoothies': smoothies,
        'product_count': product_count,
        'drink_choices': drink_choices,
        'category_products': category_products,
        'products_in_cart': products_in_cart,
    }

    return render(request, 'cafe/index.html', context)

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ProductForm()
    return render(request, 'cafe/add_product.html', {'form': form})    

def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    return redirect('index')
        
def favourite_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.favourited = not product.favourited
    product.save()
    return redirect('index')

def search_products(request):
    # Get the query via GET parameters, otherwise, default to an empty string.
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort')

    # Obtain products queryset based on search query
    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        print("Filtered products:", products)  # Debug print
    else:
        # Default to index page (Showcase All Products)
        products = Product.objects.all() 
    
    if sort_by == 'asc':
         products = products.order_by('name')
    elif sort_by == 'desc':
        products = products.order_by('-name')
    elif sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    context = {
        'products': products,
        'query': query,
        'sort_by': sort_by,
    }

    if not query and not sort_by:
        return redirect(reverse('index'))

    return render(request, 'cafe/index.html', context)

def add_category(request):
    if request.method == 'POST':
        new_category = request.POST.get('new_category')
        if new_category:
            # Append the new category to DRINK_CHOICES
            Product.DRINK_CHOICES.append((new_category, new_category.upper()))
            # Redirect to index.html after adding the category
            return redirect('index')
        else:
            print('Error')
            # return render(request, 'error_template.html', {'error_message': 'Category is required'})
    else:
        # Handle GET request (display form)
        return render(request, 'add_category.html')
    
def buy_product(request, product_id):
    #Check if the object exists.
    product = get_object_or_404(Product, pk=product_id)
    
    #Get cart from session data.        
    cart = request.session.get('cart',{})
    
    #Add the product to the cart, If it already exists, increment ints quantity.
    cart[product_id] = cart.get(product_id, 0) + 1
    
    #Update session data with modified cart
    request.session['cart'] = cart
    
    print("Product Purchased")
    print(request.session)
    sys.stdout.flush()
    
    time.sleep(0.25) #Delay to allow cart modal popup
    return redirect('index')

def get_products_in_cart(request):
    cart = request.session.get('cart', {})
    
    #Retrieve products in cart
    products_in_cart = [] 
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        products_in_cart.append({
            'product': product,
            'quantity': quantity
        })
        
    # Print cart items (for debugging purposes)
    print("Cart:")
    for item in products_in_cart:
        print(f"Product: {item['product'].name}, Quantity: {item['quantity']}")    
    
    return products_in_cart
    
class IndexView(generic.ListView):
    model = Product
    template_name = 'cafe/index.html'
    context_object_name = 'products_list'
    
    def get_queryset(self):
        return Product.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_favourite_products'] = self.get_queryset().count()
        return context   
    

class FavouritesListView(generic.ListView):
    model = Product
    template_name = 'cafe/favourites.html'
    context_object_name = 'products_list'

    def get_queryset(self):
        return Product.objects.filter(favourited=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_favourite_products'] = self.get_queryset().count()
        return context 