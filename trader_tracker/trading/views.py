from django.shortcuts import render
from .models import Trade
from .forms import TradeForm
from .my_funcs import readfile
from django.db.models import Sum, Avg
import json
from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.
def index(request):
    return render(request, 'trading/index.html')

# i found out that the code below the breakpoint is not runnning
# and when i check the value of form it retturns this 
# <TradeForm bound=True, valid=Unknown, fields=(file;notes)>
    
def collect_trades(request):
   
    if request.method == "POST":
        form = TradeForm(request.POST, request.FILES)
        if form.is_valid():
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

            return render(request, 'trading/add.html', {"form":form})
        else:
            return render(request, 'trading/add.html', {"form":form})
        
    else:
        form = TradeForm()
        return render(request, 'trading/add.html', {"form":form})
    

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
