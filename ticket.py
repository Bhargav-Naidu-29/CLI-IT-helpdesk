import model, datetime


def generate_ticket_id(ticket_prefix, ticket_history):
    existing_numbers = [int(t.ticket_id.split('-')[-1]) for t in ticket_history if t.ticket_id.startswith(ticket_prefix + '-')]
    next_number = max(existing_numbers, default = 0) + 1
    return f"{ticket_prefix}-{next_number:04d}"


def raise_ticket(emp_id, params, ticket_history):
    while True:
        try:
            name = input('Please enter your name: ')
            if not name.strip():
                raise ValueError('Name cannot be empty.')
            break
        except ValueError as ve:
            print(f'{ve}. Please enter your name.')
    while True:
        try:
            description = input('Please enter a brief description of the issue: ')
            if not description.strip():
                raise ValueError('Description cannot be empty.')
            break
        except ValueError as ve:
            print(f'{ve}. Please mention a short description of the issue you are facing.')

    available_categories = params['categories']
    print("Please select a category from the following options: ")
    for i in range(len(available_categories)):
        print(f"Select {i + 1} for {available_categories[i]}")
    while True:
        try:
            category_choice = int(input('Enter the number corresponding to your category choice: '))
            if category_choice < 1 or category_choice > len(available_categories):
                raise ValueError('Invalid category selection.')
            category = available_categories[category_choice - 1]
            break
        except ValueError as ve:
            print(f'{ve}. Please select a valid category.')

    print("Please select a priority level from the following options: ")
    priority_levels = list(params['sla_hrs'].keys())
    for i, level in enumerate(priority_levels):
        print(f"Select {i + 1} to mark ticket as {level} priority")
    while True:
        try:
            priority_choice = int(input('Enter the number corresponding to your priority choice: '))
            if priority_choice < 1 or priority_choice > len(priority_levels):
                raise ValueError('Invalid priority selection.')
            priority = priority_levels[priority_choice - 1]
            break
        except ValueError as ve:
            print(f'{ve}. Please select a valid priority level.')

    status = model.STATUS_FLOW[0]
    created_at = datetime.datetime.now()
    ticket_id = generate_ticket_id(params['ticket_prefix'], ticket_history)
    sla_hrs = params['sla_hrs'][priority]
    new_ticket = model.Ticket(ticket_id, emp_id, name, description, category, priority, status, created_at, sla_hrs)
    print('Ticket raised successfully! Here are the details of your ticket:')
    ticket_history.append(new_ticket)
    print(new_ticket)


def update_ticket(emp_id, ticket_history):
    if len(ticket_history) == 0:
        print('No tickets raised yet.')
        return
    print('Your tickets:')
    for ticket in ticket_history:
        print(f'{ticket.ticket_id} - {ticket.status}')
    while True:
        ticket_id = input('Enter the Ticket ID to update (or press Enter to go back): ').strip().upper()
        if not ticket_id:
            print('Going back to the main menu...')
            return
        matching_tickets = [t for t in ticket_history if t.ticket_id == ticket_id]
        if matching_tickets:
            selected_ticket = matching_tickets[0]
            break
        print(f'No ticket found with ID {ticket_id}. Please enter a valid Ticket ID.')

    status_options = model.STATUS_FLOW
    current_index = status_options.index(selected_ticket.status)
    if current_index == len(status_options) - 1:
        print(f'Ticket {selected_ticket.ticket_id} is already Closed and cannot be updated.')
        return
    print(f'Current status of {selected_ticket.ticket_id}: {selected_ticket.status}')
    print(f'Allowed flow: {" -> ".join(status_options)}')
    for i in range(len(status_options)):
        print(f"Select {i + 1} to mark ticket as {status_options[i]}")
    while True:
        try:
            status_choice = int(input('Enter the number corresponding to your status choice: '))
            if status_choice < 1 or status_choice > len(status_options):
                raise ValueError('Invalid status selection.')
            new_status = status_options[status_choice - 1]
            if status_choice - 1 != current_index + 1:
                raise ValueError(f'Invalid status jump from {selected_ticket.status} to {new_status}')
            selected_ticket.status = new_status
            print(f'Ticket {selected_ticket.ticket_id} updated to {new_status}.')
            break
        except ValueError as ve:
            print(f'{ve}. Please move the ticket to the next step only.')
