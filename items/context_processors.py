def categories_processor(request):
    # Make sure the import is correct for this new file location
    from .models import Category # This import should work from context_processors.py
    # If you used 'from items.models import Category' in views.py, change it to the line above
    return {
        'all_categories': Category.objects.all().order_by('name')
    }