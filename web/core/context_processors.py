import os

from base.models import SiteInfo
from django.utils.translation import gettext_lazy as _


def config(request):
    return {
        "config": {
            "app": {
                "name": os.environ.get("APP_NAME", ""),
                "site_url": os.environ.get("SITE_URL", "")
            },
        }
    }


def site_info(request):
    siteInfo = SiteInfo.objects.only("phone", "email", "logo_image", 
                                     "facebook_link", "instagram_link", "youtube_link").first()
    if siteInfo:
        return {
            "site_info": {
                "phone": siteInfo.phone,
                "email": siteInfo.email,
                "logo_image": siteInfo.logo_image,
                "social_links": [
                    {"link": siteInfo.facebook_link, "icon": "fa fa-facebook"},
                    {"link": siteInfo.instagram_link, "icon": "fa fa-instagram"},
                    {"link": siteInfo.youtube_link, "icon": "fa fa-youtube-play"},
                ]
            }
        }
    return {
        "site_info": {
            "phone": "",
            "email": "",
            "banner_image": "",
            "logo_image": "",
            "social_links": []
        }
    }


def footer_menu(request):
    return {
        "footer_menu": [
            {"title": _("Home"), "route": "base:index"},
            {"title": _("Bats"), "route": "bats:index"},
            {"title": _("Projects"), "route": "activities:project-list"},
            {"title": _("Site Visits"), "route": "activities:site-visit-list"},
            {"title": _("Articles"), "route": "base:articles"}
        ]
    }


def menu(request):
    return {
        "menu": {
            "home": {"route": "base:index", "text": _("Home")},
            "admin": [
                {"route": "administration:bat-list", "text": _("Bats")},
                {"route": "administration:project-list",
                    "text": _("Projects")},
                {"route": "administration:visit-list",
                    "text": _("Site Visits")},
                {"route": "administration:article-list-create",
                    "text": _("Articles")},
                {"route": "administration:author-list-create",
                    "text": _("Our Authors")},
                {"route": "administration:site-info",
                    "text": _("Site Info")},
                {"route": "administration:site-texts",
                    "text": _("Site Texts")},
            ],
            "activities": [
                {"route": "activities:project-list", "text": _("Projects")},
                {"route": "activities:site-visit-list", "text": _("Site Visits")},
            ],
            "bats": {"route": "bats:index", "text": _("Bats")},
            "gallery": {"route": "bats:gallery", "text": _("Gallery")},
            "articles": {"route": "base:articles", "text": _("Articles")},
        }
    }
