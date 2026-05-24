"""
RPG QUEST 2.0 — Dynamic UI System
All colors and styles are pulled from the global SETTINGS for full customization.
"""
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, SpinnerColumn
from rich.text import Text
from rich.align import Align
from rich.box import ROUNDED, HEAVY, DOUBLE, MINIMAL, SQUARE
from rich.columns import Columns
from rich.rule import Rule
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.layout import Layout
from rich.live import Live
from rich.style import Style
from rich.syntax import Syntax
from rich import box

import time
import random
import sys
import re
import os

from settings import SETTINGS

console = Console()
try:
    import pyfiglet
    _HAS_PYGFIGLET = True
except ImportError:
    _HAS_PYGFIGLET = False

# ====== THEME SHORTCUTS ======
def C(key: str, default: str = "white") -> str:
    """Get color for key from current theme."""
    return SETTINGS.color(key, default)

def S(key: str, default: str = "bold white") -> str:
    """Get full style string from theme."""
    return SETTINGS.style(key, default)

def BC() -> str:
    """Get border color."""
    return C("border", "bright_blue")

def PC() -> str:
    """Get primary color."""
    return C("primary", "bright_blue")

def AC() -> str:
    """Get accent color."""
    return C("accent", "yellow")

# ====== STYLE DETECTION (uses theme colors) ======
_STYLE_RULES = [
    (r'(?i)\b(critical|CRIT)\b', f'bold {C("danger")} on {C("warning")}'),
    (r'(?i)\b(heal|potion|restore|recover|health)\b', f'bold {C("success")}'),
    (r'(?i)\b(damage|dealt|strike|slash|pierce|swing|attacks?)\b', f'bold {C("danger")}'),
    (r'(?i)\b(miss|misses|whiff)\b', f'dim {C("info")}'),
    (r'(?i)\b(dodge|evade|sidestep|nimbly|roll away)\b', f'bold {C("info")}'),
    (r'(?i)\b(defeat|collapse|fall(s|en)?|death|vanquish|succumb|knees buckle)\b', f'bold white on {C("danger")}'),
    (r'(?i)\blevel.?up\b', f'bold {C("success")} on black'),
    (r'(?i)\b(loot|gained|found!|reward|spoil)\b', f'bold {C("accent")}'),
    (r'(?i)\b(fire|flame|burn|ignite|scorch|ember|blaze)\b', f'bold {C("danger")} on {C("accent")}'),
    (r'(?i)\b(block|shield|protect|guard|deflect)\b', f'bold {C("secondary")}'),
    (r'(?i)\b(enchant|magic|arcane|rune|crystal|spell|prism)\b', f'bold {C("magic")}'),
    (r'(?i)\b(gold|coin|diamond|dragonite)\b', f'bold {C("gold")}'),
    (r'(?i)\b(welcome|hello|greetings)\b', f'bold {PC()}'),
    (r'(?i)\b(broken|breaks?)\b', f'bold {C("danger")} on black'),
    (r'(?i)\b(divine|holy|bless)\b', f'bold {C("accent")} on {C("secondary")}'),
]

def auto_style(text):
    for pattern, style in _STYLE_RULES:
        if re.search(pattern, str(text)):
            return style
    return f"bold {C('text', 'white')}"

# ====== CORE OUTPUT ======
def clear():
    console.clear()

def type(text, delay=None, style=None):
    if delay is None:
        delay = SETTINGS.get_text_speed()
    if not SETTINGS.get("typing_effect", True):
        console.print(str(text) if style is None else Text(str(text), style=style or auto_style(text)))
        return
    if style is None:
        style = auto_style(text)
    styled = Text(str(text), style=style)
    for char in styled:
        console.print(char, end="")
        sys.stdout.flush()
        time.sleep(delay)
    print()

def fasttype(text, delay=None, style=None):
    if delay is None:
        delay = SETTINGS.get_fast_speed()
    if not SETTINGS.get("typing_effect", True):
        console.print(str(text) if style is None else Text(str(text), style=style or auto_style(text)))
        return
    if style is None:
        style = auto_style(text)
    styled = Text(str(text), style=style)
    for char in styled:
        console.print(char, end="")
        sys.stdout.flush()
        time.sleep(delay)
    print()

def chat(text):
    styles = [f"bold {C('text')}", f"italic {C('info')}", f"bold {C('accent')}", S("success", "green")]
    style = random.choice(styles)
    styled = Text(str(text), style=style)
    for char in styled:
        d = random.choice([0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07])
        console.print(char, end="")
        sys.stdout.flush()
        time.sleep(d)
    print()

