from datetime import datetime


def show_time(created_at):
    t = datetime.utcnow() - created_at
    if t.seconds < 59:
        return f'{t.seconds}s'
    elif 50 <= t.seconds < 3600:
        return f'{t.seconds//60}m'
    elif t.days < 1:
        return f'{t.seconds//3600}h'
    elif created_at.year == datetime.utcnow().year:
        return created_at.strftime('%d %b')
    else: 
        return created_at.strftime('%d %b %Y')