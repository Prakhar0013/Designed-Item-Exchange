from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Item, Category
from .forms import ItemForm
from django.db.models import Q # For search/filtering

# --- Home Page / Item List ---
class ItemListView(ListView):
    model = Item
    template_name = 'items/home.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'items'
    ordering = ['-created_at'] # Show newest items first
    paginate_by = 9 # Show 9 items per page

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_available=True) # Only show available items
        category_slug = self.request.GET.get('category')
        query = self.request.GET.get('q')

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)
        if query:
             queryset = queryset.filter(
                 Q(name__icontains=query) |
                 Q(description__icontains=query)
             )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all().order_by('name')
        context['selected_category'] = self.request.GET.get('category', '')
        context['search_query'] = self.request.GET.get('q', '')
        return context


# --- Item Detail ---
class ItemDetailView(DetailView):
    model = Item
    template_name = 'items/item_detail.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Check if the viewer is the owner
        context['is_owner'] = self.request.user == self.object.owner
        # Add logic later to check if a chat already exists
        return context


# --- Create Item ---
class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    form_class = ItemForm # Use the custom form
    template_name = 'items/item_form.html'
    success_url = reverse_lazy('my_posts') # Redirect to 'my posts' after creation

    def form_valid(self, form):
        form.instance.owner = self.request.user # Assign current user as owner
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = "Post New Item"
        return context


# --- My Posts ---
class MyPostsView(LoginRequiredMixin, ListView):
    model = Item
    template_name = 'items/my_posts.html'
    context_object_name = 'my_items'
    paginate_by = 10

    def get_queryset(self):
        # Filter items owned by the current logged-in user
        return Item.objects.filter(owner=self.request.user).order_by('-created_at')


# --- Edit Item ---
class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    form_class = ItemForm
    template_name = 'items/item_form.html'
    # success_url will redirect to item_detail by default if get_absolute_url is defined

    def form_valid(self, form):
        form.instance.owner = self.request.user # Ensure owner isn't changed
        return super().form_valid(form)

    def test_func(self):
        # Check if the current user is the owner of the item
        item = self.get_object()
        return self.request.user == item.owner

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_title'] = "Edit Item"
        return context


# --- Delete Item ---
class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item
    template_name = 'items/item_confirm_delete.html'
    success_url = reverse_lazy('my_posts') # Redirect to my posts after deletion

    def test_func(self):
        # Check if the current user is the owner of the item
        item = self.get_object()
        return self.request.user == item.owner

# --- Context Processor (needed for settings.py) ---
# Create this file: items/context_processors.py
def categories_processor(request):
    return {
        'all_categories': Category.objects.all().order_by('name')
    }