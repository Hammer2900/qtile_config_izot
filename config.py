from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook

import subprocess

mod = "mod4"
alt = "mod1"

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

    Key([mod], "F2", lazy.spawn("amixer --quiet set Master 1-")),
    Key([mod], "F3", lazy.spawn("amixer --quiet set Master 1+")),
    Key([mod, "shift"], "space", lazy.window.toggle_floating()),
    Key([mod], "q", lazy.window.kill()),
    Key([mod], "F5", lazy.spawn("sakura -e ranger")),
    Key([mod], "F6", lazy.spawn("pcmanfm")),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
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
                widget.GroupBox(**default_data),
                widget.Prompt(**default_data),
                widget.Sep(),
                widget.Spacer(),
                widget.Sep(),
                # widget.BitcoinTicker(),
                # widget.LaunchBar(progs=[('thunderbird', 'thunderbird -safe-mode', 'launch thunderbird in safe mode')]),
                widget.KeyboardLayout(configured_keyboards=['us', 'ru'], **default_data),
                widget.Volume(**default_data),
                # widget.TextBox("default config", name="default"),
                widget.Systray(**default_data),
                widget.Clock(format='%Y-%m-%d %I:%M', **default_data),
            ],
            30,
        ),
        top=bar.Bar(
            [
                widget.WindowName(**default_data)
            ],
            30,
        ),
    ),
]

group_app_dict = {
    'firefox-aurora': 'browser',
    'skype': 'skype'
}

@hook.subscribe.client_new
def dialogs(window):
    if window.window.get_wm_type() == 'dialog' or window.window.get_wm_transient_for():
        window.floating = True

    @hook.subscribe.client_new
    def grouper(window, windows={'firefox-aurora': 'browser', 'skype': 'skype', 'pcmanfm': 'fm', 'jetbrains-pycharm': 'pycharm'}):

        """
        This function relies on the contentious feature of default arguments
        where upon function definition if the argument is a mutable datatype,
        then you are able to mutate the data held within that object.
        Current usage:
        {window_name: group_name}
        or for grouping windows to different groups you will need to have a
        list under the window-key with the order that you're starting the
        apps in.
        See the 'runner()' function for an example of using this method.
        Here:
        {window_name: [group_name1, group_name2]}
        Window name can be found via window.window.get_wm_class()
        """

        windowtype = window.window.get_wm_class()[0]

        # if the window is in our map
        if windowtype in windows.keys():

            # opening terminal applications gives
            # the window title the same name, this
            # means that we need to treat these apps
            # differently

            if windowtype != 'urxvt':
                window.togroup(windows[windowtype])
                windows.pop(windowtype)

            # if it's not on our special list,
            # we send it to the group and pop
            # that entry out the map
            else:
                try:
                    window.togroup(windows[windowtype][0])
                    windows[windowtype].pop(0)
                except IndexError:
                    pass


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

@hook.subscribe.startup
def startup():
    # rc_dir = "/home/arkchar/.config/wmStartupScripts/"
    # subprocess.Popen("sleep 3".split())
    subprocess.Popen(['feh', '--bg-scale', '/home/izot/Downloads/Best-Beach-Wallpapers-Background-HD-Wallpaper.jpg'])
    subprocess.Popen(['skype'])
    # execute_once("synergys")
    # execute_once("xcompmgr")
    # execute_once(rc_dir + "xmodmap.py")
    # execute_once("ibus-daemon --xim")
    # execute_once("hsetroot -tile /home/arkchar/Pictures/desktop.jpg")
    # execute_once(rc_dir + "trackpoint.sh")
    # execute_once("xsetroot -cursor_name left_ptr")

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, github issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
