from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg, Count
from django.core.paginator import Paginator
from django.utils import timezone
from django.http import JsonResponse
from urllib.parse import quote
import cloudinary.uploader
from .models import (
    User, Category, Product, Service, Review, 
    AvailabilityReport, PromotionPackage, Promotion, 
    ChangeRequest, Message
)
from .forms import (
    UserRegisterForm, UserLoginForm, ProductForm, ServiceForm,
    ReviewForm, AvailabilityReportForm, ChangeRequestForm
)

def error_404(request, exception):
    """Custom 404 error page"""
    return render(request, '404.html', status=404)

def error_403(request, exception):
    """Custom 403 error page"""
    return render(request, '403.html', status=403)

def error_500(request):
    """Custom 500 error page"""
    return render(request, '500.html', status=500)

def error_400(request, exception):
    """Custom 400 error page"""
    return render(request, '400.html', status=400)

# Admin WhatsApp number
ADMIN_WHATSAPP = "2348135923286"

def upload_to_cloudinary(image_file):
    """Upload image to Cloudinary and return the URL"""
    try:
        upload_result = cloudinary.uploader.upload(
            image_file,
            folder="arparte_products",
            transformation=[
                {'width': 800, 'height': 600, 'crop': 'limit'},
                {'quality': 'auto:good'}
            ]
        )
        return upload_result['secure_url']
    except Exception as e:
        print(f"Cloudinary upload error: {e}")
        return None

def home(request):
    """Homepage with featured items and categories"""
    featured_products = Product.objects.filter(
        status='active', is_featured=True
    ).order_by('-created_at')[:8]
    
    featured_services = Service.objects.filter(
        status='active', is_featured=True
    ).order_by('-created_at')[:8]
    
    categories = Category.objects.filter(is_active=True)
    
    recent_products = Product.objects.filter(status='active').order_by('-created_at')[:12]
    
    context = {
        'featured_products': featured_products,
        'featured_services': featured_services,
        'categories': categories,
        'recent_products': recent_products,
    }
    return render(request, 'marketplace/home.html', context)

def register(request):
    """User registration"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome to ARPARTE! Your account has been created.')
            return redirect('home')
    else:
        form = UserRegisterForm()
    
    return render(request, 'marketplace/register.html', {'form': form})

def user_login(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            
            if user:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'marketplace/login.html', {'form': form})

def user_logout(request):
    """User logout"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')

def browse_products(request):
    """Browse all products with filters"""
    products = Product.objects.filter(status='active')
    
    # Filters
    category_slug = request.GET.get('category')
    search_query = request.GET.get('q')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    condition = request.GET.get('condition')
    campus = request.GET.get('campus')
    sort_by = request.GET.get('sort', '-created_at')
    
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    if search_query:
        products = products.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    if min_price:
        products = products.filter(price__gte=min_price)
    
    if max_price:
        products = products.filter(price__lte=max_price)
    
    if condition:
        products = products.filter(condition=condition)
    
    if campus:
        products = products.filter(campus__icontains=campus)
    
    # Sorting
    if sort_by in ['-created_at', 'price', '-price', 'title']:
        products = products.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'current_category': category_slug,
        'search_query': search_query,
    }
    return render(request, 'marketplace/browse_products.html', context)

def browse_services(request):
    """Browse all services with filters"""
    services = Service.objects.filter(status='active')
    
    # Filters
    category_slug = request.GET.get('category')
    search_query = request.GET.get('q')
    price_type = request.GET.get('price_type')
    campus = request.GET.get('campus')
    sort_by = request.GET.get('sort', '-created_at')
    
    if category_slug:
        services = services.filter(category__slug=category_slug)
    
    if search_query:
        services = services.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    if price_type:
        services = services.filter(price_type=price_type)
    
    if campus:
        services = services.filter(campus__icontains=campus)
    
    if sort_by in ['-created_at', 'price', '-price', 'title']:
        services = services.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(services, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'current_category': category_slug,
        'search_query': search_query,
    }
    return render(request, 'marketplace/browse_services.html', context)

