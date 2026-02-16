from datetime import timedelta

from django.contrib import admin
from django.db.models import Q
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth import get_user_model

from .models import (
    Athlete,
    Horse,
    AthleteDocument,
    AthleteMedicalCertificate,
    HorseDocument,
)

User = get_user_model()


# -----------------------------
# Generic actions (activate / deactivate)
# -----------------------------
@admin.action(description="✅ Ενεργοποίηση")
def make_active(modeladmin, request, queryset):
    if hasattr(modeladmin.model, "is_active"):
        queryset.update(is_active=True)


@admin.action(description="⛔ Απενεργοποίηση")
def make_inactive(modeladmin, request, queryset):
    if hasattr(modeladmin.model, "is_active"):
        queryset.update(is_active=False)


# -----------------------------
# Users (login_code)
# (ΠΡΟΣΟΧΗ: Αν έχεις ήδη UserAdmin στο accounts/admin.py, ΜΗΝ το δηλώσεις κι εδώ)
# -----------------------------
# Αν εμφανιστεί ξανά AlreadyRegistered για User, τότε:
# - ΚΡΑΤΑΣ ΜΟΝΟ ΤΟ accounts/admin.py
# - και ΣΒΗΝΕΙΣ τελείως αυτό το UserAdmin από εδώ.

# @admin.register(User)
# class UserAdmin(DjangoUserAdmin):
#     model = User
#     ordering = ("login_code",)
#     list_display = ("login_code", "username", "email", "is_active", "is_staff", "is_superuser")
#     search_fields = ("login_code", "username", "email")
#     fieldsets = DjangoUserAdmin.fieldsets + (("EOI", {"fields": ("login_code",)}),)
#     add_fieldsets = DjangoUserAdmin.add_fieldsets + (("EOI", {"fields": ("login_code",)}),)


# -----------------------------
# Inlines
# -----------------------------
class AthleteMedicalInline(admin.TabularInline):
    model = AthleteMedicalCertificate
    extra = 0
    fields = ("issued_date", "valid_until", "uploaded_at", "file")
    readonly_fields = ("uploaded_at",)
    ordering = ("-uploaded_at",)


class AthleteDocumentInline(admin.TabularInline):
    model = AthleteDocument
    extra = 0
    fields = ("document_type", "title", "uploaded_at", "file")
    readonly_fields = ("uploaded_at",)
    ordering = ("-uploaded_at",)


class HorseDocumentInline(admin.TabularInline):
    model = HorseDocument
    extra = 0
    fields = ("document_type", "title", "issued_date", "valid_until", "uploaded_at", "file")
    readonly_fields = ("uploaded_at",)
    ordering = ("-uploaded_at",)


