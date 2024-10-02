# IMPORTS
from pugilism import *

from textual.app import App, ComposeResult
from textual import on
from textual.containers import Horizontal
from textual.widgets import Button, Footer, Header, OptionList, Label, Static, Switch, RadioButton, RadioSet
from textual.widgets.option_list import Option
from textual.screen import Screen

from rich.text import Text

class TimeDisplay(Static):
    """Custom time display widget"""

class Stopwatch(Static):
    """Custom widget"""
    def compose(self):
        # this compose method tells the stopwatch widget what widgets go inside it
        # for the example, the stopwatch, we need to yield these:
        yield Button("Start", variant="success")# the text is the label for it
        yield Button("Stop", variant="error")
        yield Button("Reset")
        yield TimeDisplay("00:00:00.00")

# Textual doesn't have a TimeDisplay widget
# when you inherit from a widget you're creating a widget.
# Depending on the widget you're inheriting from, you can make diff things
# well Static is like a clean/clear/blank slate for u to work with but it makes some work for you to make it more painless.

class Menu(Screen):
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)      
        
        yield OptionList(
            Option("Fight!", id="fight"),
            Option("See Roster", id="roster"),
            Option("See Rules", id="rules"),
            Option("Options", id="options"),
            Option("Match History", id="history")
        )
        yield Footer()

    @on(OptionList.OptionSelected)
    async def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        # Handle the event
        selected_option = event.option
        await app.push_screen(selected_option.id)

class Fight(Screen):
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal():
            # A RadioSet built up from RadioButtons.
            with RadioSet(id="focus_me"):
                for pugilist in pugilists:
                    yield RadioButton(str(pugilist))
        yield Footer()

class Roster(Screen):
    def compose(self) -> ComposeResult:

        yield Header(show_clock=True)

        for pugilist in pugilists:
            rich_text = Text()
            rich_text.append(f"Name: ", style="bold magenta")
            rich_text.append(f"{pugilist.name}\n", style="bold white")
            rich_text.append(f"STR: {pugilist.strength} ", style="bold red")
            rich_text.append(f"DEX: {pugilist.dexterity} ", style="bold green")
            rich_text.append(f"CON: {pugilist.constitution}\n", style="bold blue")
            rich_text.append(f"Classes: {', '.join(pugilist.classes)}", style="italic yellow")
                
            yield Label(rich_text)

        yield Footer()

class Rules(Screen):
    def compose(self) -> ComposeResult:

        yield Header(show_clock=True)

        rich_rules = "INSERT NICELY FORMATTED RULES HERE"

        yield Label(rich_rules)

        yield Footer()


class Options(Screen):
    def compose(self) -> ComposeResult:

        yield Header(show_clock=True)
        yield Static("[b]Options\n", classes="label")

        yield Horizontal(
            Static("off:     ", classes="label"),
            Switch(animate=True),
            classes="container",
        )
        yield Horizontal(
            Static("on:      ", classes="label"),
            Switch(value=True),
            classes="container",
        )

        focused_switch = Switch()
        focused_switch.focus()
        yield Horizontal(
            Static("focused: ", classes="label"), focused_switch, classes="container"
        )

        yield Horizontal(
            Static("custom:  ", classes="label"),
            Switch(id="custom-design"),
            classes="container",
        )

        yield Footer()
##########################################################

class PugilismApp(App):
    SCREENS={
        "menu": Menu,
        "fight": Fight,
        "roster": Roster,
        "rules": Rules,
        "options": Options#,
        #"history": History
             }
    
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("m", "push_menu", "Return to Menu")
        ]

    def on_mount(self) -> None:
        self.push_screen("menu")

    async def action_push_menu(self) -> None:
        await self.push_screen("menu")

if __name__ == "__main__":
    app = PugilismApp()
    app.run()