def product_detail(request, slug):
    """Product detail page"""
    product = get_object_or_404(Product, slug=slug)
    
    # Increment views
    product.views += 1
    product.save(update_fields=['views'])
    
    # Get reviews
    reviews = product.reviews.filter(is_approved=True).order_by('-created_at')
    
    # Get related products
    related_products = Product.objects.filter(
        category=product.category,
        status='active'
    ).exclude(id=product.id)[:4]
    
    # Check if user has reviewed
    user_has_reviewed = False
    if request.user.is_authenticated:
        user_has_reviewed = reviews.filter(reviewer=request.user).exists()
    
    # Generate WhatsApp contact link
    product_url = request.build_absolute_uri()
    whatsapp_message = f"Hello, I'm interested in this product:\n\n*{product.title}*\nPrice: ₦{product.price:,.0f}\n\n{product_url}"
    whatsapp_link = f"https://wa.me/{ADMIN_WHATSAPP}?text={quote(whatsapp_message)}"
    
    # Show vendor phone if user is admin
    show_vendor_phone = request.user.is_authenticated and request.user.is_staff
    
    context = {
        'product': product,
        'reviews': reviews,
        'related_products': related_products,
        'user_has_reviewed': user_has_reviewed,
        'whatsapp_link': whatsapp_link,
        'show_vendor_phone': show_vendor_phone,
    }
    return render(request, 'marketplace/product_detail.html', context)

def service_detail(request, slug):
    """Service detail page"""
    service = get_object_or_404(Service, slug=slug)
    
    # Increment views
    service.views += 1
    service.save(update_fields=['views'])
    
    # Get reviews
    reviews = service.service_reviews.filter(is_approved=True).order_by('-created_at')
    
    # Get related services
    related_services = Service.objects.filter(
        category=service.category,
        status='active'
    ).exclude(id=service.id)[:4]
    
    # Check if user has reviewed
    user_has_reviewed = False
    if request.user.is_authenticated:
        user_has_reviewed = reviews.filter(reviewer=request.user).exists()
    
    # Generate WhatsApp contact link
    service_url = request.build_absolute_uri()
    whatsapp_message = f"Hello, I'm interested in this service:\n\n*{service.title}*\n{f'Price: ₦{service.price:,.0f}' if service.price else service.get_price_type_display()}\n\n{service_url}"
    whatsapp_link = f"https://wa.me/{ADMIN_WHATSAPP}?text={quote(whatsapp_message)}"
    
    # Show provider phone if user is admin
    show_vendor_phone = request.user.is_authenticated and request.user.is_staff
    
    context = {
        'service': service,
        'reviews': reviews,
        'related_services': related_services,
        'user_has_reviewed': user_has_reviewed,
        'whatsapp_link': whatsapp_link,
        'show_vendor_phone': show_vendor_phone,
    }
    return render(request, 'marketplace/service_detail.html', context)

@login_required
def create_product(request):
    """Create a new product"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            
            # Upload images to Cloudinary
            image1 = request.FILES.get('image1')
            image2 = request.FILES.get('image2')
            image3 = request.FILES.get('image3')
            
            if image1:
                product.image1 = upload_to_cloudinary(image1)
            if image2:
                product.image2 = upload_to_cloudinary(image2)
            if image3:
                product.image3 = upload_to_cloudinary(image3)
            
            # Check if all required images were uploaded successfully
            if not product.image1 or not product.image2:
                messages.error(request, 'Failed to upload images. Please try again.')
                return render(request, 'marketplace/create_product.html', {'form': form})
            
            product.save()
            messages.success(request, f'Product created successfully! Final price: ₦{product.price:,.0f} (includes {product.commission_rate}% commission)')
            return redirect('my_products')
    else:
        form = ProductForm()
    
    return render(request, 'marketplace/create_product.html', {'form': form})

@login_required
def create_service(request):
    """Create a new service"""
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.provider = request.user
            
            # Upload images to Cloudinary (optional for services)
            image1 = request.FILES.get('image1')
            image2 = request.FILES.get('image2')
            image3 = request.FILES.get('image3')
            
            if image1:
                service.image1 = upload_to_cloudinary(image1)
            if image2:
                service.image2 = upload_to_cloudinary(image2)
            if image3:
                service.image3 = upload_to_cloudinary(image3)
            
            service.save()
            
            if service.price:
                messages.success(request, f'Service created successfully! Final price: ₦{service.price:,.0f} (includes {service.commission_rate}% commission)')
            else:
                messages.success(request, 'Service created successfully!')
            
            return redirect('my_services')
    else:
        form = ServiceForm()
    
    return render(request, 'marketplace/create_service.html', {'form': form})

@login_required
def my_products(request):
    """User's products dashboard"""
    products = Product.objects.filter(seller=request.user).order_by('-created_at')
    
    context = {
        'products': products,
    }
    return render(request, 'marketplace/my_products.html', context)

