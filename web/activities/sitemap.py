from activities.models import Project, SiteVisit
from django.contrib.sitemaps import Sitemap


class ProjectSiteMap(Sitemap):
    changefreq = "weekly"

    def items(self):
        return Project.objects.all()
    
    def lastmod(self, obj):
        return obj.updated_at
    

class SiteVisitSiteMap(Sitemap):
    changefreq = "weekly"

    def items(self):
        return SiteVisit.objects.all()
    
    def lastmod(self, obj):
        return obj.updated_at