import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "helper.settings")
django.setup()

from handbook.models import Monster

more_monsters = [
    {
        "name": "Красный Дракон (Древний)",
        "description": "Воплощение разрушения и власти. Красные драконы жадны, коварны и обожают накапливать несметные сокровища.",
        "hit_points": 546,
        "armor_class": 22,
        "speed": "40 футов, летая 80 футов",
        "abilities": {
            "attacks": [
                {
                    "name": "Огненное дыхание",
                    "damage": {"dice": "26к6", "type": "огненный", "amount": "91"},
                    "effect": "Каждое существо в конусе 90 футов должно сделать спасбросок Ловкости DC 24 или получить полный урон (половина при успехе)."
                },
                {
                    "name": "Когти",
                    "damage": {"dice": "4к10", "type": "рубящий", "amount": "42"},
                    "effect": "Если цель меньше дракона, она опрокинута."
                }
            ]
        },
        "additional_info": {"Легендарные действия": "Может атаковать когтями или двигаться в чужой ход."},
        "image_url": "https://dnd.su/gallery/bestiary/160_1_1626461868.jpg"
    },
    {
        "name": "Лич",
        "description": "Некогда могущественный волшебник, ставший нежитью ради вечной жизни и могущества.",
        "hit_points": 135,
        "armor_class": 17,
        "speed": "30 футов",
        "abilities": {
            "attacks": [
                {
                    "name": "Прикосновение Паралича",
                    "damage": {"dice": "3к6", "type": "некротический", "amount": "16"},
                    "effect": "Цель должна пройти спасбросок Телосложения DC 18 или быть парализованной на 1 минуту."
                },
                {
                    "name": "Магия",
                    "effect": "Может использовать Высшее заклинание раз в ход (например, Огненный шар, Круг Смерти, Остановку времени)."
                }
            ]
        },
        "additional_info": {"Филактерия": "Пока оно существует, лич не может быть окончательно уничтожен."},
        "image_url": "https://dnd.su/gallery/bestiary/165_1_1626461868.jpg"
    },
    {
        "name": "Тараск",
        "description": "Величайшее чудовище в мире, непобедимый гигант, который пробуждается раз в несколько веков, чтобы разрушить всё на своём пути.",
        "hit_points": 676,
        "armor_class": 25,
        "speed": "50 футов",
        "abilities": {
            "attacks": [
                {
                    "name": "Укус",
                    "damage": {"dice": "4к12", "type": "колющий", "amount": "45"},
                    "effect": "Если цель меньше Тараска, она проглочена."
                },
                {
                    "name": "Хвост",
                    "damage": {"dice": "3к10", "type": "ударный", "amount": "33"},
                    "effect": "Цель отбрасывается на 20 футов и опрокидывается."
                }
            ]
        },
        "additional_info": {"Магическая защита": "Иммунитет к магии 6 уровня и ниже."},
        "image_url": "https://dnd.su/gallery/bestiary/170_1_1626461868.jpg"
    },
    {
        "name": "Элементаль Огня",
        "description": "Пылающее воплощение хаотического огня, этот элементаль сжигает всё на своём пути.",
        "hit_points": 102,
        "armor_class": 13,
        "speed": "50 футов",
        "abilities": {
            "attacks": [
                {
                    "name": "Пылающий удар",
                    "damage": {"dice": "2к6", "type": "огненный", "amount": "12"},
                    "effect": "Цель воспламеняется, получая 1к10 урона в начале каждого хода."
                }
            ]
        },
        "additional_info": {"Неуязвимость": "Иммунитет к огню."},
        "image_url": "https://dnd.su/gallery/bestiary/175_1_1626461868.jpg"
    },
    {
        "name": "Минотавр",
        "description": "Жестокий гуманоид с головой быка, мастер лабиринтов и охоты.",
        "hit_points": 76,
        "armor_class": 14,
        "speed": "40 футов",
        "abilities": {
            "attacks": [
                {
                    "name": "Рогатый натиск",
                    "damage": {"dice": "2к10", "type": "колющий", "amount": "22"},
                    "effect": "Цель опрокинута, если не преуспеет в спасброске Силы DC 15."
                }
            ]
        },
        "additional_info": {"Лабиринтное чутьё": "Никогда не теряется в лабиринтах."},
        "image_url": "https://dnd.su/gallery/bestiary/180_1_1626461868.jpg"
    },
    {
        "name": "Демогоргон",
        "description": "Владыка Бездны, чудовище с двумя змееподобными головами, погружающее мир в хаос.",
        "hit_points": 496,
        "armor_class": 22,
        "speed": "50 футов",
        "abilities": {
            "attacks": [
                {
                    "name": "Хлыстовая рука",
                    "damage": {"dice": "6к10", "type": "рубящий", "amount": "55"},
                    "effect": "Цель делает спасбросок Мудрости DC 23 или теряет разум."
                }
            ]
        },
        "additional_info": {"Две головы": "Может действовать дважды за ход."},
        "image_url": "https://dnd.su/gallery/bestiary/185_1_1626461868.jpg"
    },
    {
        "name": "Вампир",
        "description": "Бессмертный хищник, охотящийся на живых ради их крови.",
        "hit_points": 144,
        "armor_class": 16,
        "speed": "30 футов, летая 40 футов",
        "abilities": {
            "attacks": [
                {
                    "name": "Укус",
                    "damage": {"dice": "3к6", "type": "некротический", "amount": "20"},
                    "effect": "Цель теряет хиты навсегда, пока не выпьет святую воду."
                }
            ]
        },
        "additional_info": {"Слабость к свету": "При свете солнца теряет все способности."},
        "image_url": "https://dnd.su/gallery/bestiary/190_1_1626461868.jpg"
    }
]

for monster in more_monsters:
    Monster.objects.create(
        name=monster["name"],
        description=monster["description"],
        hit_points=monster["hit_points"],
        armor_class=monster["armor_class"],
        speed=monster["speed"],
        abilities=monster["abilities"],
        additional_info=monster["additional_info"],
        image_url=monster["image_url"]
    )

print("✅ Монстры успешно добавлены!")
