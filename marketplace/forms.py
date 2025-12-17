from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Product, Service, Review, AvailabilityReport, ChangeRequest

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    student_id = forms.CharField(max_length=50, required=True, help_text='Your student ID number')
    institution = forms.CharField(max_length=200, required=True, help_text='Your university/institution')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phone_number', 'student_id', 'institution']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class ProductForm(forms.ModelForm):
    # Image file fields (not URL fields)
    image1 = forms.ImageField(
        required=True,
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )
    image2 = forms.ImageField(
        required=True,
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )
    image3 = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )
    
    # Video field
    video = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control', 
            'accept': 'video/*',
            'id': 'video-upload'
        }),
        help_text='Optional: Upload a video (30-90 seconds, max 50MB)'
    )
    
    class Meta:
        model = Product
        fields = [
            'category', 'title', 'description', 'vendor_price', 'condition',
            'location', 'campus', 'whatsapp_number'
        ]
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., iPhone 13 Pro Max'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Describe your product in detail...'}),
            'vendor_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '₦', 'id': 'vendor_price'}),
            'condition': forms.Select(attrs={'class': 'form-control'}),
            'whatsapp_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'WhatsApp number with country code (e.g., 23480XXXXXXXX)'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Nsukka, Enugu State'}),
            'campus': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., UNN Main Campus'}),
        }
        labels = {
            'vendor_price': 'Your Price (₦)',
        }
        help_texts = {
            'vendor_price': 'Enter your desired price. Commission will be added automatically.',
        }

class ServiceForm(forms.ModelForm):
    # Image file fields (optional for services)
    image1 = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )
    image2 = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )
    image3 = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )
    
    # Video field
    video = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control', 
            'accept': 'video/*',
            'id': 'video-upload'
        }),
        help_text='Optional: Upload a video (30-90 seconds, max 50MB)'
    )
    
    class Meta:
        model = Service
        fields = [
            'category', 'title', 'slug', 'description', 'price_type', 'vendor_price',
            'location', 'campus', 'whatsapp_number'
        ]
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Math Tutoring Services'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Describe your service in detail...'}),
            'price_type': forms.Select(attrs={'class': 'form-control'}),
            'vendor_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '₦ (Optional for negotiable services)', 'id': 'vendor_price'}),
            'whatsapp_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'WhatsApp number with country code (e.g., 23480XXXXXXXX)'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Nsukka, Enugu State'}),
            'campus': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., UNN Main Campus'}),
        }
        labels = {
            'vendor_price': 'Your Price (₦)',
        }
        help_texts = {
            'vendor_price': 'Enter your desired price. Commission will be added automatically.',
        }
        

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, f'{i} Stars') for i in range(1, 6)], attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Share your experience with this product/service...'}),
        }

class AvailabilityReportForm(forms.ModelForm):
    class Meta:
        model = AvailabilityReport
        fields = ['reason']
        widgets = {
            'reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Please describe the issue (e.g., seller not responding, product already sold, etc.)'
            }),
        }

class ChangeRequestForm(forms.ModelForm):
    class Meta:
        model = ChangeRequest
        fields = ['requested_price', 'reason']
        widgets = {
            'requested_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'New Price'}),
            'reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Why do you want to change the price?'
            }),
        }