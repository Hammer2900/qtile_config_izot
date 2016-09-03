import libqtile.hook
 2
 3
 4 class ScratchPad(object):
 5     def __init__(self, app, match, qtile, position='top',
 6                  height=None, width=None):
 7         self.app = app
 8         self.client = None
 9         self.qtile = qtile
10         self.match = match
11         self.position = position
12
13         self.height = height
14         self.width = width
15
16         self.x = self.y = 0
17         self.height = height
18         self.width = width
19
20         libqtile.hook.subscribe.client_new(self.manage)
21         libqtile.hook.subscribe.setgroup(self.setgroup)
22
23     def _set_position(self):
24         if self.height is None:
25             self.height = (self.qtile.currentScreen.height / 100) * 70
26         if self.width is None:
27             self.width = (self.qtile.currentScreen.width/100) * 98
28
29         if self.position == 'top':
30             self.x = self.y = 0
31         elif self.position == 'bottom':
32             self.x = 0
33             self.y = self.height - self.qtile.currentScreen.height
34         elif self.position == 'center':
35             self.x = self.qtile.currentScreen.width/2 - self.width/2
36             self.y = self.qtile.currentScreen.height/2 - self.height/2
37
38     def manage(self, client):
39         if self.match.compare(client):
40             libqtile.hook.unsubscribe.client_new(self.manage)
41             self.client = client
42             self._set_client()
43
44     def _set_client(self):
45         self.client.defunct = True
46         self.client.floating = True
47         self._set_position()
48         self.client.place(self.x, self.y, self.width, self.height, 0, 0)
49         self.client.togroup(self.qtile.currentGroup.name)
50         if self.client.group:
51             self.client.group.focus(self.client, False)
52
53     def setgroup(self):
54         if self.client and not self.client.minimized:
55             self._set_client()
56
57     def toggle(self, qtile):
58         if not self.client:
59             libqtile.hook.subscribe.client_new(self.manage)
60             qtile.cmd_spawn(self.app)
61         else:
62             self.client.toggleminimize()
63             if not self.client.minimized:
64                 self._set_client()