# ====== EVENT MESSAGES (theme-powered) ======
def event(text, event_type="info"):
    style_map = {
        "damage": f"bold {C('danger')}",
        "heal": f"bold {C('success')}",
        "crit": f"bold {C('danger')} on {C('warning')}",
        "miss": f"dim {C('danger')}",
        "dodge": f"bold {C('info')}",
        "loot": f"bold {C('accent')}",
        "levelup": f"bold {C('success')} on black",
        "info": f"bold {C('text')}",
        "death": f"bold white on {C('danger')}",
        "fire": f"bold {C('danger')} on {C('warning')}",
        "shield": f"bold {C('secondary')}",
        "magic": f"bold {C('magic')}",
        "gold": f"bold {C('gold')}",
        "warning": f"bold {C('warning')} on black",
        "enchant": f"bold {C('magic')} on black",
        "boss": f"bold {C('danger')} on black",
        "victory": f"bold {C('warning')} on {C('success')}",
        "title": f"bold white on {C('secondary')}",
    }
    style = style_map.get(event_type, f"bold {C('text')}")
    if SETTINGS.get("colorize_events", True):
        console.print(Text(str(text), style=style))
    else:
        console.print(str(text))

# ====== PANELS (theme-aware) ======
def _get_panel_box():
    style_name = SETTINGS.get_panel_style()
    return {
        "heavy": box.HEAVY, "rounded": box.ROUNDED, "double": box.DOUBLE,
        "square": box.SQUARE, "minimal": box.MINIMAL, "none": box.MINIMAL,
    }.get(style_name, box.HEAVY)

def menu_panel(title, items, border_style=None):
    if border_style is None: border_style = BC()
    content_parts = []
    for label, desc in items:
        content_parts.append(f"  [bold {PC()}]{label}[/bold {PC()}]  [{C('text')}]{desc}[/{C('text')}]")
    content = "\n\n".join(content_parts)
    panel = Panel(
        Align.left(content),
        title=f"[bold {AC()}]{title}[/bold {AC()}]",
        border_style=border_style,
        box=_get_panel_box(),
        padding=(1, 2)
    )
    console.print(panel)

def info_panel(title, content, border_style=None):
    if border_style is None: border_style = C("success")
    panel = Panel(
        str(content),
        title=f"[bold {PC()}]{title}[/bold {PC()}]",
        border_style=border_style,
        box=box.ROUNDED,
        padding=(1, 2)
    )
    console.print(panel)

def announcement(text, subtext=None, style=None):
    if style is None:
        style = f"bold {AC()} on {C('secondary')}"
    if _HAS_PYGFIGLET:
        try:
            banner = pyfiglet.figlet_format(str(text), font="banner")
            content = f"[{style}]{banner}[/{style}]"
            if subtext:
                content += f"\n\n[bold white]{subtext}[/bold white]"
            panel = Panel(
                Align.center(content),
                border_style=AC(),
                box=box.DOUBLE,
                padding=(1, 2)
            )
            console.print(panel)
            return
        except:
            pass
    content = f"[{style}]{text}[/{style}]"
    if subtext:
        content += f"\n[white]{subtext}[/white]"
    panel = Panel(Align.center(content), border_style=AC(), box=_get_panel_box(), padding=(1, 2))
    console.print(panel)

def combat_panel(player_name, player_hp, player_max, enemy_name, enemy_hp, enemy_max, turn=0):
    pcolor = C("success")
    ecolor = C("danger")
    player_bar = _hp_bar_str(player_hp, player_max, 15)
    enemy_bar = _hp_bar_str(enemy_hp, enemy_max, 15)
    content = f"[bold {pcolor}]{player_name}[/bold {pcolor}]  {player_bar}\n\n[bold {ecolor}]{enemy_name}[/bold {ecolor}]  {enemy_bar}"
    if turn:
        content = f"[dim]Turn {turn}[/dim]\n\n" + content
    panel = Panel(
        Align.center(content),
        border_style=C("text") if SETTINGS.get("show_borders", True) else "black",
        box=_get_panel_box() if SETTINGS.get("show_borders", True) else box.MINIMAL,
        padding=(1, 3)
    )
    console.print(panel)

def _hp_bar_str(current, maximum, width=15):
    if not SETTINGS.get("show_hp_bars", True):
        return f"[bold]{int(current)}/{int(maximum)}[/bold]"
    ratio = current / maximum if maximum > 0 else 0
    filled = int(ratio * width)
    empty = width - filled
    if ratio > 0.6:
        color = C("hp_high", "green")
    elif ratio > 0.3:
        color = C("hp_mid", "yellow")
    else:
        color = C("hp_low", "red")
    bar = f"[{color}]{'█' * filled}[/{color}][dim]{'░' * empty}[/dim]"
    return f"{bar} [bold]{int(current)}/{int(maximum)}[/bold]"