# -----------------------------
# Athletes
# -----------------------------
@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    list_display = (
        "eoi_registry_number",
        "last_name",
        "first_name",
        "club",
        "birth_date",
        "athlete_license_date",
        "is_active",
        "latest_medical_valid_until",
        "latest_medical_uploaded_at",
    )
    list_filter = ("is_active", "club")
    ordering = ("last_name", "first_name", "eoi_registry_number")
    actions = (make_active, make_inactive)

    # ✅ Για autocomplete να δουλεύει σωστά, πρέπει να υπάρχουν search_fields
    search_fields = (
        "eoi_registry_number",
        "amka",
        "last_name_uc",
        "first_name_uc",
        "father_name_uc",
        "mother_name_uc",
        "club__name",
        "club__code",
    )

    autocomplete_fields = ("club",)

    readonly_fields = (
        "created_at",
        "updated_at",
        "latest_medical_issued_date",
        "latest_medical_valid_until",
        "latest_medical_uploaded_at",
    )

    fieldsets = (
        ("Στοιχεία Αθλητή", {
            "fields": (
                "eoi_registry_number",
                "amka",
                "first_name",
                "last_name",
                "father_name",
                "mother_name",
                "email",
                "birth_date",
                "birth_place",
                "nationality",
                "id_number",
                "club",
                "athlete_license_date",
                "is_active",
            )
        }),
        ("Ιατρική Βεβαίωση (τελευταία)", {
            "fields": (
                "latest_medical_issued_date",
                "latest_medical_valid_until",
                "latest_medical_uploaded_at",
            )
        }),
        ("Σύστημα", {"fields": ("created_at", "updated_at")}),
    )

    inlines = (AthleteMedicalInline, AthleteDocumentInline)

    def _latest_medical(self, obj):
        return obj.medical_certificates.order_by("-uploaded_at").first()

    @admin.display(description="Ιατρικό: Έκδοση")
    def latest_medical_issued_date(self, obj):
        m = self._latest_medical(obj)
        return m.issued_date if m else "-"

    @admin.display(description="Ιατρικό: Λήξη")
    def latest_medical_valid_until(self, obj):
        m = self._latest_medical(obj)
        return m.valid_until if m else "-"

    @admin.display(description="Ιατρικό: Καταχώρηση")
    def latest_medical_uploaded_at(self, obj):
        m = self._latest_medical(obj)
        return m.uploaded_at if m else "-"

    # ✅ Κάνει την αναζήτηση να δουλεύει σωστά με ελληνικά (γράφεις μικρά/κεφαλαία)
    def get_search_results(self, request, queryset, search_term):
        term = (search_term or "").strip()
        if not term:
            return super().get_search_results(request, queryset, search_term)

        term_uc = term.upper()
        qs = queryset.filter(
            Q(eoi_registry_number__icontains=term)
            | Q(amka__icontains=term)
            | Q(last_name_uc__contains=term_uc)
            | Q(first_name_uc__contains=term_uc)
            | Q(father_name_uc__contains=term_uc)
            | Q(mother_name_uc__contains=term_uc)
        )
        return qs, False


# -----------------------------
# Medical Certificates
# -----------------------------
@admin.register(AthleteMedicalCertificate)
class AthleteMedicalCertificateAdmin(admin.ModelAdmin):
    list_display = ("athlete", "issued_date", "valid_until", "uploaded_at", "is_valid", "notify_on")
    list_filter = ("valid_until",)
    readonly_fields = ("uploaded_at",)
    ordering = ("-uploaded_at",)

    # ✅ για autocomplete
    autocomplete_fields = ("athlete",)
    search_fields = ("athlete__eoi_registry_number", "athlete__last_name_uc", "athlete__first_name_uc")


# -----------------------------
# Athlete Documents
# -----------------------------
@admin.register(AthleteDocument)
class AthleteDocumentAdmin(admin.ModelAdmin):
    list_display = ("athlete", "document_type", "title", "uploaded_at")
    readonly_fields = ("uploaded_at",)
    ordering = ("-uploaded_at",)

    # ✅ για autocomplete
    autocomplete_fields = ("athlete",)
    search_fields = ("athlete__eoi_registry_number", "athlete__last_name_uc", "athlete__first_name_uc", "title")


# -----------------------------
# Horses
# -----------------------------
@admin.register(Horse)
class HorseAdmin(admin.ModelAdmin):
    list_display = ("registry_number", "name", "passport_number", "birth_date", "is_active")
    list_filter = ("is_active",)
    search_fields = ("registry_number", "name", "passport_number")
    ordering = ("registry_number",)
    actions = (make_active, make_inactive)

    inlines = (HorseDocumentInline,)


# -----------------------------
# Horse Documents
# -----------------------------
@admin.register(HorseDocument)
class HorseDocumentAdmin(admin.ModelAdmin):
    list_display = ("horse", "document_type", "title", "issued_date", "valid_until", "uploaded_at")
    readonly_fields = ("uploaded_at",)
    ordering = ("-uploaded_at",)

    # ✅ για autocomplete
    autocomplete_fields = ("horse",)
    search_fields = ("horse__registry_number", "horse__name", "title")
