import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

# Define stages of financial independence with descriptions
STAGES = [
    ("Total Financial Dependence", "Relying entirely on others for financial support."),
    ("Financial Solvency", "Able to pay all bills on time but has no savings or investments."),
    ("Financial Stability", "Building an emergency fund and beginning to save and invest."),
    ("Debt Freedom", "Completely debt-free, including consumer and mortgage debts."),
    ("Financial Security", "Investment income covers basic living expenses."),
    ("Financial Independence", "Investment income covers current lifestyle expenses."),
    ("Financial Freedom", "Investment income allows for luxury spending and fulfilling big dreams."),
    ("Financial Abundance", "Investment income far exceeds spending needs; focus is on legacy and giving back.")
]

# Define conscious spending categories and percentages
CONSCIOUS_SPENDING_CATEGORIES = {
    "Needs": "Essentials like housing, utilities, and food.",
    "Wants": "Discretionary spending on things like dining out, entertainment, and vacations.",
    "Savings": "Money set aside for future goals and investments.",
    "Investing": "Money put into investments for growth.",
    "Guilt-Free Spending": "Extra spending that doesn’t affect financial goals."
}

SPENDING_PERCENTAGES = {
    "Needs": "50-60%",
    "Savings": "10%",
    "Investing": "10%",
    "Guilt-Free Spending": "20-35%"
}

# Define hero's journey phases
HERO_JOURNEY_PHASES = [
    "The Call to Adventure: Recognize the need for financial change.",
    "Crossing the Threshold: Commit to a budget and financial goals.",
    "Trials and Challenges: Face financial obstacles and setbacks.",
    "Meeting the Mentor: Seek advice and education on personal finance.",
    "Transformation: Implement changes and see progress in financial health.",
    "The Return: Enjoy the benefits of financial stability and independence.",
    "Master of Two Worlds: Balance between financial security and enjoyment of life."
]

# Define random financial events
RANDOM_EVENTS = [
    ("Unexpected Expense", "A sudden car repair costs you KES 10,000.", -10000),
    ("Bonus Received", "You received a bonus at work worth KES 50,000!", 50000),
    ("Investment Gain", "Your stock investment grew by KES 20,000.", 20000),
    ("Medical Bill", "A medical emergency costs KES 30,000.", -30000),
    ("Freelance Gig", "You earned KES 15,000 from a freelance project.", 15000)
]

# Define financial tips
FINANCIAL_TIPS = [
    "Automate your savings to ensure you always pay yourself first.",
    "Create a budget and track your expenses to avoid overspending.",
    "Invest in low-cost index funds for long-term growth.",
    "Keep an emergency fund with at least 3-6 months of living expenses.",
    "Pay off high-interest debt as soon as possible.",
    "Live below your means to build financial security faster."
]

def display_tip_notification():
    tip = random.choice(FINANCIAL_TIPS)
    show_auto_disappearing_message("Financial Tip", tip)
    root.after(900000, display_tip_notification)

def calculate_stage(income, expenses, savings, liabilities):
    net_worth = savings - liabilities
    critical_mass = expenses * 300
    
    if net_worth >= 150000000:  # Stage 7: Financial Abundance
        return STAGES[7]
    elif net_worth >= 30000000:  # Stage 6: Financial Freedom
        return STAGES[6]
    elif net_worth >= 15000000:  # Stage 5: Financial Independence
        return STAGES[5]
    elif net_worth >= 7500000:  # Stage 4: Financial Security
        return STAGES[4]
    elif liabilities == 0:  # Stage 3: Debt Freedom
        return STAGES[3]
    elif income >= 120000 and expenses <= income * 0.5:  # Stage 2: Financial Stability
        return STAGES[2]
    elif income >= 60000 and expenses <= income * 0.7:  # Stage 1: Financial Solvency
        return STAGES[1]
    else:  # Stage 0: Total Financial Dependence
        return STAGES[0]

def display_conscious_spending_plan():
    plan_text = "Conscious Spending Plan:\n\n"
    for category, description in CONSCIOUS_SPENDING_CATEGORIES.items():
        plan_text += f"{category}: {description} (Recommended: {SPENDING_PERCENTAGES.get(category, 'N/A')})\n"
    return plan_text

def display_hero_journey():
    journey_text = "Your Hero's Journey:\n\n"
    for phase in HERO_JOURNEY_PHASES:
        journey_text += f"{phase}\n"
    return journey_text

def plot_charts(income, expenses, savings, liabilities):
    fig = Figure(figsize=(12, 8), dpi=100)
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)

    # Pie chart for spending distribution
    categories = ['Income', 'Expenses', 'Savings', 'Liabilities']
    values = [income, expenses, savings, liabilities]
    ax1.pie(values, labels=categories, autopct='%1.1f%%', startangle=140, colors=['#4CAF50', '#FFC107', '#2196F3', '#F44336'])
    ax1.set_title('Financial Overview')
    
    # Bar chart for financial amounts
    ax2.bar(categories, values, color=['#4CAF50', '#FFC107', '#2196F3', '#F44336'])
    ax2.set_title('Financial Breakdown')
    ax2.set_ylabel('KES')
    
    # Plot the savings rate as the number of months it can cover expenses
    ax2.bar('Savings (Months)', savings / (expenses / 12), color='#FF5722')
    ax2.set_ylabel('Number of Months')
    
    return fig

