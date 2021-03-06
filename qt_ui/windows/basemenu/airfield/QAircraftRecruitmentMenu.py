from PySide2.QtCore import Qt
from PySide2.QtWidgets import QVBoxLayout, QGridLayout, QGroupBox, QScrollArea, QFrame, QWidget, QHBoxLayout, QLabel

from game.event import UnitsDeliveryEvent
from qt_ui.uiconstants import ICONS
from qt_ui.windows.basemenu.QRecruitBehaviour import QRecruitBehaviour
from theater import ControlPoint, CAP, CAS, db, ControlPointType
from game import Game


class QAircraftRecruitmentMenu(QFrame, QRecruitBehaviour):

    def __init__(self, cp: ControlPoint, game: Game):
        QFrame.__init__(self)
        self.cp = cp
        self.game = game

        for event in self.game.events:
            if event.__class__ == UnitsDeliveryEvent and event.from_cp == self.cp:
                self.deliveryEvent = event
        if not self.deliveryEvent:
            self.deliveryEvent = self.game.units_delivery_event(self.cp)

        # Determine maximum number of aircrafts that can be bought
        self.set_maximum_units(self.cp.available_aircraft_slots)
        self.set_recruitable_types([CAP, CAS])

        self.bought_amount_labels = {}
        self.existing_units_labels = {}

        self.hangar_status = QHangarStatus(self.total_units, self.cp.available_aircraft_slots)

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        units = {
            CAP: db.find_unittype(CAP, self.game.player_name),
            CAS: db.find_unittype(CAS, self.game.player_name),
        }

        scroll_content = QWidget()
        task_box_layout = QGridLayout()
        row = 0

        for task_type in units.keys():
            units_column = list(set(units[task_type]))
            if len(units_column) == 0: continue
            units_column.sort(key=lambda x: db.PRICES[x])
            for unit_type in units_column:
                if self.cp.is_carrier and not unit_type in db.CARRIER_CAPABLE:
                    continue
                if self.cp.is_lha and not unit_type in db.LHA_CAPABLE:
                    continue
                row = self.add_purchase_row(unit_type, task_box_layout, row)
            stretch = QVBoxLayout()
            stretch.addStretch()
            task_box_layout.addLayout(stretch, row, 0)

        scroll_content.setLayout(task_box_layout)
        scroll = QScrollArea()
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setWidgetResizable(True)
        scroll.setWidget(scroll_content)
        main_layout.addLayout(self.hangar_status)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

    def buy(self, unit_type):
        super().buy(unit_type)
        self.hangar_status.update_label(self.total_units, self.cp.available_aircraft_slots)

    def sell(self, unit_type):
        super().sell(unit_type)
        self.hangar_status.update_label(self.total_units, self.cp.available_aircraft_slots)


class QHangarStatus(QHBoxLayout):

    def __init__(self, current_amount: int, max_amount: int):
        super(QHangarStatus, self).__init__()
        self.icon = QLabel()
        self.icon.setPixmap(ICONS["Hangar"])
        self.text = QLabel("")

        self.update_label(current_amount, max_amount)
        self.addWidget(self.icon, Qt.AlignLeft)
        self.addWidget(self.text, Qt.AlignLeft)
        self.addStretch(50)
        self.setAlignment(Qt.AlignLeft)

    def update_label(self, current_amount: int, max_amount: int):
        self.text.setText("<strong>{}/{}</strong>".format(current_amount, max_amount))
