from cartographie.formation.models import Fichier, Formation
from django.forms.models import inlineformset_factory
from django.forms import ClearableFileInput, ModelForm, BooleanField, URLField

from django.utils.safestring import mark_safe
from django.utils.html import escape
from django.utils.encoding import force_unicode
from django.core.urlresolvers import reverse


class CustomClearableFileInput(ClearableFileInput):

    # value: FileField
    def render(self, name, value, attrs=None):
        substitutions = {
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
        }
        template = u'%(input)s'
        substitutions['input'] = super(ClearableFileInput, self).render(name, value, attrs)

        if value:
            url = reverse("formation_fichiers", args=[self.token, value.instance.formation_id, value.instance.id])
            name = value.instance.nom

            template = self.template_with_initial
            substitutions['initial'] = (u'<a href="%s">%s</a>'
                                        % (escape(url),
                                           escape(force_unicode(name))))
            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
                substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
                substitutions['clear'] = CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
                substitutions['clear_template'] = self.template_with_clear % substitutions

        return mark_safe(template % substitutions)


class FichierForm(ModelForm):
    class Meta:
        model = Fichier
        widgets = {
            'file': CustomClearableFileInput,
            }



class FichierViewModel(object):
    files = None
    forms = None

    def __init__(self, request, token, formation_id):
        self.formation = Formation.objects.get(pk=formation_id)
        self.token = token

        self.files = Fichier.objects.filter(formation=self.formation).order_by('nom')

        # Model field -> Form field
        def callback(field, **kwargs):
            form_field = field.formfield(**kwargs)

            if field.name == 'file':
                form_field.widget.token = token

            return form_field

        FichierFormSet = inlineformset_factory(Formation, Fichier, extra=1, form=FichierForm, formfield_callback=callback)

        if request.method == "POST":
            self.formset = FichierFormSet(data=request.POST, files=request.FILES, instance=self.formation)
            if self.formset.is_valid():
                self.formset.save()
        self.formset = FichierFormSet(instance=self.formation)

    def get_data(self):
        return { 'files': self.files,
                 'formation': self.formation,
                 'token': self.token,
                 'formset': self.formset,
                 }
