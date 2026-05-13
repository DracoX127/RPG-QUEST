import random
import time
import sys
import threading
import math
from typing import Optional, Dict, Any

from rich.text import Text
from rich.panel import Panel
from rich.align import Align
from rich.box import HEAVY, DOUBLE
from rich.console import Group

from ui import console, clear, section, announcement, _HAS_PYGFIGLET
from settings import SETTINGS

try:
    import pyfiglet
except ImportError:
    pyfiglet = None

# ============================================================
#  ANIMATION GATE
# ============================================================
def _anim_enabled(effect_type: str = "particles") -> bool:
    """Check if a specific animation type is enabled based on settings."""
    level = SETTINGS.get_anim()
    if effect_type == "shake":
        return level.get("shake", False) and SETTINGS.get("screen_shake", True)
    if effect_type == "particles":
        return level.get("particles", False) and SETTINGS.get("show_particles", True)
    if effect_type == "flash":
        return level.get("flash", False) and SETTINGS.get("screen_flash", True)
    if effect_type == "cinematic":
        return level.get("cinematic", False)
    if effect_type == "transition":
        return level.get("transition", 0) > 0
    return True

def _trans_delay() -> float:
    return SETTINGS.get_anim().get("transition", 0.2)

def _maybe_do(func, *args, effect_type="particles", **kwargs):
    if _anim_enabled(effect_type):
        return func(*args, **kwargs)

# ============================================================
#  SCREEN EFFECTS
# ============================================================

