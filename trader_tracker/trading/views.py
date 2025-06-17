from django.shortcuts import render, redirect
from .models import Trade
from .forms import TradeForm
from .my_funcs import readfile, mt5_auto_collect
from django.db.models import Sum, Avg
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/login')
def index(request):
    return render(request, 'trading/index.html')
# and when i check the value of form it retturns this 
# <TradeForm bound=True, valid=Unknown, fields=(file;notes)>
@login_required(login_url='/login')
def collect_trades(request):
   
    if request.method == "POST":
        form = TradeForm(request.POST, request.FILES)
        if form.is_valid():
            if request.post.get('mt5')== 'collected':
                trades = mt5_auto_collect()
            else:
                html_file = form.cleaned_data['file']
                content = html_file.read().decode('utf-8')
                trades = readfile(content)
                notes = form.cleaned_data['notes']
                
            for trade in trades:
                Trade.objects.create(
                    user = request.user,
                    date=trade["open_time"],
                    instrument=trade["symbol"],
                    direction=trade["type"],
                    entry_price=trade["entry_price"],
                    exit_price=trade["exit_price"],
                    lot_size=trade["lot_size"],
                    notes=notes,
                    profit_loss=trade["profit"]
                )

            return redirect('dash')
        else:
            return render(request, 'trading/add.html', {"form":form})
        
    else:
        form = TradeForm()
        return render(request, 'trading/add.html', {"form":form})
    
@login_required(login_url='/login')
def dashboard(request):
    trades = Trade.objects.filter(user=request.user).order_by('date')
    dates = [t.date.strftime('%Y-%m-%d') for t in trades]
    profits = [t.profit_loss for t in trades]

    context = {
        'trades': trades,
        'dates_json': json.dumps(dates, cls=DjangoJSONEncoder),
        'profits_json': json.dumps(profits, cls=DjangoJSONEncoder),
    }
    return render(request, 'trading/dashbaord.html', context)


