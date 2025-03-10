import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.db.models import Sum
import matplotlib.dates as mdates
from .models import *

# Set matplotlib to work without a display
matplotlib.use('Agg')

def set_chart_style():
    # Use a default style
    plt.style.use('ggplot')  # You can also use 'fivethirtyeight', 'classic', or others.
    plt.rcParams['font.size'] = 14
    plt.rcParams['axes.labelsize'] = 16
    plt.rcParams['xtick.labelsize'] = 14
    plt.rcParams['ytick.labelsize'] = 14
    plt.rcParams['figure.figsize'] = (12, 8)

def generate_expense_chart(user):
    set_chart_style()
    expenses = Expense.objects.filter(user=user).values('category').annotate(total=Sum('amount'))
    categories = [expense['category'] for expense in expenses]
    totals = [expense['total'] for expense in expenses]

    if not categories:
        categories = ['No Data']
        totals = [1]

    # New color palette for Pie chart
    colors = ['#ffcc99', '#66b3ff', '#ff6666', '#c2c2f0', '#ffb3e6', '#ffb366']

    fig, ax = plt.subplots(figsize=(12, 8))  # 2D pie chart
    ax.pie(totals, labels=categories, autopct='%1.1f%%', startangle=90, colors=colors, shadow=True, wedgeprops={'edgecolor': 'black', 'linewidth': 2})

    ax.set_title('Expense Detail', fontsize=18, weight='bold')

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', dpi=150)
    buffer.seek(0)
    chart = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    plt.close()
    return chart

def generate_monthly_comparison_chart(user):
    set_chart_style()
    from django.db.models.functions import TruncMonth

    incomes = Income.objects.filter(user=user).annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('amount')).order_by('month')
    expenses = Expense.objects.filter(user=user).annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('amount')).order_by('month')

    months = [income['month'].strftime('%B %Y') for income in incomes]
    income_totals = [income['total'] for income in incomes]
    expense_totals = [expense['total'] for expense in expenses]

    if not months:
        months = ['No Data']
        income_totals = [0]
        expense_totals = [0]

    fig, ax = plt.subplots(figsize=(12, 8))  # Adjust the figure size
    x = range(len(months))
    ax.bar(x, income_totals, width=0.4, label='Income', color='#4CAF50', edgecolor='black', zorder=2, alpha=0.9)
    ax.bar([p + 0.4 for p in x], expense_totals, width=0.4, label='Expense', color='#FF5733', edgecolor='black', zorder=2, alpha=0.9)

    ax.set_xticks([p + 0.2 for p in x])
    ax.set_xticklabels(months, rotation=45, ha='right', fontsize=14)
    ax.set_ylabel('Amount (₹)', fontsize=16)
    ax.set_title('Monthly Income vs Expenses', fontsize=18, weight='bold')
    ax.legend()

    ax.grid(True, linestyle='--', alpha=0.7)

    plt.tight_layout()  # Adjust layout to avoid clipping
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=200)
    buffer.seek(0)
    chart = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    plt.close()
    return chart

def generate_daily_spending_chart(user):
    set_chart_style()
    expenses = Expense.objects.filter(user=user).values('date').annotate(total=Sum('amount')).order_by('date')
    dates = [expense['date'] for expense in expenses]
    totals = [expense['total'] for expense in expenses]

    if not dates:
        dates = ['No Data']
        totals = [0]

    fig, ax = plt.subplots(figsize=(12, 8))  # Adjust the figure size

    # Bar chart with a gradient color
    bar_color = '#FF5733'  # Bright Red for Expenses
    ax.bar(dates, totals, color=bar_color, edgecolor='black', zorder=2, alpha=0.8)

    ax.set_xlabel('Date', fontsize=16, weight='bold')
    ax.set_ylabel('Amount (₹)', fontsize=16, weight='bold')
    ax.set_title('Daily Spending Trend', fontsize=18, weight='bold')
    
    ax.grid(True, linestyle='--', alpha=0.7)

    # Rotate the dates for better visibility and avoid overlap
    plt.xticks(rotation=45, ha='right', fontsize=14)
    ax.set_xticklabels(dates, rotation=45, ha='right', fontsize=14)

    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=200)
    buffer.seek(0)
    chart = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    plt.close()
    return chart

