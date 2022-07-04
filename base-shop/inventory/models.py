from django.db import models
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator



class Category(models.Model):
    category_name = models.CharField(max_length=255)
    subcategory = models.ForeignKey(
        'Category', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_name = models.CharField(max_length=255)
    product_price = models.FloatField()
    rate = models.FloatField(null=True, blank=True)
    total_quantity = models.IntegerField()
    available_quantity = models.IntegerField(null=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='Products/', default="default.jpg")
    slug = models.SlugField(null=True, blank=True)
    discount_price = models.FloatField(null=True, blank=True)
    discount_percentage = models.FloatField(default=0)
    added_date = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    feature_value = models.ForeignKey(
        'FeatureValue', on_delete=models.RESTRICT)

    supplier = models.ManyToManyField('accounts.Supplier')

    def __str__(self):
        return self.product_name

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.product_name, allow_unicode=True)

        if self.available_quantity is None:  # age nadarim ke available che ghadre dar on record
            self.available_quantity = self.total_quantity

        if self.available_quantity > self.total_quantity:
            raise Exception(
                'available quantity can not be greater than total quantity')

        if self.discount_percentage > 0:
            self.discount_price = self.product_price - \
                                  (self.product_price * self.discount_percentage) / 100

        return super().save(*args, **kwargs)


class FeatureValue(models.Model):
    value = models.CharField(max_length=255)
    feature_key = models.ForeignKey('FeatureKey', on_delete=models.RESTRICT)

    def __str__(self):
        return self.value


class FeatureKey(models.Model):
    key = models.CharField(max_length=255)
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.key

class Comment(models.Model):
    RATE_OPTIONS = (('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'))

    commenting_user = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    description = models.CharField(max_length=255,null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_rate = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], null=True, blank=True)

