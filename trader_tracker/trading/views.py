from django.shortcuts import render, redirect
from .models import Trade, Tag, UserProfile, JournalEntry
from .forms import TradeForm, StartingBalanceForm, JournalEntryForm
from .my_funcs import readfile, mt5_auto_collect, generate_ai_feedback
from django.db.models import Sum, Avg
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.dateparse import parse_date
from django.db.models import Count, Sum, Q

# Create your views here.

@login_required(login_url='/login')
def collect_trades(request):
    if request.method == "POST":
        form = TradeForm(request.POST, request.FILES)
        if form.is_valid():
            tags = form.cleaned_data['tags']
            trades = []
            notes = form.cleaned_data.get('notes', '')

            # Check if MT5 auto collection is requested
            if request.POST.get('mt5') == 'collected':
                trades = mt5_auto_collect()
                if not trades:
                    form.add_error(None, "No trades collected from MT5.")
                    return render(request, 'trading/add.html', {"form": form})
            else:
                # Handle file upload and parse HTML content
                html_file = form.cleaned_data['file']
                try:
                    content = html_file.read().decode('utf-8')
                    trades = readfile(content)
                except Exception as e:
                    form.add_error('file', f"Error reading file: {e}")
                    return render(request, 'trading/add.html', {"form": form})

            # Save all trades
            for trade_data in trades:
                trade = Trade.objects.create(
                   user=request.user,
                    date=trade_data["open_time"],
                    instrument=trade_data["symbol"],
                    direction=trade_data["type"],
                    entry_price=trade_data["entry_price"],
                    exit_price=trade_data["exit_price"],
                    lot_size=trade_data["lot_size"],
                    notes=notes,
                    profit_loss=trade_data.get("profit") or trade_data.get("profit_loss", 0.0)
                )
                trade.tags.set(tags)  


            return redirect('dashboard')

        else:
            return render(request, 'trading/add.html', {"form": form})

    else:
        form = TradeForm()
        return render(request, 'trading/add.html', {"form": form})
    

@login_required(login_url='/login') 
def dashboard(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST" and "balance_submit" in request.POST:
        balance_form = StartingBalanceForm(request.POST, instance=profile)
        if balance_form.is_valid():
            balance_form.save()
            return redirect('dashboard')
    else:
        balance_form = StartingBalanceForm(instance=profile)

    trades = Trade.objects.filter(user=request.user).order_by('-date')
    tag_id = request.GET.get('tag')
    instrument = request.GET.get('instrument')
    direction = request.GET.get('direction')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    result = request.GET.get('result')

    if tag_id:
        trades = trades.filter(tags__id=tag_id)

    if instrument:
        trades = trades.filter(instrument__icontains=instrument)
    if direction:
        trades = trades.filter(direction=direction)
    if start_date:
        trades = trades.filter(date__gte=parse_date(start_date))
    if end_date:
        trades = trades.filter(date__lte=parse_date(end_date))
    if result == 'profit':
        trades = trades.filter(profit_loss__gt=0)
    elif result == 'loss':
        trades = trades.filter(profit_loss__lt=0)

    profile = request.user.userprofile
    starting_balance = profile.starting_balance
    running_total = starting_balance
    equity = []
    labels = []

    trades = Trade.objects.filter(user=request.user).order_by('date')

    for trade in trades:
        running_total += trade.profit_loss or 0
        equity.append(running_total)
        labels.append(trade.date.strftime('%Y-%m-%d'))

    total_pnl = trades.aggregate(Sum('profit_loss'))['profit_loss__sum'] or 0
    avg_pnl = trades.aggregate(Avg('profit_loss'))['profit_loss__avg'] or 0
    win_rate = round(100 * trades.filter(profit_loss__gt=0).count() / trades.count(), 2) if trades.exists() else 0
    # ✅ Filter first, then slice
    followed_qs = trades.filter(followed_strategy=True, strategy_outcome__in=['W', 'L']).order_by('-date')[:10]

    # Then count manually
    followed_wins = sum(1 for t in followed_qs if t.strategy_outcome == 'W')
    followed_losses = sum(1 for t in followed_qs if t.strategy_outcome == 'L')


    strategy_ratio = (
        round((followed_wins / (followed_wins + followed_losses)) * 100, 2)
        if (followed_wins + followed_losses) > 0 else 0
    )

    total_trades = trades.count()
    followed_count = trades.filter(followed_strategy=True).count()
    consistency_score = round((followed_count / total_trades) * 100, 2) if total_trades else 0
    remaining_ratio = 100 - strategy_ratio

    context = {
        'trades': trades,
        'equity': equity,
        'labels': labels,
        'avg_pnl': round(avg_pnl, 2),
        'total_pnl': round(total_pnl, 2),
        'win_rate': win_rate,
        'tags': Tag.objects.filter(user=request.user),
        'selected_tag': int(tag_id) if tag_id else None,
        'strategy_ratio': strategy_ratio,
        'consistency_score': consistency_score,
        'strategy_ratio': strategy_ratio,
        'remaining_ratio': remaining_ratio,
        'consistency_score': consistency_score
    }
    # Strategy Stats
    


    return render(request, 'trading/dashbaord.html', context)

# views.py
from django.db.models import Count, Sum, Q
from django.shortcuts import render
from .models import Trade

def strategy_stats(request):
    user_trades = Trade.objects.filter(user=request.user)

    strategies = user_trades.values('strategy').annotate(
        wins=Count('id', filter=Q(profit_loss__gt=0)),
        losses=Count('id', filter=Q(profit_loss__lt=0)),
        total_pnl=Sum('profit_loss'),
        total_trades=Count('id')
    )

    return render(request, 'trading/strategy_stats.html', {
        'strategies': strategies,
    })

@login_required
def journal(request):
    if request.method == 'POST':
        form = JournalEntryForm(request.POST, request.FILES)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.auto_feedback = generate_ai_feedback(entry.entry, entry.emotion, entry.session)
            entry.save()
            return redirect('journal')
    else:
        form = JournalEntryForm()

    entries = JournalEntry.objects.filter(user=request.user).order_by('-date')
    return render(request, 'trading/journal.html', {'form': form, 'entries': entries})
