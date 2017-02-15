#!/usr/bin/env python3


import os.path
import urwid

from aft._template import restore_template

DOT = os.path.expanduser('~/.aft/')


class ItemList(urwid.ListBox):
    def __init__(self, ui, widgets, submenu=False):
        super().__init__(widgets)
        self._ui = ui
        self._submenu = submenu

    def keypress(self, size, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()
        if key == 'right':
            if self._submenu:
                self._ui.load_config(self.get_focus())
            else:
                self._ui.load_submenu(self.get_focus())
        if key == 'left' and self._submenu:
            self._ui.create_toplevel_widgets()
        if key == 'down':
            focus, index = self.get_focus()
            if index < len(self.body)-1:
                self.set_focus(index+1, 'above')
        if key == 'up':
            focus, index = self.get_focus()
            if index > 0:
                self.set_focus(index-1, 'below')
        return None


class UI:
    def __init__(self):
        self.directory = '{}templates'.format(DOT)
        self.widget = None
        self._group = None
        self.create_toplevel_widgets()

    def create_toplevel_widgets(self):
        title = urwid.Text(('focus', 'Groups:'))
        groups = os.listdir('{}templates'.format(DOT)) 
        groups = [urwid.AttrMap(urwid.Text(x), None, 'focus') for x in groups]
        walker = urwid.SimpleListWalker(groups)
        itemlist = ItemList(self, walker)

        title_filler = urwid.Filler(title, 'top')
        pile = urwid.Pile([(2, title_filler), ('weight', 1, itemlist)])
        if self.widget is None:
            self.widget = urwid.WidgetPlaceholder(pile)
        else:
            self.widget.original_widget = pile
        return None

    def load_submenu(self, focused):
        widget, index = focused
        groups = os.listdir('{}templates'.format(DOT))
        text = groups[index]
        self._group = text
        configs = os.listdir('{}templates/{}'.format(DOT, text))
        configs = [urwid.AttrMap(urwid.Text(x), None, 'focus') for x in configs
                   if x.endswith('.yaml') and not x.startswith('.')]
        title = urwid.Text(('focus', '{} configs:'.format(text)))
        walker = urwid.SimpleListWalker(configs)
        itemlist = ItemList(self, walker, True)
        title_filler = urwid.Filler(title, 'top')
        pile = urwid.Pile([(2, title_filler), ('weight', 1, itemlist)])
        self.widget.original_widget = pile
        return None

    def load_config(self, focused):
        widget, index = focused
        configs = [x for x in os.listdir('{}templates/{}'.format(DOT, self._group))
                   if x.endswith('.yaml') and not x.startswith('.')]
        config = configs[index].replace('.yaml', '')
        restore_template(self._group, config)
        return None

    
    def run(self):
        palette = [
                ('focus', 'bold', '')
                ]
        loop = urwid.MainLoop(self.widget, palette)
        loop.run()
        return None
