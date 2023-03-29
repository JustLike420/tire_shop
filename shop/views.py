from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Product, OrderItem, Order
from django.contrib.auth.decorators import login_required
from django.utils import timezone


def home_page(request):
    return render(request, 'home_page.html')


class ProductListView(ListView):
    model = Product
    paginate_by = 1
    context_object_name = 'products'
    template_name = 'product_list.html'
    queryset = Product.objects.filter(is_active=True)


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'product_detail.html'


class ProductCreateView(PermissionRequiredMixin, CreateView):
    model = Product
    permission_required = 'user.is_superuser'
    template_name = 'product_create_or_update.html'
    fields = ('name', 'description', 'price', 'picture', 'is_active')

    def handle_no_permission(self):
        return redirect('product_list')


class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    model = Product
    permission_required = 'user.is_superuser'
    template_name = 'product_create_or_update.html'
    fields = ('name', 'description', 'price', 'picture', 'is_active')

    def handle_no_permission(self):
        return redirect('product_list')


class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    model = Product
    permission_required = 'user.is_superuser'
    template_name = 'product_delete.html'
    success_url = reverse_lazy('product_list')

    def handle_no_permission(self):
        return redirect('product_list')


@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__pk=product.pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Кол-во товара обновлено")
            return redirect("order")
        else:
            messages.info(request, "Этот товар был добавлен в вашу корзину.")
            order.items.add(order_item)
            return redirect("order")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Этот товар был добавлен в вашу корзину.")
        return redirect("order")


@login_required
def remove_from_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__pk=product.pk).exists():
            order_item = OrderItem.objects.filter(
                product=product,
                user=request.user,
                ordered=False)[0]
            order.items.remove(order_item)
            messages.info(request, "Товар был удален из вашей корзины.")
            return redirect("order")
        else:
            messages.info(request, "Этого товара нет в вашей корзине.")
            return redirect("order")
    else:
        messages.info(request, "У вас нет активного заказа.")
        return redirect("order")


@login_required
def remove_single_item_from_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__pk=product.pk).exists():
            order_item = OrderItem.objects.filter(
                product=product,
                user=request.user,
                ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "Кол-во товара обновлено")
            return redirect("order")
        else:
            messages.info(request, "Этого товара нет в вашей корзине.")
            return redirect("order")
    else:
        messages.info(request, "У вас нет активного заказа.")
        return redirect("order")


class OrderSummeryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order,
            }
            return render(self.request, 'order.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "У вас нету активного заказа")
            return redirect("/")
