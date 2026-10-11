import model


def ticket_by_priority(emp_id: str, ticket_history: list, priority_options: list):
    print("Displaying tickets raised by you based on priority:")
    for i in range(len(priority_options)):
        print(f"Select {i + 1} to view tickets with {priority_options[i]} priority")
    while True:
        try:
            priority_choice = int(input('Enter the number corresponding to your priority choice: '))
            if priority_choice < 1 or priority_choice > len(priority_options):
                raise ValueError('Invalid priority selection.')
            selected_priority = priority_options[priority_choice - 1]
            print(f'Displaying tickets with {selected_priority} priority:')
            filtered_tickets = [ticket for ticket in ticket_history if ticket.priority == selected_priority]
            if not filtered_tickets:
                print(f'No tickets found with {selected_priority} priority.')
            else:
                for ticket in filtered_tickets:
                    print(ticket)
                    print('-'*20)
            break
        except ValueError as ve:
            print(f'{ve}. Please select a valid priority level.')


def ticket_by_category(emp_id: str, ticket_history: list, category_options: list):
    print("Displaying tickets raised by you based on category:")
    for i in range(len(category_options)):
        print(f"Select {i + 1} to view tickets with {category_options[i]} category")
    while True:
        try:
            category_choice = int(input('Enter the number corresponding to your category choice: '))
            if category_choice < 1 or category_choice > len(category_options):
                raise ValueError('Invalid category selection.')
            selected_category = category_options[category_choice - 1]
            print(f'Displaying tickets with {selected_category} category:')
            filtered_tickets = [ticket for ticket in ticket_history if ticket.category == selected_category]
            if not filtered_tickets:
                print(f'No tickets found with {selected_category} category.')
            else:
                for ticket in filtered_tickets:
                    print(ticket)
                    print('-'*20)
            break
        except ValueError as ve:
            print(f'{ve}. Please select a valid category.')


def ticket_by_status(emp_id: str, ticket_history: list, status_options: list):
    print("Displaying tickets raised by you based on status:")
    for i in range(len(status_options)):
        print(f"Select {i + 1} to view tickets with {status_options[i]} status")
    while True:
        try:
            status_choice = int(input('Enter the number corresponding to your status choice: '))
            if status_choice < 1 or status_choice > len(status_options):
                raise ValueError('Invalid status selection.')
            selected_status = status_options[status_choice - 1]
            print(f'Displaying tickets with {selected_status} status:')
            filtered_tickets = [ticket for ticket in ticket_history if ticket.status == selected_status]
            if not filtered_tickets:
                print(f'No tickets found with {selected_status} status.')
            else:
                for ticket in filtered_tickets:
                    print(ticket)
                    print('-'*20)
            break
        except ValueError as ve:
            print(f'{ve}. Please select a valid status.')


def ticket_counts(emp_id: str, ticket_history: list, parameters: dict):
    status_counts = {status: len([ticket for ticket in ticket_history if ticket.status == status]) for status in model.STATUS_FLOW}
    category_counts = {category: len([ticket for ticket in ticket_history if ticket.category == category]) for category in parameters['categories']}
    breached_tickets = [ticket for ticket in ticket_history if ticket.is_breached()]
    print('-'*20)
    print('Ticket count by status:')
    for status, count in status_counts.items():
        print(f'{status}: {count}')
    print('-'*20)
    print('Ticket count by category:')
    for category, count in category_counts.items():
        print(f'{category}: {count}')
    print('-'*20)
    print(f'SLA breached tickets: {len(breached_tickets)}')
    for ticket in breached_tickets:
        print(f'Ticket ID: {ticket.ticket_id} | {ticket.priority} | {ticket.status} | SLA deadline was {ticket.get_sla_deadline().strftime("%Y-%m-%d %H:%M:%S")}.')


def check_summary(emp_id: str, ticket_history: list, parameters: dict):
    category_options = parameters['categories']
    status_options = model.STATUS_FLOW
    priority_options = list(parameters['sla_hrs'].keys())
    while True:
        print('-'*20)
        print(f'Checking ticket summary for Employee ID: {emp_id}')
        print("Select 1 to view all tickets raised by you")
        print("Select 2 to view tickets raised by you based on priority")
        print("Select 3 to view tickets raised by you based on category")
        print("Select 4 to view tickets raised by you based on status")
        print("Select 5 to view ticket counts and SLA breached tickets")
        print("Select 6 to go back to the main menu")
        try:
            summary_choice = int(input('Please select a summary option: '))
            if summary_choice == 1:
                print('Displaying all tickets:')
                if(len(ticket_history) == 0):
                    print('No tickets raised yet.')
                else:
                    print('-'*20)
                    for ticket in ticket_history:
                        print(ticket)
                        print('-'*20)
            elif summary_choice == 2:
                ticket_by_priority(emp_id, ticket_history, priority_options)
            elif summary_choice == 3:
                ticket_by_category(emp_id, ticket_history, category_options)
            elif summary_choice == 4:
                ticket_by_status(emp_id, ticket_history, status_options)
            elif summary_choice == 5:
                ticket_counts(emp_id, ticket_history, parameters)
            elif summary_choice == 6:
                print('Going back to the main menu...')
                break
            else:
                raise ValueError('Invalid summary option selection.')
        except ValueError as ve:
            print(f'{ve}. Please select a valid summary option.')
