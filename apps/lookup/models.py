from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название категории")
    code = models.IntegerField(verbose_name="Код категории")
    parent_cat = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children",
                                   verbose_name="Родительская категория")

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название материала")
    code = models.IntegerField(verbose_name="Код материала")
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена материала")
    cat = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="marerials",
                            verbose_name="Категория материала")

    def __str__(self):
        return self.name
