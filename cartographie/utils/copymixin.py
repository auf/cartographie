# -*- coding: utf-8 -*-

from copy import copy, deepcopy

from django.db.models.manager import Manager
from django.db.models import related


# List of related field types, cast to a tuple for further isinstance() usage
FIELD_TYPES = tuple([
    getattr(related, x)
    for x in dir(related)
    if isinstance(getattr(related, x), type)])


class CopyMixin(object):

    '''Mixin de copie personnalisé pour Django'''

    def __deepcopy__(self, memo):
        class_dict = self.__class__.__dict__
        fields = set([
            k
            for k, v in class_dict.items()
            if isinstance(v, FIELD_TYPES)])

        if 'content_fields' in class_dict:
            content_fields = set(self.content_fields)
            fields.union(content_fields)

        new = copy(self)
        new.pk = None
        new.save()

        print(self.__class__.__name__)

        for name in fields:
            print('\t%s' % (name, ))
            orig_field = getattr(self, name)

            if isinstance(orig_field, Manager):
                print('\t\tmanager')
                if name.endswith('_set'):
                    print('\t\t\t_set')
                    new_field = copy(orig_field)
                    for val in orig_field.all():
                        new_val = copy(val)
                        new_field.add(new_val)
                    setattr(new, name, new_field.all())
            elif isinstance(orig_field, CopyMixin):
                new_field = deepcopy(orig_field)
                setattr(new, name, new_field)
            else:
                new_field = orig_field
                setattr(new, name, new_field)

        new.save()
        
        return new
