from typing import List
import matplotlib.pyplot as plt

"""For layout of matplotlib plots
"""


def bisect(
    layout: List[float],
    direction="vert",
    offset=0.5,
    spacing=0.05,
    absolute_spacing=False,
):
    x = layout[0]
    y = layout[1]
    width = layout[2]
    height = layout[3]

    if direction != "vert":
        # horizontal bisect
        if not absolute_spacing:
            spacing = spacing * height
        return [x, y, width, height * offset - spacing / 2], [
            x,
            y + height * offset + (spacing / 2),
            width,
            height * (1 - offset) - (spacing / 2),
        ]
    else:
        # vertical bisect
        if not absolute_spacing:
            spacing = spacing * width
        return [x, y, width * offset - spacing / 2, height], [
            x + width * offset + (spacing / 2),
            y,
            width * (1 - offset) - spacing / 2,
            height,
        ]


def margin(layout: List[float], w=0.1):
    x = layout[0]
    y = layout[1]
    width = layout[2]
    height = layout[3]
    return [x + w, y + w, width - w, height - w]


if __name__ == "__main__":

    def layout_basic():
        fig = plt.figure(figsize=(total_size_x, total_size_y))

        master_left, master_right = bisect(
            [0, 0, 1, 1],
            direction="vert",
            offset=0.5,
            spacing=divider_width,
            absolute_spacing=True,
        )

        left, bulk = bisect(master_left, direction="vert", offset=0.15, spacing=0.07)
        _, left = bisect(left, direction="horiz", offset=0.15, spacing=0.07)
        bottom, image = bisect(bulk, direction="horiz", offset=0.15, spacing=0.07)

        bottom_right, top_right = bisect(
            master_right, direction="horiz", offset=0.6, spacing=0.14
        )

        ax_left_bar = fig.add_axes(left)
        ax_bottom_bar = fig.add_axes(bottom)
        ax_main = fig.add_axes(image, sharex=ax_bottom_bar, sharey=ax_left_bar)

        ax_diagonal = fig.add_axes(top_right)
        ax_hist = fig.add_axes(bottom_right)
