from datetime import datetime


def show_time(date_posted):
    t = datetime.utcnow() - date_posted
    if t.seconds < 59:
        return f'{t.seconds}s'
    elif 50 <= t.seconds < 3600:
        return f'{t.seconds//60}m'
    elif t.days < 1:
        return f'{t.seconds//3600}h'
    elif date_posted.year == datetime.utcnow().year:
        return date_posted.strftime('%d %b')
    else: 
        return date_posted.strftime('%d %b %Y')