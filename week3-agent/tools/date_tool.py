from datetime import datetime
import re
from dateutil.relativedelta import relativedelta

def get_date(query: str = "") -> str:
    """
    Returns the current date/time, or calculates a future/past date 
    if the query asks for offsets like '90 days from now' or '90 days from today'.
    """
    try:
        now = datetime.now()
        query = query.lower().strip()
        
        # Check if we have an offset indicator first
        has_offset = any(unit in query for unit in ["day", "week", "month", "year"]) and re.search(r'\d+', query)
        
        # If it doesn't look like an offset, or explicitly asks for just current status
        if not has_offset or not query or query in ["today", "now", "current date"]:
            return now.strftime("%A, %B %d, %Y (Current Time: %I:%M %p)")

        # Simple regex to extract numbers (e.g., "90 days")
        number_match = re.search(r'(\d+)', query)
        if not number_match:
            return now.strftime("%A, %B %d, %Y")
            
        amount = int(number_match.group(1))
        
        # Determine direction (future vs past)
        if "old" in query or "ago" in query or "past" in query or "before" in query:
            amount = -amount

        # Calculate relative delta based on keywords
        if "day" in query:
            target_date = now + relativedelta(days=amount)
        elif "week" in query:
            target_date = now + relativedelta(weeks=amount)
        elif "month" in query:
            target_date = now + relativedelta(months=amount)
        elif "year" in query:
            target_date = now + relativedelta(years=amount)
        else:
            return now.strftime("%A, %B %d, %Y")

        return target_date.strftime("%A, %B %d, %Y")

    except Exception as e:
        return f"[OBSERVATION Error]: Could not calculate date. Details: {e}"

# Direct file testing
if __name__ == "__main__":
    print("Testing current date lookup:", get_date("What is today's date?"))
    print("Testing 90 days from now:", get_date("90 days from now"))
    print("Testing 2 weeks ago:", get_date("2 weeks ago"))
    print("Testing empty query fallback:", get_date(""))