def shake_screen(intensity: int = 3, duration: float = 0.3) -> None:
    if not _anim_enabled("shake"): return
    """Simulate screen shake by printing blank lines with offset."""
    end = time.time() + duration
    while time.time() < end:
        offset = random.randint(0, intensity)
        sys.stdout.write("\n" * offset + " " * random.randint(0, intensity // 2))
        sys.stdout.flush()
        time.sleep(0.05)
    sys.stdout.write("\033[K")
    sys.stdout.flush()

def flash_screen(color: str = "red", duration: float = 0.15) -> None:
    if not _anim_enabled("flash"): return
    """Full screen color flash."""
    style = f"bold {color} on white" if color else "bold white on red"
    flash = Panel(
        Align.center(f"[{style}]⚡[/{style}]"),
        style=f"on {color}" if color else "on red",
        box=HEAVY,
        padding=(5, 20)
    )
    console.print(flash)
    time.sleep(duration)
    clear()

def cinematic_bars(duration: float = 1.0, text: str = "") -> None:
    """Letterbox cinematic bars with optional text."""
    bar = "▄" * console.width if hasattr(console, 'width') else "▄" * 80
    top = Panel(
        Align.center(f"[bold white]{text}[/bold white]") if text else "",
        style="on black",
        box=DOUBLE,
        padding=(2, 2)
    )
    console.print(top)
    time.sleep(duration)
    clear()

def pulse_text(text: str, style: str = "bold red", pulses: int = 3) -> None:
    """Text that pulses (appears and fades)."""
    for i in range(pulses):
        intensity = (i + 1) / pulses
        console.print(f"[{style}]{' ' * int((1-intensity)*5)}{text}[/{style}]")
        time.sleep(0.12 * intensity)
    console.print()

def rainbow_text(text: str, delay: float = 0.05) -> None:
    """Text that cycles through rainbow colors character by character."""
    colors = ["red", "yellow", "green", "cyan", "blue", "magenta", "red"]
    for i, char in enumerate(str(text)):
        color = colors[i % len(colors)]
        console.print(f"[bold {color}]{char}[/bold {color}]", end="")
        sys.stdout.flush()
        time.sleep(delay)
    console.print()

def glitch_text(text: str, style: str = "bold green on black", glitch_chance: float = 0.2) -> None:
    """Text that occasionally glitches with random characters."""
    import string
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    result = []
    for char in str(text):
        if random.random() < glitch_chance:
            result.append(random.choice(chars))
        else:
            result.append(char)
    console.print(f"[{style}]{''.join(result)}[/{style}]")

# ============================================================
#  PARTICLE SYSTEM
# ============================================================

_PARTICLES = ["✦", "✧", "★", "☆", "•", "·", "⚡", "🔥", "💥", "✨", "💫", "⭐"]

def burst_particles(count: int = 10, style: str = "bold yellow", width: int = 40) -> None:
    if not _anim_enabled("particles"): return
    """Burst of particles at random positions."""
    lines = []
    for _ in range(count):
        x = random.randint(0, width)
        particle = random.choice(_PARTICLES)
        line = " " * x + f"[{style}]{particle}[/{style}]"
        lines.append(line)
    for line in lines:
        console.print(line)
        time.sleep(0.03)
    time.sleep(0.2)

def sparkle_line(text: str, style: str = "bold white") -> None:
    """Print text with sparkle particles around it."""
    sparkle = random.choice(["✦", "✧", "✨"])
    console.print(f"[{style}]{sparkle} {text} {sparkle}[/{style}]")

def damage_popup(amount: int, is_crit: bool = False) -> None:
    """Floating damage number effect."""
    style = "bold yellow on red" if is_crit else "bold red"
    prefix = "💥 " if is_crit else ""
    console.print(f"[{style}]{prefix}{amount}[/{style}]")
    time.sleep(0.1)

# ============================================================
#  TRANSITIONS
# ============================================================

def fade_to_black(duration: float = 0.5) -> None:
    """Gradual fade to black."""
    steps = 10
    for i in range(steps):
        alpha = i / steps
        if i == steps - 1:
            clear()
        else:
            print()
        time.sleep(duration / steps)

def scan_line(text: str, style: str = "bold cyan") -> None:
    """Text that appears character by character like a scan."""
    for char in str(text):
        console.print(f"[{style}]{char}[/{style}]", end="")
        sys.stdout.flush()
        time.sleep(0.02)
    console.print()

# ============================================================
#  ANIMATED BORDERS
# ============================================================

def animated_box(content: str, title: str = "", style: str = "bold yellow") -> None:
    """Content inside an animated pulsing box."""
    box = Panel(
        Align.center(f"[{style}]{content}[/{style}]"),
        title=f"[bold white]{title}[/bold white]",
        border_style="bright_yellow",
        box=DOUBLE,
        padding=(1, 2)
    )
    console.print(box)

def scrolling_banner(text: str, width: int = 40) -> None:
    """Scroll text horizontally like a news ticker."""
    text = f"  {text}  "
    for offset in range(len(text) + width):
        display = ""
        for i in range(width):
            idx = (offset + i) % len(text)
            display += text[idx]
        console.print(f"[bold cyan]{display}[/bold cyan]", end="\r")
        sys.stdout.flush()
        time.sleep(0.08)

# ============================================================
#  DIALOGUE SYSTEM
# ============================================================

_VOICES = {
    "narrator": "bold white",
    "warrior": "bold red",
    "mage": "bold blue",
    "rogue": "bold green",
    "merchant": "bold yellow",
    "boss": "bold red on black",
    "whisper": "dim italic cyan",
    "shout": "bold yellow on red",
    "mystic": "bold magenta",
    "drunk": "italic yellow",
}

def dialogue(text: str, speaker: str = "narrator", delay: float = 0.03) -> None:
    """NPC dialogue with speaker-specific color."""
    style = _VOICES.get(speaker, "bold white")
    speaker_tag = f"[{style}][{speaker.upper()}][/{style}]"
    console.print(f"{speaker_tag} ", end="")
    for char in str(text):
        console.print(f"[{style}]{char}[/{style}]", end="")
        sys.stdout.flush()
        time.sleep(delay * random.uniform(0.8, 1.2))
    console.print()

def voice_say(text: str, voice: str = "narrator") -> None:
    """Quick dialogue with no typewriter effect."""
    style = _VOICES.get(voice, "bold white")
    tag = f"[dim][{voice.upper()}][/dim] "
    console.print(f"{tag}[{style}]{text}[/{style}]")

# ============================================================
#  CINEMATIC COMBAT EFFECTS
# ============================================================

def battle_intro(enemy_name: str) -> None:
    if not _anim_enabled("cinematic"): return
    """Cinematic battle intro sequence."""
    clear()
    flash_screen("red", 0.1)
    time.sleep(0.1)
    if pyfiglet:
        banner = pyfiglet.figlet_format("BATTLE!", font="banner")
        animated_box(banner, "⚔ ENEMY ENCOUNTER ⚔")
    else:
        animated_box("⚔ BATTLE! ⚔", enemy_name)
    time.sleep(0.5)
    burst_particles(8, "bold red")
    time.sleep(0.3)

def victory_fanfare() -> None:
    if not _anim_enabled("cinematic"): return
    """Victory fanfare effect."""
    clear()
    burst_particles(15, "bold yellow")
    if pyfiglet:
        banner = pyfiglet.figlet_format("VICTORY", font="banner")
        animated_box(banner, "🏆 YOU WIN 🏆", style="bold yellow on green")
    else:
        animated_box("🏆 VICTORY 🏆", style="bold yellow on green")
    shake_screen(2, 0.2)
    burst_particles(10, "bold green")

def level_up_effect(lvl: int) -> None:
    if not _anim_enabled("cinematic"): return
    """Level up celebration effect."""
    time.sleep(0.2)
    flash_screen("yellow", 0.1)
    rainbow_text(f"★ LEVEL UP! ★  You are now level {lvl}!")
    burst_particles(12, "bold cyan")
    time.sleep(0.3)

def loot_popup(items: list) -> None:
    """Dramatic loot display."""
    console.print()
    for item in items:
        rainbow_text(f"✦ LOOT: {item} ✦")
        time.sleep(0.1)

# ============================================================
#  HP BAR ANIMATION
# ============================================================

def animate_hp_change(
    current: float,
    target: float,
    maximum: float,
    label: str = "HP",
    width: int = 15,
    duration: float = 0.5
) -> None:
    """Smooth HP bar change animation."""
    steps = max(3, int(duration / 0.05))
    for i in range(steps + 1):
        t = i / steps
        eased = t * t * (3 - 2 * t) if t < 0.5 else 1 - (1 - t) * (1 - t) * (3 - 2 * (1 - t))
        interpolated = current + (target - current) * eased
        ratio = interpolated / maximum if maximum > 0 else 0
        filled = int(ratio * width)
        empty = max(0, width - filled)
        if ratio > 0.6:
            color = "green"
        elif ratio > 0.3:
            color = "yellow"
        else:
            color = "red"
        bar = f"[{color}]{'█' * filled}[/{color}][dim]{'░' * empty}[/dim]"
        sys.stdout.write(f"\r{label}: {bar} {int(interpolated)}/{int(maximum)}  ")
        sys.stdout.flush()
        time.sleep(0.05)
    console.print()

# ============================================================
#  SCREEN TITLE
# ============================================================

def screen_title(title: str, subtitle: str = "", style: str = "bold cyan") -> None:
    """Full-screen title display with subtitle."""
    clear()
    if pyfiglet:
        try:
            banner = pyfiglet.figlet_format(title, font="big")
            console.print(f"[{style}]{banner}[/{style}]")
        except:
            console.print(f"[{style}]{'='*60}[/{style}]")
            console.print(f"[{style}]{title.center(60)}[/{style}]")
            console.print(f"[{style}]{'='*60}[/{style}]")
    else:
        console.print(f"[{style}]{'='*60}[/{style}]")
        console.print(f"[{style}]{title.center(60)}[/{style}]")
        console.print(f"[{style}]{'='*60}[/{style}]")
    if subtitle:
        console.print(f"\n[bold white]{subtitle}[/bold white]")
    time.sleep(0.5)

# ============================================================
#  AMBIENT EFFECTS
# ============================================================

def rain_effect(seconds: float = 2.0, width: int = 40) -> None:
    """ASCII rain effect."""
    drops = ".,*:;!?"
    end = time.time() + seconds
    while time.time() < end:
        line = "".join(random.choice(drops) if random.random() < 0.3 else " " for _ in range(width))
        console.print(f"[dim cyan]{line}[/dim cyan]")
        time.sleep(0.08)

def fireflies_effect(seconds: float = 2.0, width: int = 40) -> None:
    """Floating firefly particles."""
    chars = "·.✧✦"
    end = time.time() + seconds
    last_line = ""
    while time.time() < end:
        line = ""
        for _ in range(width):
            if random.random() < 0.05:
                line += random.choice(chars)
            else:
                line += " "
        if line.strip():
            console.print(f"[dim yellow]{line}[/dim yellow]")
        else:
            console.print()
        time.sleep(0.15)

# ============================================================
#  PROGRESS ANIMATION
# ============================================================

def animated_loading(text: str = "Loading", duration: float = 1.5) -> None:
    """Animated loading dots."""
    end = time.time() + duration
    dots = 0
    while time.time() < end:
        dots = (dots % 6) + 1
        sys.stdout.write(f"\r[bold cyan]{text}{'.' * dots}{' ' * (6-dots)}[/bold cyan]")
        sys.stdout.flush()
        time.sleep(0.15)
    console.print()

# ============================================================
#  BOSS ENTRANCE
# ============================================================

def boss_entrance(boss_name: str) -> None:
    if not _anim_enabled("cinematic"): return
    """Dramatic boss entrance sequence."""
    clear()
    flash_screen("red", 0.3)
    time.sleep(0.1)
    clear()
    if pyfiglet:
        banner = pyfiglet.figlet_format(boss_name, font="bloody")
        console.print(f"[bold red]{banner}[/bold red]")
    else:
        console.print(f"[bold red on black]{'BOSS'.center(60)}[/bold red on black]")
        console.print(f"[bold red]{boss_name.center(60)}[/bold red]")
    time.sleep(0.3)
    shake_screen(5, 0.5)
    burst_particles(20, "bold red")
    dialogue("YOU DARE CHALLENGE ME?", "boss", 0.06)
    time.sleep(0.3)
    clear()
