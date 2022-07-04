from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required


from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, FormView, DeleteView, DetailView, CreateView

from .forms import CommentForm
from .models import Product, Comment


class ProductList(ListView):
    model = Product
    template_name: str = "inventory/shop.html"
    context_object_name = "products"
    paginate_by = 6

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("search")
        if q:
            qs = qs.filter(product_name__contains=q)
        return qs


class ProductDetail(DetailView):
    model = Product
    template_name: str = "inventory/product-details.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        comments = self.get_object().comments.all()
        comment_form = CommentForm()
        context['comments'] = comments
        context['comment_form'] = comment_form
        return context


@login_required(login_url="/login/")
def add_comment(request, product_pk):
    if request.method == "POST":

        comment_form = CommentForm(request.POST)
        product = get_object_or_404(Product, pk=product_pk)
        if comment_form.is_valid():
            Comment.objects.create(product=product, **comment_form.cleaned_data)
            return redirect(reverse_lazy('detail', kwargs={'pk': product.pk}))
        else:
            comments = product.comments.all()
            context = {
                "product": product,
                "comments": comments,
                "comment_form": comment_form
            }
            return render(request, "inventory/product-details.html", context)

    else:
        return HttpResponse(status=400)
