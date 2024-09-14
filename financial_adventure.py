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
    fig = Figure(figsize=(10, 8), dpi=100)
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
    
    # Automatically close the pop-up after the specified duration
    popup.after(duration, popup.destroy)

def submit_data():
    try:
        # Clear previous results and graphs
        for widget in charts_frame.winfo_children():
            widget.destroy()
        
        # Get data from input fields
        income = int(income_entry.get())
        expenses = int(expenses_entry.get())
        savings = int(savings_entry.get())
        liabilities = int(liabilities_entry.get())
        
        # Calculate financial stage and update progress bar
        net_worth = savings - liabilities
        critical_mass = expenses * 300
        stage_info = calculate_stage(income, expenses, savings, liabilities)
        stage_index = STAGES.index(stage_info)
        
        update_progress_bar(stage_index, critical_mass, net_worth)
        
        # Display conscious spending plan and hero's journey
        conscious_spending_plan_text = display_conscious_spending_plan()
        hero_journey_text = display_hero_journey()
        
        # Update the result text
        result_text.set(f"Financial Stage: {stage_info[0]}\n\nDescription: {stage_info[1]}")
        conscious_spending_plan_label.config(text=conscious_spending_plan_text)
        hero_journey_label.config(text=hero_journey_text)
        
        # Plot the charts
        fig = plot_charts(income, expenses, savings, liabilities)
        canvas = FigureCanvasTkAgg(fig, master=charts_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    except ValueError:
        show_auto_disappearing_message("Input Error", "Please enter valid numeric values.")

# Set up the main application window
root = tk.Tk()
root.title("Financial Adventure")

# Input frame
input_frame = tk.Frame(root, padx=10, pady=10)
input_frame.grid(row=0, column=0, sticky="nsew")

tk.Label(input_frame, text="Income:").grid(row=0, column=0, sticky="w")
income_entry = tk.Entry(input_frame)
income_entry.grid(row=0, column=1)

tk.Label(input_frame, text="Expenses:").grid(row=1, column=0, sticky="w")
expenses_entry = tk.Entry(input_frame)
expenses_entry.grid(row=1, column=1)

tk.Label(input_frame, text="Savings:").grid(row=2, column=0, sticky="w")
savings_entry = tk.Entry(input_frame)
savings_entry.grid(row=2, column=1)

tk.Label(input_frame, text="Liabilities:").grid(row=3, column=0, sticky="w")
liabilities_entry = tk.Entry(input_frame)
liabilities_entry.grid(row=3, column=1)

submit_button = tk.Button(input_frame, text="Submit", command=submit_data)
submit_button.grid(row=4, columnspan=2, pady=10)

random_event_button = tk.Button(input_frame, text="Trigger Random Event", command=trigger_random_event)
random_event_button.grid(row=5, columnspan=2, pady=10)

# Results frame
results_frame = tk.Frame(root, padx=10, pady=10)
results_frame.grid(row=1, column=0, sticky="nsew")

result_text = tk.StringVar()
result_label = tk.Label(results_frame, textvariable=result_text, wraplength=400)
result_label.pack()

conscious_spending_plan_label = tk.Label(results_frame, text="", wraplength=400)
conscious_spending_plan_label.pack()

hero_journey_label = tk.Label(results_frame, text="", wraplength=400)
hero_journey_label.pack()

# Charts frame
charts_frame = tk.Frame(root, padx=10, pady=10)
charts_frame.grid(row=0, column=1, rowspan=2, sticky="nsew")

# Progress bar
progress_frame = tk.Frame(root, padx=10, pady=10)
progress_frame.grid(row=2, column=0, columnspan=2, sticky="ew")

stage_progress = ttk.Progressbar(progress_frame, length=400, mode='determinate')
stage_progress.pack()

progress_label = tk.Label(progress_frame, text="Critical Mass Progress")
progress_label.pack()

# Adjust grid weights to make sure the layout expands correctly
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=2)

# Start periodic financial tip notifications
root.after(0, display_tip_notification)

# Start the application
root.mainloop()
