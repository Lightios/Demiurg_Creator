from kivy.graphics import Color
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from widgets.connection import ItemConfirm, Connection
from widgets.drag_card import DragCard


Builder.load_file('screens/creator_screen.kv')


class CreatorScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.marked_card = None
        self.cards = []
        self.line = None
        self.dialog = None
        self.selected_one = None
        self.selected_two = None
        self.selecting_stage = 0
        self.spawned_rooms = 0
        self.connections = []
        DragCard.creator_screen = self

    def spawn(self):
        card = DragCard()
        card.text = f"New Location {self.spawned_rooms}"
        self.cards.append(card)
        self.ids.content.add_widget(card)

        self.spawned_rooms += 1

    def debug(self):
        print(1)

    def unmark(self):
        if self.marked_card is not None:
            self.marked_card.line_color = 0, 0, 0, 0
            self.marked_card = None

        self.ids.input.disabled = True

    def on_size(self, *args):
        DragCard.MIN_X = self.ids.content.x
        DragCard.MAX_X = self.ids.content.x + self.ids.content.width

    def mark(self, card):
        """
        Marks a card (to edit in right section), unmarks currently marked (if exists)
        :param card: Card to be marked
        :return: None
        """
        card.line_color = "aqua"

        if self.marked_card is not None:
            self.marked_card.line_color = 0, 0, 0, 0

        self.marked_card = card
        self.ids.input.disabled = False
        self.ids.input.text = card.text

    def on_text(self, text: str):
        """
        Called from TextInput, update marked card text with every change in input field
        :param text: text from TextInput
        :return: None
        """
        if self.marked_card is not None:
            self.marked_card.text = text

    def open_connection_dialog(self):
        items = [ItemConfirm(self, i, text=self.cards[i].text) for i in range(len(self.cards))]
        self.selected_one = None
        self.selected_two = None

        self.selecting_stage = 1
        self.dialog = MDDialog(
            title="Select root",
            type="confirmation",
            items=items,
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    # text_color=self.theme_cls.primary_color,
                    on_press=lambda x: self.dialog.dismiss(),
                ),
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    # text_color=self.theme_cls.primary_color,
                    on_press=lambda x: self.show_second_dialog()
                ),
            ],
        )
        self.dialog.open()

    def show_second_dialog(self):
        items = [ItemConfirm(self, i, text=self.cards[i].text) for i in range(len(self.cards)) if self.cards[i] is not self.selected_one]

        self.selecting_stage = 2
        self.selected_one.active = False

        self.dialog.dismiss()
        self.dialog = MDDialog(
            title="Select destination",
            type="confirmation",
            items=items,
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    # text_color=self.theme_cls.primary_color,
                    on_press=lambda x: self.dialog.dismiss(),
                ),
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    # text_color=self.theme_cls.primary_color,
                    on_press=lambda x: self.create_connection(),
                ),
            ],
        )
        self.dialog.open()

    def create_connection(self):
        self.dialog.dismiss()

        # TODO: before creating a connection, check if it already exists

        with self.ids.content.canvas.before:
            Color(1, 1, 1)
            card_size_halved = self.selected_one.width / 2

            connection = Connection(
                points=[self.selected_one.x + card_size_halved, self.selected_one.y + card_size_halved,
                        self.selected_two.x + card_size_halved, self.selected_two.y + card_size_halved],
                width=2)  # Initial connection coordinates and width
            self.connections.append(connection)
            self.selected_one.attached_connections_out.append(connection)
            self.selected_two.attached_connections_in.append(connection)
            self.ids.content.canvas.add(connection)

    def update_lines(self):
        for connection in self.connections:
            if connection.changed:
                connection.points = connection.temporary_points
                connection.changed = False
