import wx

from mine_generator import generate_mine_map


class MineSweeperDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="Mine Sweeper", pos=wx.DefaultPosition,
                           size=wx.Size(1000, 600), style=wx.DEFAULT_DIALOG_STYLE)
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self._mine_width = 30
        self._mine_height = 16
        self._mines_num = 99
        self._revealed_mines = 0
        self._mines = {}
        self._revealed_area = {}
        self._init = False
        bSizer = wx.BoxSizer(wx.VERTICAL)
        headSizer = wx.BoxSizer(wx.HORIZONTAL)
        self._resolveButton = wx.Button(self, wx.ID_ANY, u"DO", wx.DefaultPosition, wx.Size(64, 16))
        self._resolveButton.Bind(wx.EVT_BUTTON, self.onResolve)
        headSizer.Add(self._resolveButton, 0, wx.ALL, 5)
        self._mineInfoText = wx.StaticText(self, wx.ID_ANY, self.mineInfo(), wx.DefaultPosition, wx.DefaultSize,
                                           wx.ALIGN_RIGHT)
        headSizer.Add(self._mineInfoText, 0, wx.ALL | wx.EXPAND, 5)
        bSizer.Add(headSizer, 0, wx.ALL | wx.EXPAND, 5)

        gridSizer = wx.GridSizer(self._mine_height, self._mine_width, 2, 2)
        self._mine_buttons = {}
        for y in range(self._mine_height):
            for x in range(self._mine_width):
                button = wx.Button(self, wx.ID_ANY, "", wx.DefaultPosition, wx.Size(32, 32), name="%d:%d" % (x, y))
                button.SetBackgroundColour(wx.Colour(224, 224, 224))
                self._mine_buttons[(x, y)] = button
                button.Bind(wx.EVT_BUTTON, self.onClick)
                gridSizer.Add(button)
        bSizer.Add(gridSizer, 0, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(bSizer)
        self.Center(wx.BOTH)
        self.Bind(wx.EVT_CLOSE, self.onClose)

    def mineInfo(self):
        return u"%d/%d" % (self._revealed_mines, self._mines_num)

    def onClose(self, event):
        self.Destroy()

    def onClick(self, event):
        button = event.GetEventObject()
        name = button.GetName()
        x, y = [int(i) for i in name.split(':')]
        if not self._init:
            mines, blank_area = generate_mine_map(self._mine_width, self._mine_height, self._mines_num, x, y, 9)
            self._mines = mines
            self._revealed_area = blank_area
            for p in self._mines.keys():
                self._mine_buttons[p].SetLabel(str(self._mines[p]))
            self.update()

    def update(self):
        for p in self._revealed_area:
            if self._mines[p] != 9:
                self._mine_buttons[p].SetBackgroundColour(wx.Colour(250, 250, 250))
            else:
                self._mine_buttons[p].SetBackgroundColour(wx.Colour(255, 0, 0))

    def setRevealedArea(self, area):
        for p in area:
            if p not in self._revealed_area:
                if self._mines[p] != 9:
                    self._mine_buttons[p].SetBackgroundColour(wx.Colour(250, 250, 250))
                else:
                    self._mine_buttons[p].SetBackgroundColour(wx.Colour(255, 0, 0))

    def onResolve(self, event):



def main():
    root = wx.App(0)
    dialog = MineSweeperDialog(parent=None)
    dialog.Show()
    root.MainLoop()


if __name__ == "__main__":
    main()