def update_progress_bar(stage_index, critical_mass, net_worth):
    stage_progress['value'] = (stage_index + 1) * 12.5
    progress_label.config(text=f"Critical Mass: KES {critical_mass:,} - Progress: {stage_progress['value']:.1f}% - Net Worth: KES {net_worth:,}")

def trigger_random_event():
    event = random.choice(RANDOM_EVENTS)
    event_title = event[0]
    event_message = event[1]
    adjustment = event[2]
    
    try:
        current_savings = int(savings_entry.get())
        current_liabilities = int(liabilities_entry.get())

        # Compute new savings and liabilities based on the event
        new_savings = current_savings + adjustment
        new_liabilities = current_liabilities

        # If savings go negative, adjust liabilities
        if new_savings < 0:
            new_liabilities += abs(new_savings)
            new_savings = 0

        # Update the entry fields with new values
        savings_entry.delete(0, tk.END)
        savings_entry.insert(0, str(new_savings))
        liabilities_entry.delete(0, tk.END)
        liabilities_entry.insert(0, str(new_liabilities))

        # Show detailed impact
        impact_message = (
            f"Event: {event_title}\n"
            f"Impact: {event_message}\n\n"
            f"Adjustments:\nSavings: KES {current_savings} -> KES {new_savings}\n"
            f"Liabilities: KES {current_liabilities} -> KES {new_liabilities}"
        )
        show_auto_disappearing_message("Event Impact", impact_message)
        
        # Suggest actions based on the event
        if adjustment < 0:
            suggestion = "Consider revising your budget or finding ways to increase income."
        else:
            suggestion = "Good job managing the impact. Continue to monitor your finances."
        
        # Show suggestions
        show_auto_disappearing_message("Suggestions", suggestion)
        
    except ValueError:
        show_auto_disappearing_message("Input Error", "Please enter valid numeric values.")

def show_auto_disappearing_message(title, message, duration=5000):
    # Create a new window for the pop-up
    popup = tk.Toplevel()
    popup.title(title)
    tk.Label(popup, text=message, padx=20, pady=20).pack()
    
    # Ensure the pop-up is above other windows
    popup.attributes('-topmost', True)
    
    # Automatically close the pop-up after the specified duration
    popup.after(duration, popup.destroy)

def on_calculate_click():
    global canvas  # Declare 'canvas' as global
    try:
        income = int(income_entry.get())
        expenses = int(expenses_entry.get())
        savings = int(savings_entry.get())
        liabilities = int(liabilities_entry.get())
        
        # Calculate the financial stage
        stage = calculate_stage(income, expenses, savings, liabilities)
        stage_label.config(text=f"Financial Stage: {stage[0]}")
        stage_description_label.config(text=stage[1])
        
        # Update progress bar
        critical_mass = expenses * 300
        net_worth = savings - liabilities
        stage_index = STAGES.index(stage)
        update_progress_bar(stage_index, critical_mass, net_worth)
        
        # Plot charts
        fig = plot_charts(income, expenses, savings, liabilities)
        if 'canvas' in globals():
            canvas.get_tk_widget().destroy()
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    except ValueError:
        show_auto_disappearing_message("Input Error", "Please enter valid numeric values.")

# Create the main window
root = tk.Tk()
root.title("Financial Independence Tracker")

# Create tab control
tab_control = ttk.Notebook(root)
tab_control.pack(expand=1, fill="both")

# Create input tab
input_tab = ttk.Frame(tab_control)
tab_control.add(input_tab, text="Input")

# Create results tab
results_tab = ttk.Frame(tab_control)
tab_control.add(results_tab, text="Results")

# Create chart tab
chart_tab = ttk.Frame(tab_control)
tab_control.add(chart_tab, text="Charts")

# Input fields frame
input_frame = ttk.Frame(input_tab, padding=10)
input_frame.pack(expand=True, fill=tk.BOTH)

ttk.Label(input_frame, text="Income (KES):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
income_entry = ttk.Entry(input_frame)
income_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(input_frame, text="Expenses (KES):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
expenses_entry = ttk.Entry(input_frame)
expenses_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(input_frame, text="Savings (KES):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
savings_entry = ttk.Entry(input_frame)
savings_entry.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(input_frame, text="Liabilities (KES):").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
liabilities_entry = ttk.Entry(input_frame)
liabilities_entry.grid(row=3, column=1, padx=5, pady=5)

calculate_button = ttk.Button(input_frame, text="Calculate", command=on_calculate_click)
calculate_button.grid(row=4, column=0, columnspan=2, pady=10)

# Results frame
results_frame = ttk.Frame(results_tab, padding=10)
results_frame.pack(expand=True, fill=tk.BOTH)

stage_label = ttk.Label(results_frame, text="Financial Stage:", font=("Arial", 14))
stage_label.pack(pady=5)

stage_description_label = ttk.Label(results_frame, text="", wraplength=500)
stage_description_label.pack(pady=5)

# Chart frame
chart_frame = ttk.Frame(chart_tab, padding=10)
chart_frame.pack(expand=True, fill=tk.BOTH)

# Plot initial charts
fig = Figure(figsize=(12, 8), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=chart_frame)
canvas.draw()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Progress bar frame
progress_frame = ttk.Frame(results_tab, padding=10)
progress_frame.pack(expand=True, fill=tk.BOTH)

stage_progress = ttk.Progressbar(progress_frame, length=300, mode='determinate')
stage_progress.pack(pady=10)

progress_label = ttk.Label(progress_frame, text="", font=("Arial", 12))
progress_label.pack(pady=5)

# Initialize tip notifications
display_tip_notification()

# Run the application
root.mainloop()
