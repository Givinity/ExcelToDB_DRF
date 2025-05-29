from django.core.cache import cache
from django.db import models
from django.db.models import Sum
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(max_length=255, verbose_name="Название категории")
    code = models.IntegerField(verbose_name="Код категории", unique=True)
    parent_cat = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children",
                                   verbose_name="Родительская категория")

    class MPTTMeta:
        order_insertion_by = ['name']
        parent_attr = 'parent_cat'

    def __str__(self):
        return self.name

    @property
    def total_cost(self):
        cache_key = f"category_total_cost_{self.id}"
        total = cache.get(cache_key)
        if total is None:
            descendants = self.get_descendants(include_self=True)
            result = Material.objects.filter(cat__in=descendants).distinct().aggregate(Sum('cost'))
            total = result['cost__sum'] or 0
            cache.set(cache_key, total, timeout=3600)
        return total


class Material(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название материала")
    code = models.IntegerField(verbose_name="Код материала", unique=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена материала")
    cat = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="materials",
                            verbose_name="Категория материала")

    def __str__(self):
        return self.name
