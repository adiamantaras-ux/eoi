from __future__ import annotations

from datetime import timedelta

from django.db import models
from django.utils import timezone


class Athlete(models.Model):
    eoi_registry_number = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        unique=True,
        verbose_name="Αριθμός Μητρώου ΕΟΙ",
    )

    amka = models.CharField(max_length=20, blank=True, null=True, verbose_name="ΑΜΚΑ")

    first_name = models.CharField(max_length=120, blank=True, verbose_name="Όνομα")
    last_name = models.CharField(max_length=120, blank=True, verbose_name="Επώνυμο")
    father_name = models.CharField(max_length=120, blank=True, verbose_name="Όνομα Πατέρα")
    mother_name = models.CharField(max_length=120, blank=True, verbose_name="Όνομα Μητέρας")

    email = models.EmailField(blank=True, null=True, verbose_name="Email Αθλητή")
    athlete_license_date = models.DateField(blank=True, null=True, verbose_name="Ημερομηνία Άδειας Αθλητή")

    # Κανονικοποίηση για αναζήτηση (ΚΕΦΑΛΑΙΑ)
    first_name_uc = models.CharField(max_length=120, blank=True, editable=False, db_index=True)
    last_name_uc = models.CharField(max_length=120, blank=True, editable=False, db_index=True)
    father_name_uc = models.CharField(max_length=120, blank=True, editable=False, db_index=True)
    mother_name_uc = models.CharField(max_length=120, blank=True, editable=False, db_index=True)

    birth_date = models.DateField(blank=True, null=True, verbose_name="Ημερ/νία Γέννησης")
    birth_place = models.CharField(max_length=120, blank=True, verbose_name="Τόπος Γέννησης")
    nationality = models.CharField(max_length=120, blank=True, verbose_name="Υπηκοότητα")
    id_number = models.CharField(max_length=80, blank=True, verbose_name="ΑΔΤ / Διαβατήριο")

    club = models.ForeignKey(
        "organizations.Club",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="athletes",
        verbose_name="Όμιλος",
    )

    # ΠΡΟΣΩΡΙΝΑ: θα δεθεί με Συνδρομή μετά
    is_active = models.BooleanField(default=True, verbose_name="Ενεργός")

    created_at = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Δημιουργήθηκε")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ενημερώθηκε")

    class Meta:
        verbose_name = "Αθλητής"
        verbose_name_plural = "Αθλητές"
        ordering = ["last_name", "first_name", "eoi_registry_number"]

    def save(self, *args, **kwargs):
        self.first_name_uc = (self.first_name or "").upper()
        self.last_name_uc = (self.last_name or "").upper()
        self.father_name_uc = (self.father_name or "").upper()
        self.mother_name_uc = (self.mother_name or "").upper()
        super().save(*args, **kwargs)

    def __str__(self):
        parts = []
        if self.eoi_registry_number:
            parts.append(str(self.eoi_registry_number))
        name = f"{self.last_name} {self.first_name}".strip()
        if name:
            parts.append(name)
        return " - ".join(parts) if parts else f"Athlete #{self.pk}"


class Horse(models.Model):
    registry_number = models.CharField(max_length=30, unique=True, verbose_name="Αριθμός Μητρώου Ίππου (ΑΜ)")
    name = models.CharField(max_length=120, verbose_name="Ίππος")
    passport_number = models.CharField(max_length=80, blank=True, verbose_name="Διαβατήριο")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Ημερ/νια Γέννησης")
    is_active = models.BooleanField(default=True, verbose_name="Ενεργός")

    class Meta:
        verbose_name = "Ίππος"
        verbose_name_plural = "Ίπποι"
        ordering = ["registry_number"]

    def __str__(self):
        return f"{self.registry_number} - {self.name}"


class AthleteDocument(models.Model):
    class DocumentType(models.TextChoices):
        MEDICAL = "MEDICAL", "Ιατρική Βεβαίωση"
        REGISTRATION = "REGISTRATION", "Αίτηση Εγγραφής"
        TRANSFER = "TRANSFER", "Αίτηση Μεταγραφής"
        CERTIFICATE = "CERTIFICATE", "Πιστοποιητικό"
        OTHER = "OTHER", "Άλλο έγγραφο"

    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE, related_name="documents", verbose_name="Αθλητής")
    document_type = models.CharField(
        max_length=30,
        choices=DocumentType.choices,
        default=DocumentType.OTHER,
        verbose_name="Τύπος Εγγράφου",
    )
    title = models.CharField(max_length=200, blank=True, verbose_name="Τίτλος")
    file = models.FileField(upload_to="athlete_documents/%Y/%m/", verbose_name="Αρχείο")
    uploaded_at = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Καταχωρήθηκε")

    class Meta:
        verbose_name = "Έγγραφο Αθλητή"
        verbose_name_plural = "Έγγραφα Αθλητών"
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.athlete} - {self.get_document_type_display()}"


class AthleteMedicalCertificate(models.Model):
    athlete = models.ForeignKey(
        Athlete,
        on_delete=models.CASCADE,
        related_name="medical_certificates",
        verbose_name="Αθλητής",
    )
    issued_date = models.DateField(null=True, blank=True, verbose_name="Ημερ/νία Έκδοσης")
    valid_until = models.DateField(null=True, blank=True, verbose_name="Ισχύει μέχρι")
    file = models.FileField(upload_to="athlete_medicals/%Y/%m/", verbose_name="Αρχείο")
    uploaded_at = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Καταχωρήθηκε")

    class Meta:
        verbose_name = "Ιατρική Βεβαίωση Αθλητή"
        verbose_name_plural = "Ιατρικές Βεβαιώσεις Αθλητών"
        ordering = ["-uploaded_at"]

    @property
    def is_valid(self):
        if not self.valid_until:
            return False
        return self.valid_until >= timezone.localdate()

    @property
    def notify_on(self):
        if not self.valid_until:
            return None
        return self.valid_until - timedelta(days=20)

    def __str__(self):
        return f"{self.athlete} - Ιατρική ({self.valid_until or '-'})"


class HorseDocument(models.Model):
    class DocumentType(models.TextChoices):
        PASSPORT = "PASSPORT", "Διαβατήριο"
        MEDICAL = "MEDICAL", "Ιατρικό"
        CERTIFICATE = "CERTIFICATE", "Πιστοποιητικό"
        OTHER = "OTHER", "Λοιπό"

    horse = models.ForeignKey(Horse, on_delete=models.CASCADE, related_name="documents", verbose_name="Ίππος")
    document_type = models.CharField(
        max_length=30,
        choices=DocumentType.choices,
        default=DocumentType.OTHER,
        verbose_name="Τύπος Εγγράφου",
    )
    title = models.CharField(max_length=200, blank=True, verbose_name="Τίτλος")

    issued_date = models.DateField(null=True, blank=True, verbose_name="Ημερ/νία Έκδοσης")
    valid_until = models.DateField(null=True, blank=True, verbose_name="Ισχύει μέχρι")

    file = models.FileField(upload_to="horse_documents/%Y/%m/", verbose_name="Αρχείο")
    uploaded_at = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Καταχωρήθηκε")

    class Meta:
        verbose_name = "Έγγραφο Ίππου"
        verbose_name_plural = "Έγγραφα Ίππων"
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.horse} - {self.get_document_type_display()}"
