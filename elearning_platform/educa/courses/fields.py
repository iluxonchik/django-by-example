from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class OrderField(models.PositiveIntegerField):

    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super(OrderField, self).__init__(*args, **kwargs)

    # NOTE: 'add' indicates wether the instance is being saved to the DB for the first time
    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is None:
            # No current value for the OrderField field
            try:
                qs = self.model.objects.all()
                if self.for_fields:
                    # filter the objects with the same field values for the fields in "for_fields"
                    query = {field: getattr(model_instance, field) for field in self.for_fields}
                    qs = qs.filter(**query)
                    # get the order of the last item
                    last_item = qs.latest(self.attname)
                    value = last_item.order + 1
            except ObjectDoesNotExist:
                # Adding the first relation to the table
                value = 0
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(OrderField, self).pre_save(model_instance, add)
