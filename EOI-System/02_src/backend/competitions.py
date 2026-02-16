from django.db import models
from django.utils.translation import gettext_lazy as _

from organizations.models import Club
from registry.models import Athlete, Horse  # αν είναι σε registry


class Competition(models.Model):
    title = models.CharField(max_length=200, verbose_name="Τίτλος Αγώνα")
    start_date = models.DateField(verbose_name="Ημερομηνία Έναρξης")
    end_date = models.DateField(verbose_name="Ημερομηνία Λήξης", blank=True, null=True)
    location = models.CharField(max_length=200, verbose_name="Τόπος")
    organizer = models.ForeignKey(Club, on_delete=models.PROTECT, verbose_name="Διοργανωτής")
    status = models.CharField(
        max_length=20,
        choices=[
            ('open', 'Ανοιχτός'),
            ('ongoing', 'Σε εξέλιξη'),
            ('completed', 'Ολοκληρωμένος'),
        ],
        default='open',
        verbose_name="Κατάσταση"
    )

    class Meta:
        verbose_name = "Αγώνας"
        verbose_name_plural = "Αγώνες"
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.title} ({self.start_date})"


class Category(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name="categories", verbose_name="Αγώνας")
    name = models.CharField(max_length=100, verbose_name="Όνομα Κατηγορίας")
    sport = models.CharField(max_length=50, verbose_name="Άθλημα")  # π.χ. Υπερπήδηση, Δεξιοτεχνία
    characteristics = models.CharField(max_length=200, blank=True, verbose_name="Χαρακτηριστικά (ύψος, γράμμα, χλμ κλπ.)")
    age_group = models.CharField(max_length=50, blank=True, verbose_name="Ηλικιακή Κατηγορία")
    regulation_article = models.CharField(max_length=100, blank=True, verbose_name="Άρθρο Κανονισμών")
    entry_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Παράβολο")

    class Meta:
        verbose_name = "Κατηγορία Αγώνα"
        verbose_name_plural = "Κατηγορίες Αγώνα"

    def __str__(self):
        return f"{self.name} - {self.competition}"


class Entry(models.Model):
    athlete = models.ForeignKey(Athlete, on_delete=models.PROTECT, verbose_name="Αθλητής")
    horse = models.ForeignKey(Horse, on_delete=models.PROTECT, verbose_name="Άλογο")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Κατηγορία")
    submission_date = models.DateTimeField(auto_now_add=True, verbose_name="Ημερομηνία Δήλωσης")
    status = models.CharField(
        max_length=20,
        choices=[
            ('draft', 'Πρόχειρη'),
            ('pending', 'Εκκρεμής'),
            ('approved', 'Εγκεκριμένη'),
            ('paid', 'Πληρωμένη'),
            ('final', 'Οριστική'),
            ('rejected', 'Απορρίφθηκε'),
        ],
        default='draft',
        verbose_name="Κατάσταση Δήλωσης"
    )

    class Meta:
        verbose_name = "Δήλωση Συμμετοχής"
        verbose_name_plural = "Δηλώσεις Συμμετοχής"

    def __str__(self):
        return f"{self.athlete} - {self.horse} - {self.category}"


class Result(models.Model):
    entry = models.OneToOneField(Entry, on_delete=models.CASCADE, verbose_name="Δήλωση")
    time_score = models.CharField(max_length=50, blank=True, verbose_name="Χρόνος / Βαθμολογία")
    ranking = models.PositiveIntegerField(blank=True, null=True, verbose_name="Κατάταξη")
    status = models.CharField(
        max_length=20,
        choices=[
            ('completed', 'Ολοκληρώθηκε'),
            ('retired', 'Retired'),
            ('eliminated', 'Eliminated'),
        ],
        verbose_name="Κατάσταση Αποτελέσματος"
    )
    notes = models.TextField(blank=True, verbose_name="Παρατηρήσεις")

    class Meta:
        verbose_name = "Αποτέλεσμα"
        verbose_name_plural = "Αποτελέσματα"

    def __str__(self):
        return f"Αποτέλεσμα για {self.entry}"
