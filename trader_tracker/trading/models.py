from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Trade(models.Model):
    strategy = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    instrument = models.CharField(max_length=100,)
    direction = models.CharField(max_length=4, choices=[('BUY', 'Buy'), ('SELL', 'Sell')])
    entry_price = models.DecimalField(max_digits=10, decimal_places=2)
    exit_price = models.DecimalField(max_digits=10, decimal_places=2)
    lot_size = models.DecimalField(max_digits=10, decimal_places=2)
    profit_loss = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    followed_strategy = models.BooleanField(default=False)
    strategy_outcome = models.CharField(max_length=1, choices=[('W', 'Win'), ('L', 'Loss')], blank=True, null=True)

class  UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    starting_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    entry = models.TextField()
    emotion = models.CharField(max_length=100, blank=True, null=True)  # optional
    session = models.CharField(max_length=50, blank=True, null=True)   # e.g., NY, London
    chart_image = models.ImageField(upload_to='journal_images/', blank=True, null=True) 
    auto_feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"
# Create your models here.
