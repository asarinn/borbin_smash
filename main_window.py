# Third party imports
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QMainWindow)

# Local imports
from main_window_init import Ui_MainWindow

# Character Info
STR = 24
RAGE_STR_BONUS = 4
ENLARGE_STR_BONUS = 2

# Attack Bonuses
BAB = 10
FEATS = 0
HASTE = 1
SURPRISE_ACCURACY = 2
ENLARGE = -1
POWER_ATTACK_ATTACK = -3
FLANKING = 2

# Damage Bonuses
POWERFUL_BLOW = 2
TWO_HANDED_MULTI = 1.5
POWER_ATTACK_DAMAGE = 6
DAMAGE_DIE = [1, 10]
ENLARGE_DAMAGE_DIE = [2, 8]

# Other
WEAPON_BONUS = 3  # Enchantment bonus
WEAPON_CRITICAL_MOD = 4  # x2, x3, x4, etc
INSPIRE = 3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Basic pyqt init for gui window
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Class variables to hold state of check boxes
        self.two_handed_enabled = True
        self.inspire_courage_enabled = False
        self.haste_enabled = False
        self.raging_enabled = False
        self.power_attack_enabled = False
        self.enlarged_enabled = False
        self.surprise_accuracy_enabled = False
        self.powerful_blow_enabled = False
        self.flanking_enabled = False

        # Connections to toggle state on check box click
        self.ui.two_handed_check_box.clicked.connect(self.two_handed_toggled)
        self.ui.inspire_courage_check_box.clicked.connect(self.inspire_courage_toggled)
        self.ui.haste_check_box.clicked.connect(self.haste_toggled)
        self.ui.raging_check_box.clicked.connect(self.raging_toggled)
        self.ui.power_attack_check_box.clicked.connect(self.power_attack_toggled)
        self.ui.enlarged_check_box.clicked.connect(self.enlarged_toggled)
        self.ui.surprise_accuracy_check_box.clicked.connect(self.surprise_accuracy_toggled)
        self.ui.powerful_blow_check_box.clicked.connect(self.powerful_blow_toggled)
        self.ui.flanking_bonus_check_box.clicked.connect(self.flanking_toggled)

        # Initialize output with initial settings
        self.update_output()

    def two_handed_toggled(self, state):
        self.two_handed_enabled = state
        self.update_output()

    def inspire_courage_toggled(self, state):
        self.inspire_courage_enabled = state
        self.update_output()

    def haste_toggled(self, state):
        self.haste_enabled = state
        self.update_output()

    def raging_toggled(self, state):
        self.raging_enabled = state
        self.update_output()

    def power_attack_toggled(self, state):
        self.power_attack_enabled = state
        self.update_output()

    def enlarged_toggled(self, state):
        self.enlarged_enabled = state
        self.update_output()

    def surprise_accuracy_toggled(self, state):
        self.surprise_accuracy_enabled = state
        self.update_output()

    def powerful_blow_toggled(self, state):
        self.powerful_blow_enabled = state
        self.update_output()

    def flanking_toggled(self, state):
        self.flanking_enabled = state
        self.update_output()

    def update_output(self):
        # Calculate strength bonus
        strength = STR
        if self.raging_enabled:
            strength += RAGE_STR_BONUS
        if self.enlarged_enabled:
            strength += ENLARGE_STR_BONUS
        effective_strength_bonus = int((strength - 10) / 2)

        attack_bonus = self.calculate_attack_bonus(effective_strength_bonus)
        self.ui.attack_bonus_label.setText(f' Attack Bonus: +{attack_bonus}')

        die, damage = self.calculate_damage(effective_strength_bonus)
        self.ui.damage_label.setText(f'Damage: {die[0]}d{die[1]} + {damage}')
        self.ui.crit_damage_label.setText(
            f'Critical Damage: {WEAPON_CRITICAL_MOD * die[0]}d{die[1]} + {WEAPON_CRITICAL_MOD * damage}')

    def calculate_attack_bonus(self, effective_strength_bonus):
        attack_bonus = BAB + WEAPON_BONUS + effective_strength_bonus

        if self.inspire_courage_enabled:
            attack_bonus += INSPIRE

        if self.haste_enabled:
            attack_bonus += HASTE

        if self.power_attack_enabled:
            attack_bonus += POWER_ATTACK_ATTACK

        if self.enlarged_enabled:
            attack_bonus += ENLARGE

        if self.surprise_accuracy_enabled:
            attack_bonus += SURPRISE_ACCURACY

        if self.flanking_enabled:
            attack_bonus += FLANKING

        return attack_bonus

    def calculate_damage(self, effective_strength_bonus):
        damage = WEAPON_BONUS

        strength_damage = effective_strength_bonus
        if self.two_handed_enabled:
            strength_damage = int(strength_damage * TWO_HANDED_MULTI)
        damage += strength_damage

        if self.powerful_blow_enabled:
            damage += POWERFUL_BLOW

        power_attack_damage = 6
        if self.two_handed_enabled:
            power_attack_damage = int(power_attack_damage * TWO_HANDED_MULTI)
        if self.power_attack_enabled:
            damage += power_attack_damage

        if self.inspire_courage_enabled:
            damage += INSPIRE

        if self.enlarged_enabled:
            die = ENLARGE_DAMAGE_DIE
        else:
            die = DAMAGE_DIE

        return die, damage