@login_required
def my_services(request):
    """User's services dashboard"""
    services = Service.objects.filter(provider=request.user).order_by('-created_at')
    
    context = {
        'services': services,
    }
    return render(request, 'marketplace/my_services.html', context)

@login_required
def edit_product(request, pk):
    """Edit product (limited fields)"""
    product = get_object_or_404(Product, id=pk, seller=request.user)
    
    if request.method == 'POST':
        # Only allow editing title, description, location, condition, status
        product.title = request.POST.get('title', product.title)
        product.description = request.POST.get('description', product.description)
        product.location = request.POST.get('location', product.location)
        product.campus = request.POST.get('campus', product.campus)
        product.condition = request.POST.get('condition', product.condition)
        product.status = request.POST.get('status', product.status)
        product.save()
        
        messages.success(request, 'Product updated successfully!')
        return redirect('my_products')
    
    return render(request, 'marketplace/edit_product.html', {'product': product})

@login_required
def edit_service(request, pk):
    """Edit service (limited fields)"""
    service = get_object_or_404(Service, id=pk, provider=request.user)
    
    if request.method == 'POST':
        service.title = request.POST.get('title', service.title)
        service.description = request.POST.get('description', service.description)
        service.location = request.POST.get('location', service.location)
        service.campus = request.POST.get('campus', service.campus)
        service.status = request.POST.get('status', service.status)
        service.save()
        
        messages.success(request, 'Service updated successfully!')
        return redirect('my_services')
    
    return render(request, 'marketplace/edit_service.html', {'service': service})

@login_required
def delete_product(request, pk):
    """Delete product"""
    product = get_object_or_404(Product, id=pk, seller=request.user)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('my_products')
    
    return render(request, 'marketplace/confirm_delete.html', {'item': product, 'type': 'product'})

@login_required
def delete_service(request, pk):
    """Delete service"""
    service = get_object_or_404(Service, id=pk, provider=request.user)
    
    if request.method == 'POST':
        service.delete()
        messages.success(request, 'Service deleted successfully!')
        return redirect('my_services')
    
    return render(request, 'marketplace/confirm_delete.html', {'item': service, 'type': 'service'})

@login_required
def request_price_change(request, pk):
    """Request price change for product"""
    product = get_object_or_404(Product, id=pk, seller=request.user)
    
    if request.method == 'POST':
        new_vendor_price = request.POST.get('new_price')
        reason = request.POST.get('reason')
        
        ChangeRequest.objects.create(
            product=product,
            request_type='price',
            current_price=product.vendor_price,
            requested_price=new_vendor_price,
            reason=reason
        )
        
        messages.success(request, 'Price change request submitted! Admin will review it.')
        return redirect('my_products')
    
    return render(request, 'marketplace/request_price_change.html', {'product': product})

@login_required
def request_image_change(request, pk):
    """Request image change for product"""
    product = get_object_or_404(Product, id=pk, seller=request.user)
    
    if request.method == 'POST':
        # Get new image files
        image1 = request.FILES.get('image1')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        
        new_images = []
        if image1:
            url = upload_to_cloudinary(image1)
            if url:
                new_images.append(url)
        if image2:
            url = upload_to_cloudinary(image2)
            if url:
                new_images.append(url)
        if image3:
            url = upload_to_cloudinary(image3)
            if url:
                new_images.append(url)
        
        reason = request.POST.get('reason')
        
        ChangeRequest.objects.create(
            product=product,
            request_type='images',
            new_images=new_images,
            reason=reason
        )
        
        messages.success(request, 'Image change request submitted! Admin will review it.')
        return redirect('my_products')
    
    return render(request, 'marketplace/request_image_change.html', {'product': product})

