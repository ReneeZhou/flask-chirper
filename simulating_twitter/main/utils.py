from simulating_twitter.models import User


def get_recommendation(current_user):
    people = User.query.all()
    follow_recommendation = []
    
    for person in people:
        if len(follow_recommendation) < 4:
            if (not current_user.is_following(person)) and (current_user != person):
                follow_recommendation.append(person)

    return follow_recommendation