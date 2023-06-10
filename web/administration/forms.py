from activities.models import Project, ProjectImage, SiteVisit, SiteVisitImage
from base.models import Author, AuthorAttributes, SiteInfo, SiteText
from bats.models import (Genus, Species, SpeciesAttributes, SpeciesImage,
                         SpeciesRedBook)
from ckeditor_uploader import widgets as ckeditor_widgets
from django import forms
from django.conf import settings
from django.contrib.auth import forms as auth_forms
from django.utils.translation import gettext_lazy as _


class BatSpeciesForm(forms.ModelForm):
    is_red_book = forms.BooleanField(
        label=_("Is it a Red Book specie?"),
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )
    name = forms.CharField(
        label=_("Name"),
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Name"),
                "title": _("Please enter name"),
            }
        ),
    )
    genus = forms.ModelChoiceField(
        label=_("Genus"),
        initial=_("Select Genus"),
        widget=forms.Select(
            attrs={"class": "form-select", "title": _("Please enter genus")}
        ),
        queryset=Genus.objects.all(),
    )
    cover_image = forms.ImageField(
        label=_("Cover Image"),
        widget=forms.ClearableFileInput(
            attrs={"multiple": False, "class": "form-control"}
        ),
        required=True,
    )

    class Meta:
        model = Species
        fields = ("name", "genus", "cover_image", "is_red_book")


class SpeciesAttributesForm(forms.ModelForm):
    language = forms.ChoiceField(
        label=_("Language"),
        widget=forms.Select(
            attrs={"class": "form-select", "title": _("Please enter language")}
        ),
        choices=settings.LANGUAGES,
    )
    description = forms.CharField(
        label=_("Description"), widget=ckeditor_widgets.CKEditorUploadingWidget()
    )
    distribution = forms.CharField(
        label=_("Distribution"), widget=ckeditor_widgets.CKEditorUploadingWidget()
    )
    biology = forms.CharField(
        label=_("Biology"), widget=ckeditor_widgets.CKEditorUploadingWidget()
    )
    conservation = forms.CharField(
        label=_("Conservation"), widget=ckeditor_widgets.CKEditorUploadingWidget()
    )
    habitat = forms.CharField(
        label=_("Habitat"), widget=ckeditor_widgets.CKEditorUploadingWidget()
    )
    threats = forms.CharField(
        label=_("Threats"), widget=ckeditor_widgets.CKEditorUploadingWidget()
    )

    class Meta:
        model = SpeciesAttributes
        fields = (
            "description",
            "language",
            "distribution",
            "biology",
            "conservation",
            "habitat",
            "threats",
        )


class SpeciesRedBookForm(forms.ModelForm):
    language = forms.ChoiceField(
        label=_("Language"),
        widget=forms.Select(
            attrs={"class": "form-select", "title": _("Please enter language")}
        ),
        choices=settings.LANGUAGES,
    )
    description = forms.CharField(
        label=_("Description"),
        widget=ckeditor_widgets.CKEditorUploadingWidget(),
        required=False,
    )

    class Meta:
        model = SpeciesRedBook
        fields = ("description", "language")


class SpeciesImageForm(forms.ModelForm):
    image = forms.ImageField(
        label=_("Image"),
        widget=forms.ClearableFileInput(
            attrs={"multiple": False, "class": "form-control"}
        ),
        required=False,
    )

    class Meta:
        model = ProjectImage
        fields = ("image",)


SpeciesImageFormset = forms.inlineformset_factory(
    Species,
    SpeciesImage,
    form=SpeciesImageForm,
    extra=5,
    max_num=10,
    can_delete=True,
)
SpeciesAttributesFormset = forms.inlineformset_factory(
    Species,
    SpeciesAttributes,
    form=SpeciesAttributesForm,
    max_num=len(settings.LANGUAGES),
    can_delete=True,
)
SpeciesRedBookFormset = forms.inlineformset_factory(
    Species,
    SpeciesRedBook,
    form=SpeciesRedBookForm,
    max_num=len(settings.LANGUAGES),
    can_delete=True,
)


class AuthorForm(forms.ModelForm):
    cover_image = forms.ImageField(
        label=_("Cover Image"),
        widget=forms.ClearableFileInput(
            attrs={"multiple": False, "class": "form-control"}
        ),
        required=False,
    )

    class Meta:
        model = Author
        fields = "__all__"


class AuthorAttributesForm(forms.ModelForm):
    name = forms.CharField(
        label=_("Name"),
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Name"),
                "title": _("Please enter name"),
            }
        ),
    )
    language = forms.ChoiceField(
        label=_("Language"),
        widget=forms.Select(
            attrs={"class": "form-select", "title": _("Please enter language")},
        ),
        choices=settings.LANGUAGES,
    )
    description = forms.CharField(
        label=_("Description"), widget=ckeditor_widgets.CKEditorUploadingWidget()
    )

    class Meta:
        model = AuthorAttributes
        fields = ("description", "language", "name")


AuthorAttributesFormset = forms.inlineformset_factory(
    Author,
    AuthorAttributes,
    form=AuthorAttributesForm,
    max_num=len(settings.LANGUAGES),
    can_delete=True,
)


class ArticleForm(forms.ModelForm):
    name = forms.CharField(
        label=_("Name"),
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Name"),
                "title": _("Please enter name"),
            }
        ),
    )
    url = forms.URLField(
        label=_("Link"),
        widget=forms.URLInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Link"),
                "title": _("Please enter link"),
            }
        ),
    )
    author = forms.CharField(
        label=_("Author"),
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Author"),
                "title": _("Please enter author name"),
            }
        ),
    )

    class Meta:
        model = Author
        fields = "__all__"


