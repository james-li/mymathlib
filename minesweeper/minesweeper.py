import wx

from mine_generator import generate_mine_map, neighbor_area, BoomException, get_common_neighbor


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
        self._clear_area = {}
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
        updated = False
        for p in area:
            if p not in self._revealed_area:
                updated = True
                if self._mines[p] != 9:
                    self._mine_buttons[p].SetBackgroundColour(wx.Colour(250, 250, 250))
                else:
                    self._mine_buttons[p].SetBackgroundColour(wx.Colour(255, 0, 0))
        if updated:
            self._mineInfoText.SetLabel(self.mineInfo())
            self._revealed_area = area.copy()
        return updated

    def onResolve(self, event):
        area = self._simpleResolve()
        if not area:
            area = self._complexResolve()
        if area:
            self.setRevealedArea(area)

    def _simpleResolve(self):
        revealed_area = self._revealed_area.copy()
        mines = self._mines
        updated = False
        for p in list(revealed_area.keys()):
            if p in self._clear_area.keys():
                continue
            mine_number = revealed_area[p]
            revealed_mines = 0
            if mine_number == 9:
                self._clear_area[p] = 9
                continue
            x, y = p
            neighbor = neighbor_area(x, y, self._mine_width, self._mine_height)
            i_lst = []
            for _pos in neighbor:
                pos = tuple(_pos)
                if pos not in revealed_area:
                    i_lst.append(pos)
                elif revealed_area[pos] == 9:
                    revealed_mines += 1
            if (mine_number - revealed_mines) == len(i_lst):
                # dig mine
                for mine in i_lst:
                    revealed_area[mine] = 9
                    revealed_mines += 1
                    self._revealed_mines += 1
                    updated = True
                # reveal safe area
            if mine_number == revealed_mines:
                for _pos in neighbor:
                    pos = tuple(_pos)
                    if pos not in revealed_area:
                        if mines[pos] == 9:
                            raise BoomException("Boom!!!!!")
                        revealed_area[pos] = mines[pos]
                        updated = True
                self._clear_area[p] = mine_number
            if updated:
                return revealed_area
        return None

        ## TODO: 比较相邻两个位置，标识

    def _complexResolve(self):
        revealed_area = self._revealed_area.copy()
        mines = self._mines
        updated = False
        p_lst = []
        for p1 in list(revealed_area.keys()):
            if p1 in self._clear_area:
                continue
            p_lst.append(p1)
            p1_neighbor = neighbor_area(p1[0], p1[1], self._mine_width, self._mine_height)
            for p2 in list(revealed_area.keys()):
                if p2 in p_lst or p2 in self._clear_area:
                    continue
                p2_neighbor = neighbor_area(p2[0], p2[1], self._mine_width, self._mine_height)
                common_neighbor = get_common_neighbor(p1_neighbor, p2_neighbor)
                if not common_neighbor:
                    continue
                    
        return None


def main():
    root = wx.App(0)
    dialog = MineSweeperDialog(parent=None)
    dialog.Show()
    root.MainLoop()


if __name__ == "__main__":
    main()
