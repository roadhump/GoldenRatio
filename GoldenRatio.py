import sublime
import sublime_plugin

XMIN, YMIN, XMAX, YMAX = range(4)
GOLDEN_RATIO = 1.618


class GoldenRatioCommand(sublime_plugin.WindowCommand):

    def run(self):
        self.resize_to_golden_ratio()

    def get_layout(self):
        layout = self.window.get_layout()
        #print layout
        cells = layout["cells"]
        rows = layout["rows"]
        cols = layout["cols"]
        return rows, cols, cells

    def resize_to_golden_ratio(self):
        window = self.window
        view = window.active_view()
        rows, cols, cells = self.get_layout()
        current_group = window.active_group()

        current_cell = cells[current_group]
        # print(cols)
        colnum = len(cols) - 1
        if colnum > 1:
            colspan = (current_cell[XMAX] - current_cell[XMIN])
            other_width = dest_width = 1 / GOLDEN_RATIO / colspan

            other_width = (1 - 1 / GOLDEN_RATIO) / (colnum - colspan)

            v = 0.0
            i = 0
            for col in cols:
                cols[i] = v

                if i >= current_cell[XMIN] and i < current_cell[XMAX]:
                    v = v + dest_width
                else:
                    v = v + other_width
                i = i + 1

        rownum = len(rows) - 1
        if rownum > 1:
            rowspan = (current_cell[YMAX] - current_cell[YMIN])
            other_height = dest_height = 1 / GOLDEN_RATIO / rowspan

            other_height = (1 - 1 / GOLDEN_RATIO) / (rownum - rowspan)

            v = 0.0
            i = 0
            for row in rows:
                rows[i] = v

                if i >= current_cell[YMIN] and i < current_cell[YMAX]:
                    v = v + dest_height
                else:
                    v = v + other_height
                i = i + 1

        layout = {"cols": cols, "rows": rows, "cells": cells}
        #print layout
        window.set_layout(layout)


class GoldenRatioAutoRun(sublime_plugin.EventListener):
    def on_activated(self, view):
        window = sublime.active_window()
        auto_resize = sublime.load_settings('GoldenRatio.sublime-settings').get('auto_resize')
        if auto_resize:
            window.run_command('golden_ratio')
