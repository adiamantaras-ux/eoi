from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=120, unique=True, verbose_name="Περιφέρεια")
    is_active = models.BooleanField(default=True, verbose_name="Ενεργή")

    class Meta:
        verbose_name = "Περιφέρεια"
        verbose_name_plural = "Περιφέρειες"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Club(models.Model):
    code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Κωδικός Ομίλου",
        help_text="Π.χ. ΙΟΠ",
    )
    name = models.CharField(max_length=200, verbose_name="Όνομα Ομίλου")
    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        related_name="clubs",
        verbose_name="Περιφέρεια",
    )

    phone = models.CharField(max_length=30, blank=True, verbose_name="Τηλέφωνο")
    email = models.EmailField(blank=True, verbose_name="Email")
    address = models.CharField(max_length=255, blank=True, verbose_name="Διεύθυνση")

    is_active = models.BooleanField(default=True, verbose_name="Ενεργός Όμιλος")

    class Meta:
        verbose_name = "Όμιλος"
        verbose_name_plural = "Όμιλοι"
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.name}"
