from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
        labels = {
            'name': 'Your Name',
            'email': 'Email Address',
            'body': 'Your Comment',
        }
        help_texts = {
            'body': 'Share your thoughts (minimum 10 characters)',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name',
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com',
                'required': True,
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your Comment',
                'rows': 4,
                'required': True,
            }),
        }
    
    def clean_name(self):
        """Validate name field."""
        name = self.cleaned_data.get('name')
        
        if len(name) < 3:
            raise forms.ValidationError('Name must be at least 3 characters.')
        
        # Basic spam detection
        spam_keywords = ['spam', 'viagra', 'casino', 'buy now']
        if any(keyword in name.lower() for keyword in spam_keywords):
            raise forms.ValidationError('Invalid name detected.')
        
        return name
    
    def clean_body(self):
        """Validate comment body."""
        body = self.cleaned_data.get('body')
        
        if len(body) < 10:
            raise forms.ValidationError('Comment must be at least 10 characters.')
        
        # Detect excessive links (spam)
        if body.count('http') > 2:
            raise forms.ValidationError('Too many links. Maximum 2 links allowed.')
        
        return body
