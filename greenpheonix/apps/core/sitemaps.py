from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.studii_de_caz.models import StudiuDeCaz
from apps.blog.models import Articol


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return [
            "core:home", "core:despre", "contact:contact",
            "servicii:ads", "servicii:web", "servicii:audit",
            "studii_de_caz:list", "blog:list",
        ]

    def location(self, item):
        return reverse(item)


class StudiiDeCazSitemap(Sitemap):
    priority = 0.7
    changefreq = "monthly"

    def items(self):
        return StudiuDeCaz.objects.filter(activ=True)

    def lastmod(self, obj):
        return obj.creat_la


class BlogSitemap(Sitemap):
    priority = 0.6
    changefreq = "weekly"

    def items(self):
        return Articol.objects.filter(status="publicat")

    def lastmod(self, obj):
        return obj.actualizat_la


sitemaps = {
    "static": StaticViewSitemap,
    "studii": StudiiDeCazSitemap,
    "blog": BlogSitemap,
}
