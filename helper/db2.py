import os
import django
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "helper.settings")
django.setup()

from handboook.models import Spell

real_dnd_spells = [
    {
        "name": "Вихрь Лезвий",
        "description": "Создает вихрь, наполненный острыми лезвиями, который наносит урон всем существам в радиусе.",
        "level": 3,
        "character_class": "Колдун, Маг",
        "school": "Школа разрушения",
        "casting_time": "1 действие",
        "range": "60 футов",
        "components": "V, S, M (металлические осколки)",
        "duration": "1 минута",
        "last_updated": datetime.now()
    },
    {
        "name": "Воскрешение",
        "description": "Мощное заклинание, позволяющее вернуть к жизни умершее существо, восстанавливая его к целому состоянию.",
        "level": 7,
        "character_class": "Клирик",
        "school": "Школа некромантии",
        "casting_time": "1 действие",
        "range": "Цель в пределах 10 футов",
        "components": "V, S, M (алмазы стоимостью 1000 золотых)",
        "duration": "Мгновенно",
        "last_updated": datetime.now()
    },
    {
        "name": "Волна Энергии",
        "description": "Выпускает волну энергии, которая наносит урон всем врагам в радиусе, в зависимости от типа энергии (огонь, холод, электричество).",
        "level": 5,
        "character_class": "Маг, Колдун",
        "school": "Школа разрушения",
        "casting_time": "1 действие",
        "range": "120 футов",
        "components": "V, S",
        "duration": "Мгновенно",
        "last_updated": datetime.now()
    },
    {
        "name": "Внезапное Поглощение",
        "description": "Перемещает цель в другое измерение, временно лишая ее возможности действовать.",
        "level": 6,
        "character_class": "Маг",
        "school": "Школа иллюзий",
        "casting_time": "1 действие",
        "range": "30 футов",
        "components": "V, S, M (песок)",
        "duration": "1 минута",
        "last_updated": datetime.now()
    },
    {
        "name": "Вихрь Стрел",
        "description": "Вызывает множество стрел, которые стремительно летят к врагам, нанося урон.",
        "level": 4,
        "character_class": "Колдун, Маг",
        "school": "Школа силы",
        "casting_time": "1 действие",
        "range": "90 футов",
        "components": "V, S",
        "duration": "Мгновенно",
        "last_updated": datetime.now()
    }
]

for spell in real_dnd_spells:
    Spell.objects.create(
        name=spell["name"],
        description=spell["description"],
        level=spell["level"],
        character_class=spell["character_class"],
        school=spell["school"],
        casting_time=spell["casting_time"],
        range=spell["range"],
        components=spell["components"],
        duration=spell["duration"],
        last_updated=spell["last_updated"]
    )

print("✅ Заклинания успешно добавлены в базу данных!")
