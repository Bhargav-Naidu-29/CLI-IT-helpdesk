# IT Service Desk Ticketing System

A command line helpdesk application where an agent can raise, track, update and resolve IT support tickets. Every ticket is checked against an SLA (Service Level Agreement) deadline, so late tickets are flagged automatically. All tickets are saved to a file, so your data is still there when you close and reopen the program.

## Requirements

- Python 3.7 or higher
- No external libraries. Only the standard library is used (`datetime`, `json`, `os`, `random`, `hashlib`).

## How to Run

1. Put all the files below in the same folder.
2. Open a terminal in that folder.
3. Start the program:

```
python main.py
```

On some systems, use `python3 main.py` instead.

4. Enter your Employee ID when asked. Use only letters, numbers, `-` or `_`.
5. Choose a service from the main menu by typing its number.

## Project Structure

| File | What it does |
|---|---|
| `main.py` | Entry point. Asks for the Employee ID, loads saved tickets, shows the main menu and saves after changes. |
| `model.py` | The `Ticket` class, the status flow, and the functions that load and save tickets to JSON. |
| `ticket.py` | Raising a new ticket and updating a ticket's status. |
| `summary.py` | Viewing tickets, filtering them, and showing counts and SLA breached tickets. |
| `personalization.py` | Creates your personal settings (categories, SLA hours, ID prefix) from your Employee ID. |

## Personalized Settings

Your settings are worked out from your Employee ID. Think of the ID as a lock combination: the same ID always opens the same settings, and a different ID gives different ones.

Each Employee ID gets:

- **5 categories** picked from: Software, Hardware, Network, Access Request, Email, Printer, VPN, Application Bug, Account Lockout, Data Backup
- **SLA hours for each priority**, within these ranges:

| Priority | SLA hours range |
|---|---|
| Critical | 2 to 4 |
| High | 6 to 12 |
| Medium | 24 to 48 |
| Low | 72 to 120 |

- **A ticket ID prefix**, one of `TCK`, `REQ`, `SR`, `INC`

These are shown to you right after you enter your ID. Note that the Employee ID is case-sensitive, so `emp01` and `EMP01` are treated as two different employees.

## Main Menu

| Option | Service |
|---|---|
| 1 | Raise a ticket |
| 2 | Update a ticket status |
| 3 | Check your ticket summary |
| 4 | Exit the application |

### 1. Raise a Ticket

You are asked for:

1. Your name
2. A short description of the issue
3. A category, chosen by number from your 5 assigned categories
4. A priority, chosen by number (Critical, High, Medium, Low)

The program fills in the rest automatically:

- **Ticket ID**: your prefix plus a running number, for example `INC-0001`
- **Status**: starts as `Open`
- **Created time**: the current date and time
- **SLA hours**: taken from the priority you chose

Empty names, empty descriptions and invalid menu choices show an error message and ask again. The program does not crash.

### 2. Update a Ticket Status

Enter the Ticket ID you want to update (or press Enter to go back). A ticket moves through this flow, one step at a time:

```
Open -> In Progress -> Resolved -> Closed
```

- Skipping a step (for example `Open` straight to `Closed`) is rejected with an error message.
- Going backwards is also rejected.
- A `Closed` ticket cannot be updated any more.

### 3. Ticket Summary

This opens a sub-menu:

| Option | What it shows |
|---|---|
| 1 | All your tickets |
| 2 | Tickets filtered by priority |
| 3 | Tickets filtered by category |
| 4 | Tickets filtered by status |
| 5 | Ticket counts by status, counts by category, and the list of SLA breached tickets |
| 6 | Back to the main menu |

## SLA Breach Detection

Every ticket has a deadline:

```
deadline = created time + SLA hours for its priority
```

A ticket is marked **BREACHED** when its deadline has passed and it is still `Open` or `In Progress`. Tickets that are `Resolved` or `Closed` are no longer counted as breached.

You can see this in three places:

- A warning at startup if any saved ticket has already breached its SLA
- The `SLA State` line when a ticket is displayed
- The breached ticket list in the summary (option 3, then 5)

## Data Storage (JSON)

Tickets are stored in **JSON**, one file for each Employee ID:

```
tickets_<employee_id>.json
```

For example, Employee ID `EMP01` uses `tickets_EMP01.json`. The file is created in the folder where you run the program.

- The file is **loaded** when the program starts.
- The file is **saved** right after you raise a ticket or update a status.
- Dates are stored as text (ISO format) and converted back when loading.
- If the file is missing, the program starts with no tickets.
- If the file cannot be read, a message is shown and the program starts with an empty list.

JSON was chosen because it keeps each ticket's fields together in a clear, readable way and is easy to save and load with Python's built-in `json` module.

Example of a saved ticket:

```json
[
    {
        "ticket_id": "INC-0001",
        "emp_id": "EMP01",
        "name": "Asha",
        "description": "VPN keeps disconnecting",
        "category": "VPN",
        "priority": "High",
        "status": "Open",
        "created_at": "2026-10-10T10:30:00.123456",
        "sla_hrs": 8
    }
]
```

## The Ticket Class

Each ticket is an object of the `Ticket` class in `model.py`.

| Attribute | Meaning |
|---|---|
| `ticket_id` | Auto-generated ID, for example `INC-0001` |
| `emp_id` | Employee ID of the person who raised it |
| `name` | Requester name |
| `description` | Short description of the issue |
| `category` | One of the employee's assigned categories |
| `priority` | Critical, High, Medium or Low |
| `status` | Open, In Progress, Resolved or Closed |
| `created_at` | Date and time the ticket was raised |
| `sla_hrs` | Hours allowed to resolve the ticket |

Main methods: `get_sla_deadline()`, `is_breached()`, `to_dict()`, `from_dict()` and `__str__()`, which prints the full ticket details.

## Sample Session

```
Welcome to the IT Service Desk Ticketing System!!!
Please enter your Employee ID: EMP01
Your parameters are as follows:
categories: ['VPN', 'Email', 'Hardware', 'Network', 'Software']
sla_hrs: {'Critical': 3, 'High': 8, 'Medium': 30, 'Low': 90}
ticket_prefix: INC
Loaded 0 saved ticket(s).
--------------------
available services
Select 1 to raise a ticket
Select 2 to update a ticket status
Select 3 to check your ticket summary
Select 4 to exit the application
Please select a service: 1
```

The categories and SLA hours above are only an example. Your own values depend on your Employee ID.

## Error Handling

The program shows a clear message and asks again, instead of crashing, when:

- The Employee ID is empty or has invalid characters
- The name or description is empty
- A menu choice is not a valid number or is out of range
- A Ticket ID does not exist
- A status change skips a step or goes backwards
- The saved file cannot be read or written

Pressing `Ctrl+C` or closing the input also exits the program cleanly.
