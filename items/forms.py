from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'category', 'expected_price', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        help_texts = {
            'expected_price': 'Enter 0 if the item is free or intended for swapping.'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make category selection more user-friendly (optional)
        self.fields['category'].queryset = self.fields['category'].queryset.order_by('name')
        self.fields['category'].empty_label = "Select a Category"

        # Optional: Add Bootstrap classes if not using crispy-forms tags extensively
        for field_name, field in self.fields.items():
             field.widget.attrs['class'] = 'form-control'
             if isinstance(field.widget, forms.CheckboxInput):
                 field.widget.attrs['class'] = 'form-check-input'
             elif isinstance(field.widget, forms.Textarea):
                 field.widget.attrs.pop('class', None) # Crispy forms might handle textarea better
                 field.widget.attrs['class'] = 'form-control'
             elif isinstance(field.widget, forms.ClearableFileInput):
                 field.widget.attrs['class'] = 'form-control-file' # Bootstrap 4/5 might use form-control