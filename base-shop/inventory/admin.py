from django.contrib import admin
from .models import Product, Category, FeatureValue, FeatureKey, Comment, SubCategory

admin.site.register(Product)
admin.site.register(Category)

admin.site.register(SubCategory)
admin.site.register(FeatureValue)
admin.site.register(FeatureKey)

admin.site.register(Comment)