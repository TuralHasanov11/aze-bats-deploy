from bats.models import Bat
from django.contrib.sitemaps import Sitemap


class BatSiteMap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Bat.objects.all()

    def lastmod(self, obj):
        return obj.updated_at
