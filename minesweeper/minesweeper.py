import time
import traceback

import wx

from mine_generator import mine_generator, BoomException


class MineSweeperDialog(wx.Dialog):
    def __init__(self, parent, mine_width=30, mine_height=16, mine_number=99):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title="Mine Sweeper", pos=wx.DefaultPosition,
                           size=wx.Size(1000, 600), style=wx.DEFAULT_DIALOG_STYLE)
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self._mine_generator = None
        self._mine_width = mine_width
        self._mine_height = mine_height
        self._mine_number = mine_number
        self._revealed_area = {}
        bSizer = wx.BoxSizer(wx.VERTICAL)
        headSizer = wx.BoxSizer(wx.HORIZONTAL)
        self._resolveButton = wx.Button(self, wx.ID_ANY, u"Dig", wx.DefaultPosition, wx.Size(64, 32))
        self._resolveButton.Bind(wx.EVT_BUTTON, self.onResolve)
        headSizer.Add(self._resolveButton, 0, wx.ALL, 5)
        self._refreshButton = wx.Button(self, wx.ID_ANY, u"Try Again", wx.DefaultPosition, wx.Size(64, 32))
        self._refreshButton.Bind(wx.EVT_BUTTON, self.onTryAgain)
        headSizer.Add(self._refreshButton, 0, wx.ALL, 5)
        self._mineInfoText = wx.StaticText(self, wx.ID_ANY, self.mineInfo(), wx.DefaultPosition, wx.Size(600, 32),
                                           wx.ALIGN_RIGHT | wx.ALIGN_CENTRE_VERTICAL)
        headSizer.Add(self._mineInfoText, -1, wx.ALL | wx.EXPAND, 5)
        bSizer.Add(headSizer, 0, wx.ALL | wx.EXPAND, 5)

        gridSizer = wx.GridSizer(self._mine_height + 1, self._mine_width + 1, 2, 2)
        self._mine_buttons = {}
        for y in range(self._mine_height + 1):
            for x in range(self._mine_width + 1):
                if x == 0 and y == 0:
                    button = wx.StaticText(self, wx.ID_ANY, "", wx.DefaultPosition, wx.Size(32, 32), 0)
                elif y == 0:
                    button = wx.StaticText(self, wx.ID_ANY, "%d" % (x - 1), wx.DefaultPosition, wx.Size(32, 32),
                                           wx.ALIGN_CENTRE)
                elif x == 0:
                    button = wx.StaticText(self, wx.ID_ANY, "%d" % (y - 1), wx.DefaultPosition, wx.Size(32, 32),
                                           wx.ALIGN_CENTRE)
                else:
                    button = wx.Button(self, wx.ID_ANY, "", wx.DefaultPosition, wx.Size(32, 32), name="%d:%d" % (x, y))
                    self._mine_buttons[(x - 1, y - 1)] = button
                    button.SetBackgroundColour(wx.Colour(224, 224, 224))
                    button.Bind(wx.EVT_BUTTON, self.onClick)
                gridSizer.Add(button)
        bSizer.Add(gridSizer, 0, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(bSizer)
        self.Center(wx.BOTH)
        self.Bind(wx.EVT_CLOSE, self.onClose)

    def mineInfo(self):
        if not self._mine_generator:
            return u"0/%d" % self._mine_number
        else:
            return self._mine_generator.get_mine_info()

    def onClose(self, event):
        self.Destroy()

    def onTryAgain(self, event):
        self._mine_generator = None
        self._revealed_area = None
        for button in self._mine_buttons.values():
            button.SetLabel("")
            button.SetBackgroundColour(wx.Colour(224, 224, 224))

    def onClick(self, event):
        button = event.GetEventObject()
        name = button.GetName()
        x, y = [int(i) for i in name.split(':')]
        if not self._mine_generator:
            self._mine_generator = mine_generator(self._mine_width, self._mine_height, self._mine_number, x, y, 9)
            self._revealed_area = self._mine_generator.get_revealed_area().copy()
            for p in self._mine_generator.get_squares():
                self._mine_buttons[p].SetLabel(str(self._mine_generator.get_square_mines(p)))
            self.update()

    def update(self):
        self._mineInfoText.SetLabel(self.mineInfo())
        for p in self._revealed_area:
            if self._mine_generator.get_square_mines(p) != 9:
                self._mine_buttons[p].SetBackgroundColour(wx.Colour(250, 250, 250))
            else:
                self._mine_buttons[p].SetBackgroundColour(wx.Colour(255, 0, 0))

    def setRevealedArea(self, area):
        updated = False
        for p in area:
            if p not in self._revealed_area:
                updated = True
            if self._mine_generator.get_square_mines(p) != 9:
                self._mine_buttons[p].SetBackgroundColour(wx.Colour(250, 250, 250))
            else:
                self._mine_buttons[p].SetBackgroundColour(wx.Colour(255, 0, 0))
        if updated:
            self._mineInfoText.SetLabel(self.mineInfo())
            self._revealed_area = area.copy()
            if len(self._mine_generator.get_revealed_area()) == len(self._mine_generator.get_squares()):
                wx.MessageBox("Congratulations", "Info", wx.OK | wx.ICON_INFORMATION)
        return updated

    def onResolve(self, event):
        if not self._mine_generator or len(self._mine_generator.get_revealed_area()) == len(
                self._mine_generator.get_squares()):
            return
        try:
            while len(self._mine_generator.get_squares()) > len(self._mine_generator.get_revealed_area()):
                if self._mine_generator.simple_resolve() or self._mine_generator.combo_resolve():
                    self.setRevealedArea(self._mine_generator.get_revealed_area())
                else:
                    wx.MessageBox("No way out", "Info", wx.OK | wx.ICON_INFORMATION)
                    break
        except BoomException as e:
            traceback.print_exc()
            wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)


def main():
    root = wx.App(0)
    dialog = MineSweeperDialog(parent=None)
    dialog.Show()
    root.MainLoop()


if __name__ == "__main__":
    main()
