import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .models import Action

def create_action(user, verb, target=None):
    # check for any similiar aciton made in the last minute
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    similiar_actions = Action.objects.filter(user_id=user.id, verb=verb, created__gte=last_minute)

    if target:
        target_ct = ContentType.objects.get_for_model(target)  # returns a ContentType instance representing the model of "taget"
        similiar_acitons = similiar_actions.filter(target_ct=target_ct, target_id=target.id)

    if not similiar_actions:
        # no similiar actions found (in the last minute)
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True
    return False
