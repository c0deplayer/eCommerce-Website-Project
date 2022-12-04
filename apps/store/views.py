from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from .models import Product, Category
from ..cart.cart import Cart


def search(request):
    query = request.GET.get('query')
    products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))

    context = {
        'query': query,
        'products': products
    }

    return render(request, 'search.html', context)


def product_detail(request, category_slug, slug):
    product = get_object_or_404(Product, slug=slug)

    images_string = f"{{'thumbnail': '{product.thumbnail.url}', 'image': '{product.image.url}'}}, "

    for image in product.images.all():
        images_string = images_string + (f"{{'thumbnail': '{image.thumbnail.url}', "
                                         f"'image': '{image.image.url}'}}, ")

    cart = Cart(request)

    if cart.has_product(product.id):
        product.in_cart = True
    else:
        product.in_cart = False

    context = {
        'product': product,
        'images_string': images_string
    }

    return render(request, 'product_detail.html', context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.product.all()

    context = {
        'category': category,
        'products': products
    }

    return render(request, 'category_detail.html', context)
