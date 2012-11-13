import sublime
import sublime_plugin

XMIN, YMIN, XMAX, YMAX = range(4)


class PaneCommand(sublime_plugin.WindowCommand):

    def get_layout(self):
        layout = self.window.get_layout()
        cells = layout["cells"]
        rows = layout["rows"]
        cols = layout["cols"]
        return rows, cols, cells

    def _dim(self, dim_items, cur_cell_min, cur_cell_max, ratio):

        dimnum = len(dim_items) - 1
        span = (cur_cell_max - cur_cell_min)

        if dimnum > 1 and dimnum > span:

            dest_size = 1 / ratio / span
            other_size = (1 - 1 / ratio) / (dimnum - span)

            v = 0.0
            i = 0
            for item in dim_items:
                dim_items[i] = v

                if i >= cur_cell_min and i < cur_cell_max:
                    v = v + dest_size
                else:
                    v = v + other_size
                i = i + 1

        return dim_items

    def resize_to_golden_ratio(self):

        window = self.window
        view = window.active_view()
        rows, cols, cells = self.get_layout()
        current_group = window.active_group()

        current_cell = cells[current_group]

        ratio = sublime.load_settings('GoldenRatio.sublime-settings').get('golden_ratio')
        if ratio <= 1:
            ratio = 1.05

        cols = self._dim(cols, current_cell[XMIN], current_cell[XMAX], ratio)
        rows = self._dim(rows, current_cell[YMIN], current_cell[YMAX], ratio)

        layout = {"cols": cols, "rows": rows, "cells": cells}
        window.set_layout(layout)

    def auto_resize_toggle(self):

        setting = sublime.load_settings('GoldenRatio.sublime-settings').get('auto_resize')
        sublime.load_settings('GoldenRatio.sublime-settings').set('auto_resize', ('' if setting else True))


class GoldenRatioCommand(PaneCommand):
    def run(self):
        self.resize_to_golden_ratio()


class AutoResizeToggleCommand(PaneCommand):
    def run(self):
        self.auto_resize_toggle()


class GoldenRatioAutoRun(sublime_plugin.EventListener):
    def on_activated(self, view):
        window = sublime.active_window()
        auto_resize = sublime.load_settings('GoldenRatio.sublime-settings').get('auto_resize')
        if auto_resize:
            window.run_command('golden_ratio')