# ====== TABLES ======
def section(text, style=None):
    if style is None:
        style = f"bold {PC()}"
    console.print()
    console.print(Rule(f"[{style}]{text}[/{style}]", style=BC()))
    console.print()

def stats_table(stats_dict):
    table = Table(
        box=_get_panel_box() if SETTINGS.get("show_borders", True) else box.MINIMAL,
        border_style=BC(),
        title=f"[bold {AC()}]{C('text')}[/bold {AC()}]"  # Will be replaced by actual title below
    )
    # Actually set the title properly
    table.title = f"[bold {AC()}]Player Stats[/bold {AC()}]"
    table.border_style = BC()
    table.add_column("Stat", style=f"bold {PC()}", width=22)
    table.add_column("Value", style=f"bold {C('text')}")
    special = {"Name", "Lvl", "HP", "Gold", "EXP", "Max EXP"}
    keys = [k for k in stats_dict if k not in special or k in special]
    special_keys = [k for k in keys if k in special and not isinstance(stats_dict[k], (dict, list))]
    other_keys = [k for k in keys if k not in special and not isinstance(stats_dict[k], (dict, list))]
    for key in special_keys + other_keys:
        val = stats_dict[key]
        if key == "Gold":
            table.add_row(str(key), f"[bold {C('gold')}]{val}[/bold {C('gold')}]")
        elif key == "HP":
            table.add_row(str(key), f"[bold {C('success')}]{val}[/bold {C('success')}]")
        elif key == "Lvl":
            table.add_row(str(key), f"[bold {C('magic')}]{val}[/bold {C('magic')}]")
        elif key == "EXP":
            me = stats_dict.get("Max EXP", "?")
            table.add_row(str(key), f"[bold {C('info')}]{val}[/bold {C('info')}] / [bold]{me}[/bold]")
        else:
            table.add_row(str(key), str(val))
    console.print(table)

def equip_card(title, equip_dict, border=None):
    if border is None: border = C("info")
    if not equip_dict:
        console.print(f"  [dim italic]{title}: Empty[/dim italic]")
        return
    table = Table(box=box.MINIMAL, show_header=False, padding=(0, 1))
    table.add_column("Field", style=f"bold {PC()}", width=14)
    table.add_column("Value", style=f"bold {C('text')}", overflow="fold")
    name = equip_dict.get("Name", "Unknown")
    cls = equip_dict.get("Class", "")
    nc = {"Weapon": C("weapon", "bold red"), "Helmet": C("armor", "bold blue"),
          "Chestplate": C("armor", "bold blue"), "Leggings": C("armor", "bold blue"),
          "Boots": C("armor", "bold blue"), "Shield": C("armor", "bold blue"),
          "Rune": C("magic", "bold magenta"), "Scroll": C("accent", "bold yellow"),
          "Artifact": C("legendary", "bold yellow"), "Ring": C("epic", "bold magenta")}.get(cls, "bold white")
    if "Potion" in cls: nc = C("potion", "bold green")
    table.add_row(f"[bold {AC()}]Name[/bold {AC()}]", f"[{nc}]{name}[/{nc}]")
    for k, v in equip_dict.items():
        if k != "Name":
            sk = "bold white"
            if k in ("ATK", "DMG"): sk = f"bold {C('danger')}"
            elif k == "DEF": sk = f"bold {C('secondary')}"
            elif k in ("SP", "Speed"): sk = f"bold {C('success')}"
            elif k == "Cost": sk = f"bold {C('gold')}"
            elif k in ("DUR", "MAX DUR"): sk = f"bold {C('text')}"
            elif k == "Tier": sk = f"bold {C('magic')}"
            table.add_row(f"  {k}", Text(str(v), style=sk))
    panel = Panel(
        Align.left(table),
        title=f"[bold {AC()}]{title}[/bold {AC()}]",
        border_style=border,
        box=box.ROUNDED,
        padding=(0, 1)
    )
    console.print(panel)

