from django.test import TestCase
from .models import Monster

# Create your tests here.

class MonsterModelTest(TestCase):
    def setUp(self):
        self.monster = Monster.objects.create(
            name="Goblin",
            description="Small green humanoid",
            hit_points=7,
            armor_class=13,
            speed="30ft",
            abilities="Darkvision, Nimble Escape"
        )

    def test_monster_creation(self):
        self.assertEqual(self.monster.name, "Goblin")
        self.assertEqual(self.monster.hit_points, 7)
        self.assertEqual(self.monster.armor_class, 13)
        self.assertEqual(self.monster.speed, "30ft")
        self.assertIn("Darkvision", self.monster.abilities)

    def test_apply_changes(self):
        changes = {
            "name": "Hobgoblin",
            "hit_points": 11,
            "armor_class": 15
        }
        self.monster.apply_changes(changes)
        self.monster.refresh_from_db()
        self.assertEqual(self.monster.name, "Hobgoblin")
        self.assertEqual(self.monster.hit_points, 11)
        self.assertEqual(self.monster.armor_class, 15)

    def test_last_updated_auto(self):
        before = self.monster.last_updated
        self.monster.description = "Updated description"
        self.monster.save()
        self.assertTrue(self.monster.last_updated > before)