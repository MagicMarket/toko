from django.shortcuts import render, redirect
from globalApp.models import TbMenu
from .models import Product
from django.core.paginator import Paginator
from django.db.models import Q
import os
from django.conf import settings
import base64
from django.http import JsonResponse

# Create your views here.

def product_landing(request):
    side_menu = TbMenu.objects.filter(is_active=True).order_by('order')  # type: ignore
    query = request.GET.get('q', '')
    order_by = request.GET.get('order_by', 'product')
    order_dir = request.GET.get('order_dir', 'asc')
    products = Product.objects.filter(deleted__isnull=True) # type: ignore
    if query:
        products = products.filter(Q(product__icontains=query) | Q(product_code__icontains=query))
    # Support sorting by numbering (No) column
    if order_by == 'num':
        if order_dir == 'desc':
            products = products.order_by('-id')
        else:
            products = products.order_by('id')
    elif order_by in ['product', 'stock', 'price', 'last_update_price', 'product_code']:
        if order_dir == 'desc':
            products = products.order_by(f'-{order_by}')
        else:
            products = products.order_by(order_by)
    # Compute next_dir for each column
    columns = ['num', 'product', 'stock', 'price', 'last_update_price', 'product_code']
    next_dir = {}
    for col in columns:
        if order_by == col and order_dir == 'asc':
            next_dir[col] = 'desc'
        else:
            next_dir[col] = 'asc'

    error_message = None
    edit_error_message = None
    edit_image_url = None
    edit_image_base64 = None

    # Provide base64 image for preview in edit modal if a product is being edited
    if request.method == 'GET' and request.GET.get('edit_id'):
        try:
            product_obj = Product.objects.get(pk=request.GET['edit_id']) # type: ignore
            if product_obj.image:
                image_path = os.path.join(settings.BASE_DIR, 'globalApp', 'static', product_obj.image)
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as img_file:
                        encoded = base64.b64encode(img_file.read()).decode('utf-8')
                        ext = os.path.splitext(image_path)[1].lower()
                        mime = 'image/jpeg'
                        if ext == '.png':
                            mime = 'image/png'
                        elif ext == '.gif':
                            mime = 'image/gif'
                        edit_image_base64 = f"data:{mime};base64,{encoded}"
        except Product.DoesNotExist: # type: ignore
            pass

    # Handle POST for adding or editing a product
    if request.method == 'POST':
        # Edit logic
        edit_id = request.POST.get('edit_id')
        if edit_id:
            try:
                product_obj = Product.objects.get(pk=edit_id) # type: ignore
                # Check if this is a delete action
                if request.POST.get('delete_product'):
                    product_obj.deleted = True
                    product_obj.save()
                    return redirect(request.path)
                # Edit logic
                new_product = request.POST.get('edit_product')
                new_product_code = request.POST.get('edit_product_code')
                if (product_obj.product != new_product or product_obj.product_code != new_product_code):
                    if Product.objects.filter(product=new_product, product_code=new_product_code).exclude(pk=edit_id).exists(): # type: ignore
                        edit_error_message = 'A product with the same name and code already exists.'
                        edit_image_url = product_obj.image if product_obj.image else ''
                        # Provide base64 image for preview
                        if product_obj.image:
                            image_path = os.path.join(settings.BASE_DIR, 'globalApp', 'static', product_obj.image)
                            if os.path.exists(image_path):
                                with open(image_path, 'rb') as img_file:
                                    encoded = base64.b64encode(img_file.read()).decode('utf-8')
                                    ext = os.path.splitext(image_path)[1].lower()
                                    mime = 'image/jpeg'
                                    if ext == '.png':
                                        mime = 'image/png'
                                    elif ext == '.gif':
                                        mime = 'image/gif'
                                    edit_image_base64 = f"data:{mime};base64,{encoded}"
                    else:
                        product_obj.product = new_product
                        product_obj.stock = request.POST.get('edit_stock')
                        product_obj.price = request.POST.get('edit_price')
                        product_obj.product_code = new_product_code
                        # Handle image update
                        edit_image_file = request.FILES.get('edit_image')
                        if edit_image_file:
                            # Remove old image if it exists
                            if product_obj.image:
                                old_image_path = os.path.join(settings.BASE_DIR, 'globalApp', 'static', product_obj.image)
                                if os.path.exists(old_image_path):
                                    os.remove(old_image_path)
                            # Get file extension
                            file_extension = os.path.splitext(edit_image_file.name)[1]
                            # Create new filename: ID+product_code.ext
                            new_filename = f"{product_obj.id}{product_obj.product_code}{file_extension}"
                            save_dir = os.path.join(settings.BASE_DIR, 'globalApp', 'static', 'product_photo')
                            os.makedirs(save_dir, exist_ok=True)
                            file_path = os.path.join(save_dir, new_filename)
                            with open(file_path, 'wb+') as destination:
                                for chunk in edit_image_file.chunks():
                                    destination.write(chunk)
                            product_obj.image = f'product_photo/{new_filename}'
                        product_obj.save()
                        return redirect(request.path)
                else:
                    product_obj.product = new_product
                    product_obj.stock = request.POST.get('edit_stock')
                    product_obj.price = request.POST.get('edit_price')
                    product_obj.product_code = new_product_code
                    # Handle image update
                    edit_image_file = request.FILES.get('edit_image')
                    if edit_image_file:
                        # Remove old image if it exists
                        if product_obj.image:
                            old_image_path = os.path.join(settings.BASE_DIR, 'globalApp', 'static', product_obj.image)
                            if os.path.exists(old_image_path):
                                os.remove(old_image_path)
                        # Get file extension
                        file_extension = os.path.splitext(edit_image_file.name)[1]
                        # Create new filename: ID+product_code.ext
                        new_filename = f"{product_obj.id}{product_obj.product_code}{file_extension}"
                        save_dir = os.path.join(settings.BASE_DIR, 'globalApp', 'static', 'product_photo')
                        os.makedirs(save_dir, exist_ok=True)
                        file_path = os.path.join(save_dir, new_filename)
                        with open(file_path, 'wb+') as destination:
                            for chunk in edit_image_file.chunks():
                                destination.write(chunk)
                        product_obj.image = f'product_photo/{new_filename}'
                    product_obj.save()
                    return redirect(request.path)
            except Product.DoesNotExist: # type: ignore
                pass
        # Add logic
        product = request.POST.get('product')
        stock = request.POST.get('stock')
        price = request.POST.get('price')
        product_code = request.POST.get('product_code')
        if product and stock and price and product_code:
            # Prevent duplicate product name and code
            if Product.objects.filter(product=product, product_code=product_code).exists(): # type: ignore
                error_message = 'A product with the same name and code already exists.'
            else:
                image_file = request.FILES.get('image')
                product_obj = Product.objects.create( # type: ignore
                    product=product,
                    stock=stock,
                    price=price,
                    product_code=product_code,
                    image=None,
                    deleted=None
                )
                if image_file:
                    # Save the file to static/product_photo/
                    save_dir = os.path.join(settings.BASE_DIR, 'globalApp', 'static', 'product_photo')
                    os.makedirs(save_dir, exist_ok=True)
                    # Get file extension
                    file_extension = os.path.splitext(image_file.name)[1]
                    # Create new filename: ID+product_code.ext
                    new_filename = f"{product_obj.id}{product_code}{file_extension}"
                    file_path = os.path.join(save_dir, new_filename)
                    with open(file_path, 'wb+') as destination:
                        for chunk in image_file.chunks():
                            destination.write(chunk)
                    image_path = f'product_photo/{new_filename}'
                    product_obj.image = image_path
                    product_obj.save()
                return redirect(request.path)

    paginator = Paginator(products, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'storageModule/product_landing.html', {
        'side_menu': side_menu,
        'products': page_obj.object_list,
        'page_obj': page_obj,
        'query': query,
        'order_by': order_by,
        'order_dir': order_dir,
        'next_dir': next_dir,
        'error_message': error_message,
        'edit_error_message': edit_error_message,
        'edit_image_url': edit_image_url,
        'edit_image_base64': edit_image_base64,
    })

def product_image_base64(request, product_id):
    import base64, os
    from django.conf import settings
    try:
        product = Product.objects.get(pk=product_id) # type: ignore
        if product.image:
            image_path = os.path.join(settings.BASE_DIR, 'globalApp', 'static', product.image)
            if os.path.exists(image_path):
                with open(image_path, 'rb') as img_file:
                    encoded = base64.b64encode(img_file.read()).decode('utf-8')
                    ext = os.path.splitext(image_path)[1].lower()
                    mime = 'image/jpeg'
                    if ext == '.png':
                        mime = 'image/png'
                    elif ext == '.gif':
                        mime = 'image/gif'
                    return JsonResponse({'base64': f"data:{mime};base64,{encoded}"})
    except Product.DoesNotExist: # type: ignore
        pass
    return JsonResponse({'base64': None})
