from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product
from .forms import ProductForm, UpdateQuantityForm


def product_list(request):
    products = Product.objects.all().order_by("-updated_at")
    total_products = products.count()
    low_stock = products.filter(quantity__lte=5).count()

    return render(request, "products/product_list.html", {
        "products": products,
        "total_products": total_products,
        "low_stock": low_stock,
    })


def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully!")
            return redirect("products:product_list")
    else:
        form = ProductForm()
    return render(request, "products/add_product.html", {"form": form})


def update_quantity(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = UpdateQuantityForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"Updated quantity for {product.name}")
            return redirect("products:product_list")
    else:
        form = UpdateQuantityForm(instance=product)
    return render(request, "products/update_quantity.html", {"form": form, "product": product})


def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, "Product deleted successfully!")
    return redirect("products:product_list")
