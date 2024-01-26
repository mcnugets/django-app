from django.db import models


# Couple things to consider when coding: format, comments, conventional commit, pre-commit???


# Create your models here.

# Following models implementation:
# product, category, and tag


class Tag(models.Model):
    tag_name = models.CharField(max_length=50)
    def __str__(self):
        return self.tag_name


class Category(models.Model):
    cat_name = models.CharField(max_length=100)

    def __str__(self):
        return self.cat_name

# Product model with
class Product(models.Model):
    p_name = models.CharField(max_length=200)
    product_tag = models.ManyToManyField(Tag)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.p_name
