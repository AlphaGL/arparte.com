from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
import uuid
from decimal import Decimal

class User(AbstractUser):
    ACCOUNT_TYPE = (
        ('student', 'Student'),
        # ('admin', 'Admin'),
    )
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE, default='student')
    phone_number = models.CharField(max_length=15, blank=True)
    student_id = models.CharField(max_length=50, blank=True)
    institution = models.CharField(max_length=200, blank=True)
    is_verified = models.BooleanField(default=False)
    profile_image = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    CONDITION_CHOICES = (
        ('new', 'Brand New'),
        ('like_new', 'Like New'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('for_parts', 'For Parts/Not Working'),
    )
    
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('sold', 'Sold'),
        ('inactive', 'Inactive'),
        ('pending', 'Pending Approval'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    description = models.TextField()
    
    # Original price (what vendor sets)
    vendor_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    # Commission percentage applied
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    # Final price (with commission)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='good')
    
    # Location
    location = models.CharField(max_length=200)
    campus = models.CharField(max_length=200, blank=True)
    
    # WhatsApp contact
    whatsapp_number = models.CharField(max_length=20, blank=True, help_text='WhatsApp number with country code (e.g., 23480XXXXXXXX')
    
    # Images (Cloudinary URLs)
    image1 = models.URLField()
    image2 = models.URLField()
    image3 = models.URLField(blank=True)
    
    # Status & Promotion
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_featured = models.BooleanField(default=False)
    featured_until = models.DateTimeField(null=True, blank=True)
    
    # Engagement metrics
    views = models.PositiveIntegerField(default=0)
    
    # Availability reporting
    availability_reports = models.PositiveIntegerField(default=0)
    
    # Price/Image change requests
    price_change_requested = models.BooleanField(default=False)
    requested_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image_change_requested = models.BooleanField(default=False)
    change_request_note = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['is_featured', '-created_at']),
            models.Index(fields=['category', 'status']),
        ]
    
    def calculate_commission_and_price(self):
        """Calculate commission rate and final price based on vendor price"""
        if self.vendor_price:
            if self.vendor_price <= Decimal('9999'):
                self.commission_rate = Decimal('20.0')
            else:
                self.commission_rate = Decimal('10.0')

            commission_amount = (self.vendor_price * self.commission_rate) / Decimal('100')
            self.price = self.vendor_price + commission_amount
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f"{slugify(self.title)}-{str(self.id)[:8]}"
        
        # Calculate commission and final price if vendor_price is set
        if self.vendor_price:
            self.calculate_commission_and_price()
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    @property
    def average_rating(self):
        ratings = self.reviews.all()
        if ratings.exists():
            return sum(r.rating for r in ratings) / ratings.count()
        return 0
    
    @property
    def commission_amount(self):
        """Get the commission amount"""
        return self.price - self.vendor_price  

class Service(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('pending', 'Pending Approval'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='services')
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    description = models.TextField()
    
    # Pricing
    price_type = models.CharField(max_length=20, choices=(
        ('fixed', 'Fixed Price'),
        ('hourly', 'Per Hour'),
        ('negotiable', 'Negotiable'),
    ), default='fixed')
    
    # Original price (what provider sets)
    vendor_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], null=True, blank=True)
    # Commission percentage applied
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    # Final price (with commission)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], null=True, blank=True)
    
    location = models.CharField(max_length=200)
    campus = models.CharField(max_length=200, blank=True)
    
    # WhatsApp contact
    whatsapp_number = models.CharField(max_length=20, blank=True, help_text='WhatsApp number with country code (e.g., 23480XXXXXXXX')
    
    # Images
    image1 = models.URLField(blank=True)
    image2 = models.URLField(blank=True)
    image3 = models.URLField(blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_featured = models.BooleanField(default=False)
    featured_until = models.DateTimeField(null=True, blank=True)
    
    views = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']


    def calculate_commission_and_price(self):
        """Calculate commission rate and final price based on vendor price"""
        if self.vendor_price:
            if self.vendor_price <= Decimal('9999'):
                self.commission_rate = Decimal('20.0')
            else:
                self.commission_rate = Decimal('10.0')

            commission_amount = (self.vendor_price * self.commission_rate) / Decimal('100')
            self.price = self.vendor_price + commission_amount

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f"{slugify(self.title)}-{str(self.id)[:8]}"
        
        # Calculate commission and final price if vendor_price is set
        if self.vendor_price:
            self.calculate_commission_and_price()
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    @property
    def average_rating(self):
        ratings = self.service_reviews.all()
        if ratings.exists():
            return sum(r.rating for r in ratings) / ratings.count()
        return 0
    
    @property
    def commission_amount(self):
        """Get the commission amount"""
        if self.price and self.vendor_price:
            return self.price - self.vendor_price
        return 0

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='service_reviews', null=True, blank=True)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    
    is_verified_purchase = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        item = self.product or self.service
        return f"Review by {self.reviewer.username} for {item}"

class AvailabilityReport(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='availability_reports_detail')
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    is_resolved = models.BooleanField(default=False)
    admin_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Report for {self.product.title} by {self.reporter.username}"

class PromotionPackage(models.Model):
    name = models.CharField(max_length=100)
    duration_days = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['price']
    
    def __str__(self):
        return f"{self.name} - {self.duration_days} days"

class Promotion(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Payment'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    )
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='promotions', null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='promotions', null=True, blank=True)
    package = models.ForeignKey(PromotionPackage, on_delete=models.SET_NULL, null=True)
    
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    
    payment_reference = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        item = self.product or self.service
        return f"Promotion for {item} - {self.status}"

class ChangeRequest(models.Model):
    REQUEST_TYPE = (
        ('price', 'Price Change'),
        ('images', 'Image Change'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='change_requests')
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPE)
    
    # For price changes
    current_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    requested_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # For image changes
    new_images = models.JSONField(null=True, blank=True)  # Store URLs
    
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_note = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_requests')
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.request_type} request for {self.product.title}"

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_sent')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_received')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')
    
    subject = models.CharField(max_length=200)
    message = models.TextField()
    
    is_read = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Message from {self.sender.username} to {self.recipient.username}"