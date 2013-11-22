# -*- coding: utf-8 -*-

from copy import copy, deepcopy

from django.db.models.manager import Manager


class CopyMixin(object):

    '''Mixin de copie personnalisé pour Django'''

    def __deepcopy__(self, memo):
        new = copy(self)
        new.pk = None
        new.save()

        print(self.__class__.__name__)

        if 'content_fields' in self.__class__.__dict__:
            for attr in self.content_fields:
                other = getattr(self, attr)
                print('\t%s - %s' % (other, other.__class__.__name__))
                if isinstance(other, Manager):

                    new_other = [deepcopy(instance) for instance in other.all()]

                    
                elif isinstance(other, CopyMixin):
                    print('\t\tCopyMixin')
                    new_other = deepcopy(other)
                else:
                    new_other = other

                new.__setattr__(attr, new_other)

            new.save()

        return new
