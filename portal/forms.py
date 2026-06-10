from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Ticket, LostFoundItem, Category


class CommentForm(forms.Form):
    """Simple form for adding a comment to a ticket or lost/found report."""
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': '3',
            'placeholder': 'Write your comment here...'
        }),
        required=True,
    )


class UserRegisterForm(UserCreationForm):
    """
    Registration form — extends Django's built-in UserCreationForm.
    Adds email, first_name, and last_name fields.
    """
    email      = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name  = forms.CharField(max_length=30, required=True)

    class Meta:
        model  = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap form-control class to every widget
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class UserUpdateForm(forms.ModelForm):
    """Updates the core Django User fields: first name, last name, and email."""
    email = forms.EmailField(required=True)

    class Meta:
        model  = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class UserProfileUpdateForm(forms.ModelForm):
    """Updates the extended UserProfile fields including the profile image."""

    class Meta:
        model  = UserProfile
        fields = ['student_id', 'phone', 'department', 'profile_image', 'bio']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            if name == 'bio':
                field.widget.attrs.update({'rows': '4'})


# ------------------------------------------------------------------
# Phase 4 Forms
# ------------------------------------------------------------------

class TicketForm(forms.ModelForm):
    """Form for submitting a new helpdesk ticket."""

    class Meta:
        model  = Ticket
        fields = ['category', 'title', 'description', 'location',
                  'priority', 'attachment', 'is_public']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show Ticket categories in the dropdown
        self.fields['category'].queryset = Category.objects.filter(
            category_type='Ticket', is_active=True
        )
        # Add Bootstrap classes to every widget
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})
        # Give the description textarea a sensible height
        self.fields['description'].widget.attrs.update({'rows': '5'})


class LostFoundItemForm(forms.ModelForm):
    """Form for submitting a new lost or found item report."""

    class Meta:
        model  = LostFoundItem
        fields = ['item_type', 'title', 'description', 'location',
                  'date_reported', 'photo', 'document',
                  'contact_email', 'is_public']
        widgets = {
            # HTML date picker for the date_reported field
            'date_reported': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            elif name != 'date_reported':   # already set in widgets above
                field.widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'rows': '5'})



class UserRegisterForm(UserCreationForm):
    """
    Registration form — extends Django's built-in UserCreationForm.
    Adds email, first_name, and last_name fields.
    """
    email      = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name  = forms.CharField(max_length=30, required=True)

    class Meta:
        model  = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap form-control class to every widget
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class UserUpdateForm(forms.ModelForm):
    """Updates the core Django User fields: first name, last name, and email."""
    email = forms.EmailField(required=True)

    class Meta:
        model  = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class UserProfileUpdateForm(forms.ModelForm):
    """Updates the extended UserProfile fields including the profile image."""

    class Meta:
        model  = UserProfile
        fields = ['student_id', 'phone', 'department', 'profile_image', 'bio']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            # Give the bio textarea a sensible height
            if name == 'bio':
                field.widget.attrs.update({'rows': '4'})