@login_required
def add_review(request, slug, item_type):
    """Add review for product or service"""
    if item_type == 'product':
        item = get_object_or_404(Product, slug=slug)
        existing_review = Review.objects.filter(product=item, reviewer=request.user)
    else:
        item = get_object_or_404(Service, slug=slug)
        existing_review = Review.objects.filter(service=item, reviewer=request.user)
    
    if existing_review.exists():
        messages.warning(request, 'You have already reviewed this item.')
        return redirect(item.get_absolute_url() if hasattr(item, 'get_absolute_url') else 'home')
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            
            if item_type == 'product':
                review.product = item
            else:
                review.service = item
            
            review.save()
            messages.success(request, 'Review submitted successfully!')
            return redirect('product_detail' if item_type == 'product' else 'service_detail', slug=slug)
    else:
        form = ReviewForm()
    
    context = {
        'form': form,
        'item': item,
        'item_type': item_type,
    }
    return render(request, 'marketplace/add_review.html', context)

@login_required
def report_availability(request, slug):
    """Report product availability issue"""
    product = get_object_or_404(Product, slug=slug)
    
    if request.method == 'POST':
        form = AvailabilityReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.product = product
            report.reporter = request.user
            report.save()
            
            # Increment product's availability reports count
            product.availability_reports += 1
            product.save(update_fields=['availability_reports'])
            
            messages.success(request, 'Thank you for reporting! Admin will investigate.')
            return redirect('product_detail', slug=slug)
    else:
        form = AvailabilityReportForm()
    
    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'marketplace/report_availability.html', context)

@login_required
def promote_product(request, pk):
    """Promote product (select package)"""
    product = get_object_or_404(Product, id=pk, seller=request.user)
    packages = PromotionPackage.objects.filter(is_active=True)
    
    if request.method == 'POST':
        package_id = request.POST.get('package')
        package = get_object_or_404(PromotionPackage, id=package_id)
        
        # Create promotion (pending payment)
        Promotion.objects.create(
            product=product,
            package=package,
            amount_paid=package.price,
            status='pending'
        )
        
        messages.success(request, f'Promotion request created! Please proceed to payment.')
        return redirect('my_products')
    
    context = {
        'product': product,
        'packages': packages,
    }
    return render(request, 'marketplace/promote_product.html', context)

@login_required
def promote_service(request, pk):
    """Promote service (select package)"""
    service = get_object_or_404(Service, id=pk, provider=request.user)
    packages = PromotionPackage.objects.filter(is_active=True)
    
    if request.method == 'POST':
        package_id = request.POST.get('package')
        package = get_object_or_404(PromotionPackage, id=package_id)
        
        # Create promotion (pending payment)
        Promotion.objects.create(
            service=service,
            package=package,
            amount_paid=package.price,
            status='pending'
        )
        
        messages.success(request, f'Promotion request created! Please proceed to payment.')
        return redirect('my_services')
    
    context = {
        'service': service,
        'packages': packages,
    }
    return render(request, 'marketplace/promote_service.html', context)

@login_required
def contact_seller(request, slug, item_type):
    """Contact seller/provider - Redirect to WhatsApp"""
    if item_type == 'product':
        item = get_object_or_404(Product, slug=slug)
        vendor = item.seller
    else:
        item = get_object_or_404(Service, slug=slug)
        vendor = item.provider
    
    # Generate WhatsApp link with product/service info
    item_url = request.build_absolute_uri(f"/{item_type}/{slug}/")
    whatsapp_message = f"Hello, I'm interested in:\n\n*{item.title}*\n{f'Price: ₦{item.price:,.0f}' if item.price else ''}\n\n{item_url}"
    whatsapp_link = f"https://wa.me/{ADMIN_WHATSAPP}?text={quote(whatsapp_message)}"
    
    return redirect(whatsapp_link)

@login_required
def my_messages(request):
    """View user's messages"""
    received = Message.objects.filter(recipient=request.user).order_by('-created_at')
    sent = Message.objects.filter(sender=request.user).order_by('-created_at')
    
    # Mark as read
    if request.GET.get('mark_read'):
        msg_id = request.GET.get('mark_read')
        msg = Message.objects.filter(id=msg_id, recipient=request.user).first()
        if msg:
            msg.is_read = True
            msg.save()
    
    context = {
        'received': received,
        'sent': sent,
    }
    return render(request, 'marketplace/my_messages.html', context)