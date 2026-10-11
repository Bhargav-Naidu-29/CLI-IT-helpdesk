import datetime, json, os

STATUS_FLOW = ['Open', 'In Progress', 'Resolved', 'Closed']


class Ticket:
    def __init__(self, ticket_id, emp_id, name, description, category, priority, status, created_at, sla_hrs):
        self.ticket_id = ticket_id
        self.emp_id = emp_id
        self.name = name
        self.description = description
        self.category = category
        self.priority = priority
        self.status = status
        self.created_at = created_at
        self.sla_hrs = sla_hrs


    def get_sla_deadline(self):
        sla_hours = self.sla_hrs
        # Calculate the SLA deadline by adding sla_hours to created_at
        return self.created_at + datetime.timedelta(hours = sla_hours)


    def is_breached(self):
        # Resolved and Closed tickets are no longer running against the SLA
        if self.status in ('Resolved', 'Closed'):
            return False
        return self.get_sla_deadline() < datetime.datetime.now()


    def to_dict(self):
        ticket_data = self.__dict__.copy()
        ticket_data['created_at'] = self.created_at.isoformat()
        return ticket_data


    @classmethod
    def from_dict(cls, ticket_data):
        ticket_data = ticket_data.copy()
        ticket_data['created_at'] = datetime.datetime.fromisoformat(ticket_data['created_at'])
        return cls(**ticket_data)


    def __str__(self):
        sla_state = 'BREACHED' if self.is_breached() else 'Within SLA'
        return f'Ticket ID: {self.ticket_id}\nEmployee ID: {self.emp_id}\nName: {self.name}\nDescription: {self.description}\nCategory: {self.category}\nPriority: {self.priority}\nStatus: {self.status}\nCreated At: {self.created_at.strftime("%Y-%m-%d %H:%M:%S")}\nSLA Hours: {self.sla_hrs}\nSLA Deadline: {self.get_sla_deadline().strftime("%Y-%m-%d %H:%M:%S")}\nSLA State: {sla_state}'


def load_tickets(file_path: str) -> list:
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, 'r') as file:
            return [Ticket.from_dict(ticket_data) for ticket_data in json.load(file)]
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
        print(f'Could not read saved tickets. Error details: {e}. Starting with an empty list.')
        return []


def save_tickets(file_path: str, ticket_history: list):
    try:
        with open(file_path, 'w') as file:
            json.dump([ticket.to_dict() for ticket in ticket_history], file, indent = 4)
    except OSError as e:
        print(f'Could not save tickets. Error details: {e}')
