from datetime import datetime

def validate_date(date_text):
    try:
        # Adjust the format to your requirement
        datetime.strptime(date_text, '%d-%m-%Y')  # Example: DD-MM-YYYY
        return True
    except ValueError:
        return False
# Function to format price in "RM XX.XX" format
def format_price(price):
    if price.startswith("RM "):
        try:
            float_value = float(price[3:])
            return f"RM {float_value:.2f}"
        except ValueError:
            pass
    try:
        float_value = float(price)
        return f"RM {float_value:.2f}"
    except ValueError:
        return "Invalid Price"

# Function to calculate profit or deficit
def calculate_profit_or_deficit(selling_price, quantity, cost):
    try:
        # Remove the "RM " prefix if present
        if selling_price.startswith("RM "):
            selling_price = selling_price[3:]
        if cost.startswith("RM "):
            cost = cost[3:]
        
        # Convert values to float for calculation
        selling_total = float(selling_price) * int(quantity)
        total_cost = float(cost) * int(quantity)
        profit_deficit = selling_total - total_cost
        return f"RM {profit_deficit:.2f}"
    except ValueError:
        return "Invalid Profit"