def inventory_table(items, title="Backpack"):
    if not items:
        console.print("  [dim italic]Backpack is empty[/dim italic]")
        return
    keys = ["Name"]
    seen = set(keys)
    for item in items:
        for k in item:
            if k not in seen:
                keys.append(k)
                seen.add(k)
    table = Table(
        box=_get_panel_box() if SETTINGS.get("show_borders", True) else box.MINIMAL,
        border_style=C("info"),
        title=f"[bold {AC()}]{title}[/bold {AC()}]",
        show_lines=True, padding=(0, 1),
        row_styles=["", "dim"]
    )
    wc = C("weapon", "bold red"); ac = C("armor", "bold blue"); gc = C("success", "bold green")
    mc = C("magic", "bold magenta"); yc = C("accent", "bold yellow")
    for i, k in enumerate(keys):
        style = f"bold {C('text')}"
        if k == "ATK": style = f"bold {C('danger')}"
        elif k == "DEF": style = f"bold {C('secondary')}"
        elif k == "Cost": style = f"bold {C('gold')}"
        elif k == "Class": style = f"bold {C('magic')}"
        table.add_column(k, style=style, max_width=28, overflow="fold")
    for item in items:
        row = []
        for k in keys:
            val = item.get(k, "")
            if isinstance(val, float):
                val = f"{val:.1f}" if val != int(val) else str(int(val))
            else:
                val = str(val)
            cls = item.get("Class", "")
            if k == "Name":
                if cls == "Weapon": val = f"[{wc}]{val}[/{wc}]"
                elif cls in ("Helmet","Chestplate","Leggings","Boots","Shield"): val = f"[{ac}]{val}[/{ac}]"
                elif "Potion" in cls: val = f"[{gc}]{val}[/{gc}]"
                elif cls == "Rune": val = f"[{mc}]{val}[/{mc}]"
                elif cls == "Scroll": val = f"[{yc}]{val}[/{yc}]"
                elif cls == "Artifact": val = f"[bold {C('legendary')}]{val}[/bold {C('legendary')}]"
            row.append(val)
        table.add_row(*row)
    console.print(table)

# ====== PROGRESS ======
def loading_bar(description, duration):
    progress = Progress(
        SpinnerColumn("dots", style=f"bold {PC()}"),
        TextColumn(f"[bold {PC()}]{description}[/bold {PC()}]"),
        BarColumn(bar_width=40, style=BC(), complete_style=C("success"), finished_style=C("success")),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
        console=console,
    )
    with progress:
        task = progress.add_task(description, total=duration)
        elapsed = 0.0
        while elapsed < duration:
            time.sleep(0.1)
            elapsed = min(elapsed + 0.1, duration)
            progress.update(task, completed=elapsed)

# ====== PROMPTS ======
def input_prompt(prompt="", password=False):
    return console.input(f"[bold {AC()}]{prompt}[/bold {AC()}]")

def int_prompt(prompt="", default=None):
    result = console.input(f"[bold {AC()}]{prompt}[/bold {AC()}]")
    if default is not None and result.strip() == "":
        return default
    try:
        return int(result)
    except ValueError:
        return 0

def confirm_prompt(prompt="Are you sure?"):
    return Confirm.ask(f"[bold {AC()}]{prompt}[/bold {AC()}]")

# ====== DECORATIONS ======
def separator(style=None, char="─"):
    if style is None: style = BC()
    console.print(Rule(style=style, characters=char))

def small_title(text, style=None):
    if style is None: style = f"bold {PC()}"
    if _HAS_PYGFIGLET:
        try:
            banner = pyfiglet.figlet_format(str(text), font="small")
            console.print(f"[{style}]{banner}[/{style}]")
            return
        except:
            pass
    console.print(f"[{style}]{text}[/{style}]")

def zone_header(zone_name, description, border=None):
    if border is None: border = BC()
    if _HAS_PYGFIGLET:
        try:
            banner = pyfiglet.figlet_format(zone_name, font="small")
            content = f"[bold {PC()}]{banner}[/bold {PC()}]\n[{C('text')}]{description}[/{C('text')}]"
        except:
            content = f"[bold {PC()}]{zone_name}[/bold {PC()}]\n[{C('text')}]{description}[/{C('text')}]"
    else:
        content = f"[bold {PC()}]{zone_name}[/bold {PC()}]\n[{C('text')}]{description}[/{C('text')}]"
    panel = Panel(
        Align.center(content),
        border_style=border,
        box=box.DOUBLE,
        padding=(1, 2)
    )
    console.print(panel)

def item_style(item):
    cls = item.get("Class", "")
    if cls == "Weapon": return C("weapon", "bold red")
    elif cls in ("Helmet","Chestplate","Leggings","Boots","Shield"): return C("armor", "bold blue")
    elif "Potion" in cls: return C("potion", "bold green")
    elif cls == "Rune": return C("magic", "bold magenta")
    elif cls == "Scroll": return C("accent", "bold yellow")
    elif cls == "Artifact": return C("legendary", "bold yellow")
    return "bold white"
