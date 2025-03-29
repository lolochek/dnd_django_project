from django import forms
from django.contrib.contenttypes.models import ContentType

from .models import Monster, Spell
from handbook.models import ChangeRequest

from django import forms
from django.contrib.contenttypes.models import ContentType
from .models import Monster


class MonsterChangeForm(forms.ModelForm):
    class Meta:
        model = Monster
        fields = ['name', 'description', 'hit_points', 'armor_class', 'speed', 'abilities']

    def save_changes(self, user, monster):
        changes = {}
        for field in self.changed_data:
            original_value = getattr(monster, field)
            new_value = self.cleaned_data[field]

            if original_value != new_value:
                changes[field] = new_value

        content_type = ContentType.objects.get_for_model(Monster)
        change_request = ChangeRequest.objects.create(
            user=user,
            content_type=content_type,
            object_id=monster.id,
            changes=changes
        )
        return change_request

class SpellChangeForm(forms.ModelForm):
    class Meta:
        model = Spell
        fields = ['name', 'description', 'level', 'character_class', 'school', 'casting_time', 'range', 'components', 'duration']

    def save_changes(self, user, spell):
        changes = {}
        for field in self.changed_data:
            original_value = getattr(spell, field)
            new_value = self.cleaned_data[field]

            if original_value != new_value:
                changes[field] = new_value

        content_type = ContentType.objects.get_for_model(Spell)
        change_request = ChangeRequest.objects.create(
            user=user,
            content_type=content_type,
            object_id=spell.id,
            changes=changes
        )
        return change_request