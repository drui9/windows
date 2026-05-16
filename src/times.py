import calendar

def print_calendar(year, month):
  cal = calendar.month(year, month)
  print(cal)

# Example usage
year = int(input("Enter year (e.g., 2026): "))
month = int(input("Enter month (1-12): "))

print_calendar(year, month)
