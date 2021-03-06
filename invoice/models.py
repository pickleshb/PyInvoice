from __future__ import unicode_literals

from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class Profile(AbstractUser):
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    utr = models.BigIntegerField(blank=True, null=True)

    bank = models.CharField(max_length=180, blank=True, null=True)
    sort_code = models.CharField(max_length=50, blank=True, null=True)
    account_number = models.IntegerField(blank=True, null=True)

    invoice_primary_color = models.CharField(max_length=10, blank=True, null=True, help_text='Colour in hex')
    invoice_secondary_color = models.CharField(max_length=10, blank=True, null=True, help_text='Colour in hex')
    invoice_accent_color = models.CharField(max_length=10, blank=True, null=True, help_text='Colour in hex')
    invoice_background_color = models.CharField(max_length=10, blank=True, null=True, help_text='Colour in hex')

    invoice_logo = models.ImageField(upload_to='invoice_logos', blank=True, null=True)


class Company(models.Model):
    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    name = models.CharField(max_length=200, unique=True)
    address = models.TextField()
    email = models.CharField(max_length=150)
    person = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    require_utr = models.BooleanField(default=False)

    def company_invoice_total(self):
        return Sum(self.invoice_set.all)

    def __str__(self):
        return self.name


class Invoice(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(blank=True, auto_now_add=True)
    updated = models.DateTimeField(blank=True, auto_now=True)
    paid = models.BooleanField(default=False)
    paid_date = models.DateTimeField(blank=True, null=True)
    utr = models.BooleanField(default=False)
    po_number = models.CharField(max_length=30, blank=True, null=True)
    is_quote = models.BooleanField(default=False)
    sent_date = models.DateTimeField(blank=True, null=True)
    user_invoice_number = models.CharField(max_length=15, blank=True, null=True)

    def invoice_number(self):
        if not self.user_invoice_number:
            return 'N%04d' % self.pk
        else:
            return self.user_invoice_number

    def get_items(self):
        return self.items.all()

    def total(self):
        return self.items.all().aggregate(total=models.Sum('total'))['total']

    def date_delta(self):
        return timezone.now() - self.created

    def sent_date_delta(self):
        if self.sent_date:
            return (timezone.now() - self.sent_date).days
        else:
            return None

    def expenses_total(self):
        return self.expenses.all().aggregate(total=models.Sum('cost'))['total']

    def num_expenses(self):
        return self.expenses.all().count()

    def __str__(self):
        company = self.company.name if self.company else 'None'
        return self.invoice_number() + ' - ' + company

    def save(self, *args, **kwargs):
        self.updated = timezone.now()

        if self.paid and not self.paid_date:
            self.paid_date = timezone.now()
        elif self.paid_date and not self.paid:
            self.paid_date = None

        super(Invoice, self).save(*args, **kwargs)


class InvoiceItem(models.Model):
    class Meta:
        ordering = ['id']

    invoice = models.ForeignKey(Invoice, related_name='items')
    description = models.CharField(max_length=200)
    quantity = models.DecimalField(max_digits=5, decimal_places=1)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

    def save(self, *args, **kwargs):
        self.total = float(self.quantity) * float(self.cost)

        super(InvoiceItem, self).save(*args, **kwargs)


class ExpenseGroup(models.Model):
    class Meta:
        verbose_name = 'Expense Group'
        verbose_name_plural = 'Expense Groups'

    name = models.CharField(max_length=80)

    def expenses_total(self):
        return self.expense_group.all().aggregate(total=models.Sum('cost'))['total']

    def num_invoices(self):
        return self.expense_group.all().aggregate(count=models.Count('invoice'))['count']

    def __str__(self):
        return self.name


class Expense(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='expenses', blank=True, null=True)
    group = models.ForeignKey(ExpenseGroup, related_name='expense_group', blank=True, null=True)
    description = models.CharField(max_length=200)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(blank=True, auto_now_add=True)

    def __str__(self):
        return self.description + ' for ' + self.invoice.__str__()
