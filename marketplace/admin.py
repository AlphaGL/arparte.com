from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils import timezone
from django.db.models import Count, Avg
from .models import (
    User, Category, Product, Service, Review,
    AvailabilityReport, PromotionPackage, Promotion,
    ChangeRequest, Message
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'account_type', 'institution', 'is_verified', 'date_joined']
    list_filter = ['account_type', 'is_verified', 'is_staff', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'student_id', 'institution']
    readonly_fields = ['date_joined', 'last_login', 'created_at']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Student Information', {
            'fields': ('account_type', 'phone_number', 'student_id', 'institution', 'is_verified', 'profile_image', 'created_at')
        }),
    )
    
    actions = ['verify_users', 'unverify_users']
    
    def verify_users(self, request, queryset):
        count = queryset.update(is_verified=True)
        self.message_user(request, f'{count} user(s) verified successfully.')
    verify_users.short_description = 'Verify selected users'
    
    def unverify_users(self, request, queryset):
        count = queryset.update(is_verified=False)
        self.message_user(request, f'{count} user(s) unverified.')
    unverify_users.short_description = 'Unverify selected users'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'is_active', 'product_count', 'service_count']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['product_count', 'service_count']
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Products'
    
    def service_count(self, obj):
        return obj.services.count()
    service_count.short_description = 'Services'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'seller', 'category', 'price', 'condition', 
        'status', 'is_featured', 'views', 'avg_rating', 'created_at'
    ]
    list_filter = [
        'status', 'condition', 'is_featured', 'category', 
        'availability_reports', 'created_at'
    ]
    search_fields = ['title', 'description', 'seller__username', 'location', 'campus']
    readonly_fields = [
        'id', 'slug', 'views', 'created_at', 'updated_at', 
        'availability_reports', 'avg_rating', 'image_preview'
    ]
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'seller', 'category', 'title', 'slug', 'description')
        }),
        ('Pricing & Condition', {
            'fields': ('price', 'condition')
        }),
        ('Location', {
            'fields': ('location', 'campus')
        }),
        ('Images', {
            'fields': ('image_preview', 'image1', 'image2', 'image3', 'image4', 'image5')
        }),
        ('Status & Promotion', {
            'fields': ('status', 'is_featured', 'featured_until')
        }),
        ('Metrics', {
            'fields': ('views', 'availability_reports', 'avg_rating')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    actions = ['mark_as_featured', 'mark_as_active', 'mark_as_sold', 'mark_as_inactive']
    
    def avg_rating(self, obj):
        return round(obj.average_rating, 1) if obj.average_rating else 'No ratings'
    avg_rating.short_description = 'Avg Rating'
    
    def image_preview(self, obj):
        if obj.image1:
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 300px;"/>',
                obj.image1
            )
        return 'No image'
    image_preview.short_description = 'Primary Image Preview'
    
    def mark_as_featured(self, request, queryset):
        count = queryset.update(is_featured=True)
        self.message_user(request, f'{count} product(s) marked as featured.')
    mark_as_featured.short_description = 'Mark as featured'
    
    def mark_as_active(self, request, queryset):
        count = queryset.update(status='active')
        self.message_user(request, f'{count} product(s) marked as active.')
    mark_as_active.short_description = 'Mark as active'
    
    def mark_as_sold(self, request, queryset):
        count = queryset.update(status='sold')
        self.message_user(request, f'{count} product(s) marked as sold.')
    mark_as_sold.short_description = 'Mark as sold'
    
    def mark_as_inactive(self, request, queryset):
        count = queryset.update(status='inactive')
        self.message_user(request, f'{count} product(s) marked as inactive.')
    mark_as_inactive.short_description = 'Mark as inactive'


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'provider', 'category', 'price_type', 'price',
        'status', 'is_featured', 'views', 'avg_rating', 'created_at'
    ]
    list_filter = ['status', 'price_type', 'is_featured', 'category', 'created_at']
    search_fields = ['title', 'description', 'provider__username', 'location', 'campus']
    readonly_fields = [
        'id', 'slug', 'views', 'created_at', 'updated_at', 'avg_rating', 'image_preview'
    ]
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'provider', 'category', 'title', 'slug', 'description')
        }),
        ('Pricing', {
            'fields': ('price_type', 'price')
        }),
        ('Location', {
            'fields': ('location', 'campus')
        }),
        ('Images', {
            'fields': ('image_preview', 'image1', 'image2', 'image3')
        }),
        ('Status & Promotion', {
            'fields': ('status', 'is_featured', 'featured_until')
        }),
        ('Metrics', {
            'fields': ('views', 'avg_rating')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    actions = ['mark_as_featured', 'mark_as_active', 'mark_as_inactive']
    
    def avg_rating(self, obj):
        return round(obj.average_rating, 1) if obj.average_rating else 'No ratings'
    avg_rating.short_description = 'Avg Rating'
    
    def image_preview(self, obj):
        if obj.image1:
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 300px;"/>',
                obj.image1
            )
        return 'No image'
    image_preview.short_description = 'Primary Image Preview'
    
    def mark_as_featured(self, request, queryset):
        count = queryset.update(is_featured=True)
        self.message_user(request, f'{count} service(s) marked as featured.')
    mark_as_featured.short_description = 'Mark as featured'
    
    def mark_as_active(self, request, queryset):
        count = queryset.update(status='active')
        self.message_user(request, f'{count} service(s) marked as active.')
    mark_as_active.short_description = 'Mark as active'
    
    def mark_as_inactive(self, request, queryset):
        count = queryset.update(status='inactive')
        self.message_user(request, f'{count} service(s) marked as inactive.')
    mark_as_inactive.short_description = 'Mark as inactive'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        'reviewer', 'get_item', 'rating', 'is_approved', 
        'is_verified_purchase', 'created_at'
    ]
    list_filter = ['rating', 'is_approved', 'is_verified_purchase', 'created_at']
    search_fields = ['reviewer__username', 'comment', 'product__title', 'service__title']
    readonly_fields = ['created_at', 'get_item']
    
    fieldsets = (
        ('Review Information', {
            'fields': ('reviewer', 'get_item', 'product', 'service', 'rating', 'comment')
        }),
        ('Status', {
            'fields': ('is_approved', 'is_verified_purchase')
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )
    
    actions = ['approve_reviews', 'unapprove_reviews']
    
    def get_item(self, obj):
        return obj.product or obj.service
    get_item.short_description = 'Item'
    
    def approve_reviews(self, request, queryset):
        count = queryset.update(is_approved=True)
        self.message_user(request, f'{count} review(s) approved.')
    approve_reviews.short_description = 'Approve selected reviews'
    
    def unapprove_reviews(self, request, queryset):
        count = queryset.update(is_approved=False)
        self.message_user(request, f'{count} review(s) unapproved.')
    unapprove_reviews.short_description = 'Unapprove selected reviews'


@admin.register(AvailabilityReport)
class AvailabilityReportAdmin(admin.ModelAdmin):
    list_display = [
        'product', 'reporter', 'is_resolved', 'created_at', 'resolved_at'
    ]
    list_filter = ['is_resolved', 'created_at']
    search_fields = ['product__title', 'reporter__username', 'reason']
    readonly_fields = ['created_at', 'product', 'reporter']
    
    fieldsets = (
        ('Report Information', {
            'fields': ('product', 'reporter', 'reason')
        }),
        ('Resolution', {
            'fields': ('is_resolved', 'admin_note', 'resolved_at')
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )
    
    actions = ['mark_as_resolved', 'mark_as_unresolved']
    
    def mark_as_resolved(self, request, queryset):
        count = queryset.update(is_resolved=True, resolved_at=timezone.now())
        self.message_user(request, f'{count} report(s) marked as resolved.')
    mark_as_resolved.short_description = 'Mark as resolved'
    
    def mark_as_unresolved(self, request, queryset):
        count = queryset.update(is_resolved=False, resolved_at=None)
        self.message_user(request, f'{count} report(s) marked as unresolved.')
    mark_as_unresolved.short_description = 'Mark as unresolved'


@admin.register(PromotionPackage)
class PromotionPackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'duration_days', 'price', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    
    fieldsets = (
        ('Package Information', {
            'fields': ('name', 'duration_days', 'price', 'description')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = [
        'get_item', 'package', 'amount_paid', 'status',
        'start_date', 'end_date', 'created_at'
    ]
    list_filter = ['status', 'created_at', 'start_date', 'end_date']
    search_fields = ['product__title', 'service__title', 'payment_reference']
    readonly_fields = ['created_at', 'get_item']
    
    fieldsets = (
        ('Promotion Information', {
            'fields': ('get_item', 'product', 'service', 'package', 'amount_paid')
        }),
        ('Status & Duration', {
            'fields': ('status', 'start_date', 'end_date')
        }),
        ('Payment', {
            'fields': ('payment_reference',)
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )
    
    actions = ['activate_promotions', 'expire_promotions']
    
    def get_item(self, obj):
        return obj.product or obj.service
    get_item.short_description = 'Item'
    
    def activate_promotions(self, request, queryset):
        count = 0
        for promo in queryset:
            if promo.status == 'pending':
                promo.status = 'active'
                promo.start_date = timezone.now()
                if promo.package:
                    from datetime import timedelta
                    promo.end_date = timezone.now() + timedelta(days=promo.package.duration_days)
                promo.save()
                
                # Mark item as featured
                item = promo.product or promo.service
                if item:
                    item.is_featured = True
                    item.featured_until = promo.end_date
                    item.save()
                count += 1
        
        self.message_user(request, f'{count} promotion(s) activated.')
    activate_promotions.short_description = 'Activate selected promotions'
    
    def expire_promotions(self, request, queryset):
        count = queryset.update(status='expired')
        self.message_user(request, f'{count} promotion(s) expired.')
    expire_promotions.short_description = 'Expire selected promotions'


@admin.register(ChangeRequest)
class ChangeRequestAdmin(admin.ModelAdmin):
    list_display = [
        'product', 'request_type', 'status', 'created_at', 'reviewed_by'
    ]
    list_filter = ['request_type', 'status', 'created_at']
    search_fields = ['product__title', 'reason']
    readonly_fields = ['created_at', 'product', 'request_type', 'current_price']
    
    fieldsets = (
        ('Request Information', {
            'fields': ('product', 'request_type', 'reason')
        }),
        ('Price Change Details', {
            'fields': ('current_price', 'requested_price'),
            'classes': ('collapse',)
        }),
        ('Image Change Details', {
            'fields': ('new_images',),
            'classes': ('collapse',)
        }),
        ('Review', {
            'fields': ('status', 'admin_note', 'reviewed_by', 'reviewed_at')
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )
    
    actions = ['approve_requests', 'reject_requests']
    
    def approve_requests(self, request, queryset):
        count = 0
        for change_req in queryset.filter(status='pending'):
            product = change_req.product
            
            if change_req.request_type == 'price' and change_req.requested_price:
                product.price = change_req.requested_price
                product.save()
            elif change_req.request_type == 'images' and change_req.new_images:
                images = change_req.new_images
                for i, url in enumerate(images[:5], 1):
                    setattr(product, f'image{i}', url)
                product.save()
            
            change_req.status = 'approved'
            change_req.reviewed_by = request.user
            change_req.reviewed_at = timezone.now()
            change_req.save()
            count += 1
        
        self.message_user(request, f'{count} request(s) approved.')
    approve_requests.short_description = 'Approve selected requests'
    
    def reject_requests(self, request, queryset):
        count = queryset.filter(status='pending').update(
            status='rejected',
            reviewed_by=request.user,
            reviewed_at=timezone.now()
        )
        self.message_user(request, f'{count} request(s) rejected.')
    reject_requests.short_description = 'Reject selected requests'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [
        'sender', 'recipient', 'subject', 'get_item', 
        'is_read', 'created_at'
    ]
    list_filter = ['is_read', 'created_at']
    search_fields = [
        'sender__username', 'recipient__username', 
        'subject', 'message', 'product__title', 'service__title'
    ]
    readonly_fields = ['created_at', 'get_item']
    
    fieldsets = (
        ('Message Information', {
            'fields': ('sender', 'recipient', 'get_item', 'product', 'service')
        }),
        ('Content', {
            'fields': ('subject', 'message')
        }),
        ('Status', {
            'fields': ('is_read',)
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )
    
    def get_item(self, obj):
        return obj.product or obj.service or 'General Message'
    get_item.short_description = 'Related Item'