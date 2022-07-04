from django.contrib import admin
from .models import Product, Category, FeatureValue, FeatureKey, Comment

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(FeatureValue)
admin.site.register(FeatureKey)

admin.site.register(Comment)