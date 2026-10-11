import ticket, summary, model, personalization


print('Welcome to the IT Service Desk Ticketing System!!!')
emp_id = input('Please enter your Employee ID: ').strip().upper()
while not emp_id or not emp_id.replace('-', '').replace('_', '').isalnum():
    print('Employee ID cannot be empty and can only contain letters, numbers, - or _.')
    emp_id = input('Please enter your Employee ID: ').strip()
parameters = personalization.get_my_parameters(emp_id)
print('Your parameters are as follows:')
for key, value in parameters.items():
    print(f'{key}: {value}')

file_path = f'tickets_{emp_id}.json'
ticket_history = model.load_tickets(file_path)
print(f'Loaded {len(ticket_history)} saved ticket(s).')
breached_count = len([t for t in ticket_history if t.is_breached()])
if breached_count > 0:
    print(f'WARNING: {breached_count} ticket(s) have breached their SLA!')



while True:
    print('-'*20)
    print(f'available services')
    print('Select 1 to raise a ticket')
    print('Select 2 to update a ticket status')
    print('Select 3 to check your ticket summary')
    print('Select 4 to exit the application')
    try:
        service = int(input('Please select a service: '))
        if service == 1:
            print('Navigating to ticket raising service...')
            ticket.raise_ticket(emp_id, parameters, ticket_history)
            model.save_tickets(file_path, ticket_history)
        elif service == 2:
            print('Navigating to ticket status update service...')
            ticket.update_ticket(emp_id, ticket_history)
            model.save_tickets(file_path, ticket_history)
        elif service == 3:
            print('Navigating to ticket summary service...')
            summary.check_summary(emp_id, ticket_history, parameters)
        elif service == 4:
            break

        else:
            raise ValueError('Invalid service selection.')
    except ValueError as ve:
        print(f'Please select a valid Service by choosing a number between 1 and 4. Error details: {ve}')
    except TypeError as e:
        print(f'Please select a valid Service by choosing a number between 1 and 4. Error details: {e}')
    except (EOFError, KeyboardInterrupt):
        print('\nInput closed. Exiting the application...')
        break
    except Exception as e:
        print(f'Unexpected error occurred: {e}')


print("Thank you for using the IT Service Desk Ticketing System. Goodbye!")
