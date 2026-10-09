import random, hashlib


def get_my_parameters(emp_id: str) -> dict:
    seed = int(hashlib.sha256(emp_id.encode('utf-8')).hexdigest(), 16) % (2 ** 31)
    rng = random.Random(seed)
    all_categories = ['Software', 'Hardware', 'Network', 'Access Request', 'Email', 'Printer', 'VPN', 'Application Bug', 'Account Lockout', 'Data Backup']
    return {
        'categories': rng.sample(all_categories, 5),
        'sla_hrs': {
            'Critical' : rng.randint(2, 4),
            'High' : rng.randint(6, 12),
            'Medium' : rng.randint(24, 48),
            'Low' : rng.randint(72, 120),
        },
        'ticket_prefix' : rng.choice(['TCK', 'REQ', 'SR', 'INC']),
    }
