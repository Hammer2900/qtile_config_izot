from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget

mod = "mod4"

keys = [
    # Switch between windows in current stack pane
    Key(
        [mod], "k",
        lazy.layout.down()
    ),
    Key(
        [mod], "j",
        lazy.layout.up()
    ),

    # Move windows up or down in current stack
    Key(
        [mod, "control"], "k",
        lazy.layout.shuffle_down()
    ),
    Key(
        [mod, "control"], "j",
        lazy.layout.shuffle_up()
    ),

    # Switch window focus to other pane(s) of stack
    Key(
        [mod], "space",
        lazy.layout.next()
    ),

    # Swap panes of split stack
    Key(
        [mod, "shift"], "space",
        lazy.layout.rotate()
    ),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"], "Return",
        lazy.layout.toggle_split()
    ),
    Key([mod], "Return", lazy.spawn("sakura")),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "w", lazy.window.kill()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),
]

groups = [
    Group('browser'),
    Group('term'),
    Group('fm'),
    Group('skype'),
    Group('pycharm'),
    Group('6'),
    Group('7'),
    Group('8'),
    Group('9'),
]

for index, grp in enumerate(groups):
    keys.extend([

        # switch to group
        Key([mod], str(index + 1), lazy.group[grp.name].toscreen()),

        # send to group
        Key([mod, "shift"], str(index + 1), lazy.window.togroup(grp.name)),

        # swap with group
        Key([mod, "shift"], str(index + 1), lazy.group.swap_groups(grp.name))
    ])

layouts = [
    layout.Max(),
    layout.Stack(stacks=2),
    layout.Tile(ratio=0.25),
]

widget_defaults = dict(
    font='ttf-droid',
    fontsize=14,
    padding=5,
)

default_data = dict(fontsize=12, foreground="FF6600", background="1D1D1D", font="ttf-droid")

screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.GroupBox(),
                widget.Prompt(),
                widget.Sep(),
                widget.Spacer(),
                widget.Sep(),
                # widget.BitcoinTicker(),
                # widget.LaunchBar(progs=[('thunderbird', 'thunderbird -safe-mode', 'launch thunderbird in safe mode')]),
                widget.KeyboardLayout(configured_keyboards=['us', 'ru']),
                widget.Volume(),
                # widget.TextBox("default config", name="default"),
                widget.Systray(),
                widget.Clock(format='%Y-%m-%d %I:%M'),
            ],
            30,
        ),
        top=bar.Bar(
            [
                widget.WindowName()
            ],
            30,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating()
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, github issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