class ProjectForm(forms.ModelForm):
    name = forms.CharField(
        label=_("Name"),
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Name"),
                "title": _("Please enter name"),
            }
        ),
    )
    cover_image = forms.ImageField(
        label=_("Cover Image"),
        widget=forms.ClearableFileInput(
            attrs={"multiple": False, "class": "form-control"}
        ),
        required=False,
    )
    language = forms.ChoiceField(
        label=_("Language"),
        widget=forms.Select(attrs={"class": "form-select"}),
        choices=settings.LANGUAGES,
    )
    description = forms.CharField(
        label=_("Description"), widget=ckeditor_widgets.CKEditorUploadingWidget()
    )

    class Meta:
        model = Project
        fields = ("name", "cover_image", "description", "language")


class ProjectImageForm(forms.ModelForm):
    image = forms.ImageField(
        label=_("Image"),
        widget=forms.ClearableFileInput(
            attrs={"multiple": False, "class": "form-control"}
        ),
        required=False,
    )

    class Meta:
        model = ProjectImage
        fields = ("image",)


ProjectImageFormset = forms.inlineformset_factory(
    Project,
    ProjectImage,
    form=ProjectImageForm,
    extra=5,
    max_num=10,
    can_delete=True,
)


class SiteVisitForm(forms.ModelForm):
    name = forms.CharField(
        label=_("Name"),
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": _("Name")}
        ),
    )
    cover_image = forms.ImageField(
        label=_("Cover Image"),
        widget=forms.ClearableFileInput(
            attrs={"multiple": False, "class": "form-control"}
        ),
        required=True,
    )
    language = forms.ChoiceField(
        label=_("Language"),
        widget=forms.Select(attrs={"class": "form-select"}),
        choices=settings.LANGUAGES,
    )
    description = forms.CharField(
        label=_("Description"), widget=ckeditor_widgets.CKEditorUploadingWidget()
    )
    results = forms.CharField(
        label=_("Results"), widget=ckeditor_widgets.CKEditorUploadingWidget()
    )

    class Meta:
        model = SiteVisit
        fields = ("name", "cover_image", "description", "language", "results")


class SiteVisitImageForm(forms.ModelForm):
    image = forms.ImageField(
        label=_("Image"),
        widget=forms.ClearableFileInput(
            attrs={"multiple": False, "class": "form-control"}
        ),
        required=False,
    )

    class Meta:
        model = SiteVisitImage
        fields = ("image",)


SiteVisitImageFormset = forms.inlineformset_factory(
    SiteVisit,
    SiteVisitImage,
    form=SiteVisitImageForm,
    extra=5,
    max_num=10,
    can_delete=True,
)


class UserLoginForm(auth_forms.AuthenticationForm):
    username = forms.CharField(
        label=_("Username"),
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Username"),
                "title": _("Please enter username"),
            }
        ),
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Password"),
                "title": _("Please enter password"),
            }
        ),
    )

    def confirm_login_allowed(self, user):
        pass


class SiteInfoForm(forms.ModelForm):
    phone = forms.CharField(
        label=_("Phone"),
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Phone"),
                "title": _("Please enter phone"),
            }
        ),
    )
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Email"),
                "title": _("Please enter email"),
            }
        ),
    )
    facebook_link = forms.URLField(
        label=_("Facebook link"),
        widget=forms.URLInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Facebook link"),
                "title": _("Please enter facebook link"),
            }
        ),
    )
    instagram_link = forms.URLField(
        label=_("Instagram link"),
        widget=forms.URLInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Instagram link"),
                "title": _("Please enter instagram link"),
            }
        ),
    )
    youtube_link = forms.URLField(
        label=_("YouTube link"),
        widget=forms.URLInput(
            attrs={
                "class": "form-control",
                "placeholder": _("YouTube link"),
                "title": _("Please enter youtube link"),
            }
        ),
    )
    banner_image = forms.ImageField(
        label=_("Banner Image"),
        widget=forms.ClearableFileInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Banner Image"),
                "title": _("Please upload banner image"),
                "multiple": False,
            }
        ),
        required=False,
    )
    logo_image = forms.ImageField(
        label=_("Logo Image"),
        widget=forms.ClearableFileInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Logo Image"),
                "title": _("Please upload logo image"),
                "multiple": False,
            }
        ),
        required=False,
    )

    class Meta:
        model = SiteInfo
        fields = [
            "phone",
            "email",
            "facebook_link",
            "instagram_link",
            "youtube_link",
            "banner_image",
            "logo_image",
        ]


class SiteTextForm(forms.ModelForm):
    language = forms.ChoiceField(
        label=_("Language"),
        widget=forms.Select(
            attrs={
                "class": "form-select form-select-sm",
                "readonly": True,
                "title": _("Please select language"),
            }
        ),
        choices=settings.LANGUAGES,
        disabled=True,
    )
    about = forms.CharField(
        label=_("About"),
        widget=forms.Textarea(
            attrs={
                "class": "form-control form-control-sm",
                "placeholder": _("About"),
                "rows": 25,
            }
        ),
        required=False,
    )
    banner = forms.CharField(
        label=_("Banner"),
        widget=forms.Textarea(
            attrs={
                "class": "form-control form-control-sm",
                "placeholder": _("Banner"),
                "rows": 25,
            }
        ),
        required=False,
    )
    privacy_policy = forms.CharField(
        label=_("Privacy Policy"),
        widget=ckeditor_widgets.CKEditorUploadingWidget(),
        required=False,
    )

    class Meta:
        model = SiteText
        fields = ["about", "language", "privacy_policy", "banner"]


SiteTextFormSet = forms.modelformset_factory(
    model=SiteText, form=SiteTextForm, max_num=len(settings.LANGUAGES)
)
