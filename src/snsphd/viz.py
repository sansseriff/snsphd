# import seaborn as sns
import numpy as np

# import os
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.path import Path
from matplotlib.patches import BoxStyle
from matplotlib.offsetbox import AnchoredText
import matplotlib
from typing import TYPE_CHECKING


def despine(ax, offset=2):
    if (type(ax) != np.ndarray) & (type(ax) != list):
        ax = [ax]
    for a in ax:
        a.spines["bottom"].set_position(("outward", offset))
        a.spines["left"].set_position(("outward", offset))


def color_palette(dark=False) -> tuple[dict, list]:
    """
    Returns my preferred color scheme
    """
    colors = {
        "dark_purple": "#5F2E88",
        "purple": "#9d71c7",
        "light_purple": "#c08df0",
        "pale_purple": "#dfd6e5",
        "dark_orange": "#F38227",
        "orange": "#E39943",
        "light_orange": "#EEBA7F",
        "pale_orange": "#f2d4b6",
        "dark_blue": "#3F60AC",
        "blue": "#7292C7",
        "light_blue": "#A5B3CC",
        "pale_blue": "#dae4f1",
        "dark_red": "#9C372F",
        "red": "#C76A6A",
        "light_red": "#E39C9D",
        "pale_red": "#edcccc",
        "dark_green": "#395A34",
        "green": "#688A2F",
        "light_green": "#B3CD86",
        "pale_green": "#d8e2c3",
        "dark_brown": "#764f2a",
        "brown": "#c2996c",
        "light_brown": "#e1bb96",
        "pale_brown": "#efccaf",
        "black": "#444147",
        "grey": "#EFEFEF",
        "gray": "#EFEFEF",
        "light_grey": "#6D6F72",
        "light_gray": "#6D6F72",
    }

    if dark:
        colors = {
            "light_purple": "#c08df0",
            "light_orange": "#EEBA7F",
            "light_blue": "#A5B3CC",
            "light_red": "#E39C9D",
            "light_green": "#B3CD86",
            "light_brown": "#e1bb96",
            "pale_brown": "#efccaf",
            "black": "#444147",
            "grey": "#EFEFEF",
            "gray": "#EFEFEF",
            "light_grey": "#6D6F72",
            "light_gray": "#6D6F72",
        }
    palette = [
        v
        for k, v in colors.items()
        if (v not in ["grey", "gray", "dark_purple", "light_grey"])
        and ("pale" not in [v])
    ]
    return colors, palette


def bokeh_basic():
    # because I always forget bokeh syntax
    print(
        "colors, swatches = viz.bokeh_theme()\n\
from bokeh.plotting import figure, show\n\
import numpy as np\n\
from bokeh.io import output_notebook\n\
output_notebook(hide_banner=True)\n\
p = figure(width=800, height=400, output_backend='webgl')\n\
p.line(x=np.arange(100), y=np.sin(np.arange(100)*.2), line_color=colors['black'], line_width=3, line_alpha=0.6)\n\
show(p)"
    )


def update_colors(dark=False):
    if not dark:
        plt.rcParams.update(
            {
                # "axes.facecolor": "#fafafa",
                "axes.facecolor": "#ffffff",
                "axes.edgecolor": "#333333",
                "axes.labelcolor": "#333333",
                "text.color": "#333333",
                "xtick.color": "#333333",
                "ytick.color": "#333333",
                "legend.edgecolor": "#333333",
                "figure.facecolor": "white",
                "grid.alpha": 0.3,
            }
        )
        colors, palette = color_palette()
    else:
        plt.rcParams.update(
            {
                "axes.facecolor": "#3d3f4f",
                "axes.edgecolor": "#dbdbdb",
                "axes.labelcolor": "#dbdbdb",
                "text.color": "#dbdbdb",
                "xtick.color": "#dbdbdb",
                "ytick.color": "#dbdbdb",
                "legend.edgecolor": "#dbdbdb",
                "figure.facecolor": "#2E303E",
                "grid.alpha": 0.3,
            }
        )
        colors, palette = color_palette(dark=True)
    # sns.set_palette(palette)
    return "done"


import copy
import matplotlib.colors as mcolors
import colorsys
import matplotlib.colors as mcolors
import math
import pickle
import io
import os
import traceback


def dark_alpha_converter(alpha):
    try:
        math.sqrt(math.sqrt(math.sqrt(alpha)))
    except Exception as e:
        # traceback.print_exc()
        return alpha


import colorsys
import matplotlib.colors as mcolors
from matplotlib.colors import ListedColormap


def plot_arrows(
    ax,
    start,
    end,
    color="red",
    arrowstyle="<->",
    alpha=1,
    lw=1,
    ls="-",
    label="",
    fontsize=12,
    arrowsize=10,
):
    ax.annotate(
        text="",
        xy=start,
        xytext=end,
        arrowprops=dict(
            color=color,
            alpha=alpha,
            lw=lw,
            ls=ls,
            shrinkA=0,
            shrinkB=0,
            patchA=None,
            patchB=None,
            arrowstyle=arrowstyle,
            mutation_scale=arrowsize,
        ),
        bbox=dict(pad=0),
    )
    center_x = (start[0] + end[0]) / 2
    center_y = (start[1] + end[1]) / 2
    if label != "":
        ax.annotate(
            label,
            xy=(center_x, center_y),
            color=color,
            alpha=alpha,
            xytext=(0, -1),
            fontsize=fontsize,
            textcoords="offset points",
            horizontalalignment="center",
            verticalalignment="top",
        )


def mix_with_white(hex_color, amount):
    # Convert hex color to RGB format
    rgb_color = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))

    # Mix with white by adding RGB values
    white_rgb = (255, 255, 255)
    mixed_rgb = tuple(
        int((1 - amount) * c + amount * w) for c, w in zip(rgb_color, white_rgb)
    )

    # Convert mixed RGB color back to hex format
    mixed_hex_color = "#{:02x}{:02x}{:02x}".format(*mixed_rgb)

    return mixed_hex_color


def saturation_response(x):
    # a somewhat filmic-like saturation response curve
    return (np.abs(-2.8 * (x - 0.38) ** 2 + 1)) ** 2


def rgb_color_saturation(rgb_color, saturation):
    hls_color = colorsys.rgb_to_hls(*rgb_color)
    saturation_adj = saturation_response(hls_color[1])
    # print("light: ", hls_color[1])
    # print(saturation_adj)
    hls_color = (hls_color[0], hls_color[1], hls_color[2] * saturation_adj)
    rgb_color = colorsys.hls_to_rgb(*hls_color)
    return rgb_color


def brighten_color(hex_color, min_lightness):
    # Convert hex color to RGB format
    # hex_representation_of_black = "#000000"
    if hex_color.upper() == "#000000":
        return "#B6BCCF"

    rgb_color = mcolors.to_rgb(hex_color)

    # Convert RGB color to HLS format and get lightness value
    hls_color = colorsys.rgb_to_hls(*rgb_color)
    lightness = hls_color[1]
    saturation = hls_color[2]

    # Check if lightness is below the minimum value
    if lightness < min_lightness:
        # Brighten the color by increasing the lightness value
        lightness_diff = min_lightness - lightness
        lightness = min(lightness + lightness_diff * 1.3, 1.0)
        rgb_color = colorsys.hls_to_rgb(hls_color[0], lightness, hls_color[2])

    # Convert RGB color back to hex format
    hex_color = mcolors.to_hex(rgb_color)

    # if it's a very saturated color, mix with white
    if (
        # hex_color.upper() == "#0000FF"
        # or hex_color.upper() == "#FF0000"
        # or hex_color.upper() == "#00FF00"
        saturation
        > 0.8
    ):
        # print(hex_color)
        # print(hls_color)
        # print(get_color_value(hex_color))
        hex_color = mix_with_white(hex_color[1:].upper(), 0.5)

    return hex_color


def lift_gamma_gain(rgb_color, lift, gamma, gain):
    return (gain * (rgb_color + lift * (1 - rgb_color))) ** (1 / gamma)


def manage_lines(lines_list, override_alpha=False):
    for line in lines_list:
        c = line.get_color()
        # a = line.get_alpha()
        c_b = mcolors.to_rgba(brighten_color(mcolors.to_hex(c), 0.5), 1)
        line.set_color(c_b)
        if not override_alpha:
            line.set_alpha(dark_alpha_converter(line.get_alpha()))
        # line.set_color('w')
        # print("color: ", c)


def handle_legend_errbars(children, max_depth, depth=0, override_alpha=False):
    if depth >= max_depth:
        for child in children:
            # print(child)
            if isinstance(child, matplotlib.collections.LineCollection):
                # print(child.get_color())
                child.set_color(
                    mcolors.to_rgb(
                        brighten_color(mcolors.to_hex(child.get_color()), 0.5)
                    )
                )
                if not override_alpha:
                    child.set_alpha(dark_alpha_converter(child.get_alpha()))

            if isinstance(child, matplotlib.lines.Line2D):
                # print(child.get_color())
                child.set_color(
                    mcolors.to_rgb(
                        brighten_color(mcolors.to_hex(child.get_color()), 0.5)
                    )
                )
                if not override_alpha:
                    child.set_alpha(dark_alpha_converter(child.get_alpha()))
        return
    for child in children:
        handle_legend_errbars(
            child.get_children(), max_depth, depth + 1, override_alpha=override_alpha
        )


# from matplotlib.patches


def custom_cmap(lift: float = 0.1, gamma: float = 1, gain: float = 1) -> ListedColormap:
    cmap1 = plt.cm.plasma
    cmap2 = plt.cm.inferno
    n = 256
    colors1 = cmap1(np.linspace(0.0, 1, n))
    colors2 = cmap2(np.linspace(0, 1, n))
    colors = np.zeros((n, 4))
    colors[:, :3] = 0.4 * colors1[:, :3] + 0.6 * colors2[:, :3]  # / 2
    colors[:, 3] = 0.4 * colors1[:, 3] + 0.6 * colors2[:, 3]  # / 2

    for i in range(len(colors)):
        colors[i][:3] = rgb_color_saturation(colors[i][:3], 0.75)
        colors[i][:3] = lift_gamma_gain(colors[i][:3], lift, gamma, gain)

    mixed_cmap = ListedColormap(colors)
    return mixed_cmap


def save_light_dark_all(
    fig: plt.Figure | None = None,
    name: str = "figure",
    loc: str = "./",
    override_alpha: bool = False,
    override_cmap: bool = False,
    custom_map: bool | ListedColormap = None,
):
    """for making light and dark versions of a figure all at once. The idea is to drop in this function at the bottom, and not have
    to modify the above code much at all.

    - use small_ax.bg = "dm_convert" to convert an ax background (like an inset) to dark background, but no alpha
    - on text elements that should not be converted from non-white to white, use the gid param with 'keep': 'ax.text(..., gid="keep")

    Args:
        fig (plt.Figure | None, optional): _description_. Defaults to None.
        name (str, optional): _description_. Defaults to "figure".
        loc (str, optional): _description_. Defaults to "./".
        override_alpha (bool, optional): _description_. Defaults to False.
        override_cmap (bool, optional): _description_. Defaults to False.
    """

    sep = name.split("/")
    print(sep)
    sl = "/"
    loc = sl.join(sep[:-1]) + "/"
    print(loc)
    name = sep[-1]

    if loc != "./":
        if not os.path.exists(loc):
            os.makedirs(loc)

    # create two colormaps
    # cmap1 = plt.cm.plasma
    # cmap2 = plt.cm.inferno
    # n = 256
    # # create a new colormap that is a mix of the two
    # colors1 = cmap1(np.linspace(0.0, 1, n))
    # colors2 = cmap2(np.linspace(0, 1, n))
    # colors = np.zeros((n, 4))
    # colors[:, :3] = 0.4 * colors1[:, :3] + 0.6 * colors2[:, :3]  # / 2
    # colors[:, 3] = 0.4 * colors1[:, 3] + 0.6 * colors2[:, 3]  # / 2
    # # print(colors)
    # for i in range(len(colors)):
    #     colors[i][:3] = rgb_color_saturation(colors[i][:3], 0.75)
    #     colors[i][:3] = lift_gamma_gain(colors[i][:3], 0.1, 1.0, 1.0)

    # mixed_cmap = ListedColormap(colors)

    if custom_map is None:
        mixed_cmap = custom_cmap()

    if fig is None:
        fig = plt.gcf()
    assert isinstance(fig, matplotlib.figure.Figure)

    # some graphs are not pickleable, like 3d plots
    # pickeling is the only reliable way of fully duplicating a figure
    try:
        buf = io.BytesIO()
        pickle.dump(fig, buf)
        buf.seek(0)
        fig2 = pickle.load(buf)
        pickleable = True
        print("pickleable")
    except Exception as e:
        traceback.print_exc()
        pickleable = False

    old_legends = []

    for ax in fig.axes:
        try:
            print(ax.my_key)
        except:
            pass

        # print("edgeclor: ", ax.spines["right"].get_edgecolor())
        # print("edgeclor: ", ax.spines["bottom"].get_edgecolor())
        # print("edgeclor: ", ax.spines["left"].get_edgecolor())

        default_dark_color = (0.2, 0.2, 0.2, 1.0)

        # this changes color of the colorbar edges

        for spine in ax.spines.values():
            if spine.get_edgecolor() == default_dark_color:
                spine.set_color("#B6BCCF")
        for tick in ax.xaxis.get_major_ticks() + ax.yaxis.get_major_ticks():
            if tick.label1.get_color() == default_dark_color:
                tick.label1.set_color("#B6BCCF")

        x_tick_color = mcolors.to_rgba(ax.xaxis.get_ticklabels()[0].get_color())
        y_tick_color = mcolors.to_rgba(ax.yaxis.get_ticklabels()[0].get_color())

        if x_tick_color == default_dark_color:
            ax.tick_params(axis="x", colors="#B6BCCF")
        if y_tick_color == default_dark_color:
            ax.tick_params(axis="y", colors="#B6BCCF")

        # ax.tick_params(axis="both", colors="#B6BCCF")
        # ax.tick_params(axis="x", colors="#B6BCCF")
        # ax.tick_params(axis="y", colors="#B6BCCF")

        # dark mode
        if ax.spines["bottom"].get_edgecolor() == default_dark_color:
            ax.spines["bottom"].set_color("#B6BCCF")

        if ax.spines["left"].get_edgecolor() == default_dark_color:
            ax.spines["left"].set_color("#B6BCCF")

        if ax.spines["right"].get_edgecolor() == default_dark_color:
            ax.spines["right"].set_color("#B6BCCF")

        if ax.spines["top"].get_edgecolor() == default_dark_color:
            ax.spines["top"].set_color("#B6BCCF")

        if ax.xaxis.label.get_color() == default_dark_color:
            ax.xaxis.label.set_color("#B6BCCF")

        if ax.yaxis.label.get_color() == default_dark_color:
            ax.yaxis.label.set_color("#B6BCCF")

        # ax.yaxis.label.set_color("#B6BCCF")

        manage_lines(ax.lines, override_alpha)

        rectangles = [
            child for child in ax.get_children() if isinstance(child, plt.Rectangle)
        ]

        for rect in rectangles:
            # print("rect: ", rect)
            # print("rect color: ", rect.get_facecolor())
            c = rect.get_facecolor()
            if mcolors.to_hex(c) != "#39394A":
                c_b = mcolors.to_rgba(brighten_color(mcolors.to_hex(c), 0.5), 1)
                # print(c_b)
                rect.set_facecolor(c_b)

        if ax.__dict__.get("bg") == "dm_convert":
            # a light blue with very low alpha
            # ax.set_facecolor("#222229")
            ax.set_facecolor(mcolors.to_rgba("#222229", 1))
        else:
            # a light blue with very low alpha
            ax.set_facecolor(mcolors.to_rgba("#A3A3FF", 0.04))

        quad_mesh = [
            child
            for child in ax.get_children()
            if isinstance(child, plt.matplotlib.collections.QuadMesh)
        ]
        for mesh in quad_mesh:
            mesh.set_cmap(mixed_cmap)

        for image in ax.get_images():
            if not override_cmap:
                image.set_cmap(mixed_cmap)

        collections_list = ax.collections
        for obj in collections_list:
            if isinstance(obj, matplotlib.collections.PathCollection):
                # This object is a scatter plot
                # Do something with it
                if not override_cmap:
                    obj.set_cmap(mixed_cmap)
                # print(obj.get_facecolor()[0])

                color = obj.get_facecolor()[0]
                if np.allclose(color[:3], [0, 0, 0]):  # RGBA for black
                    obj.set_facecolor([1, 1, 1, color[-1]])
                    obj.set_edgecolor([1, 1, 1, color[-1]])
                else:
                    obj.set_facecolor(
                        mcolors.to_rgba(
                            brighten_color(mcolors.to_hex(color), color[-1]),
                            np.sqrt(color[-1]),
                        )
                    )
                    obj.set_edgecolor(
                        mcolors.to_rgba(
                            brighten_color(mcolors.to_hex(color), color[-1]),
                            np.sqrt(color[-1]),
                        )
                    )

                # print(obj.get_facecolor()[0])

            if isinstance(obj, matplotlib.collections.PolyCollection):
                print("found fill_bewteen poly collection")

                color = obj.get_facecolor()[0]
                # Convert the color to HLS
                h, l, s = colorsys.rgb_to_hls(color[0], color[1], color[2])
                # Increase the lightness by 2x
                l = min(l * 1.5, 1)
                # Convert the color back to RGB
                r, g, b = colorsys.hls_to_rgb(h, l, s)
                # Set the new color
                obj.set_facecolor((r, g, b, np.sqrt(color[3])))
                obj.set_edgecolor((r, g, b, np.sqrt(color[3])))

        for patch in ax.patches:
            face_color = patch.get_facecolor()
            patch.set_facecolor(
                mcolors.to_rgba(
                    brighten_color(mcolors.to_hex(face_color), 0.1),
                    np.sqrt(face_color[-1]),
                )
            )
            edge_color = patch.get_edgecolor()
            patch.set_edgecolor(
                mcolors.to_rgba(
                    brighten_color(mcolors.to_hex(edge_color), 0.1),
                    np.sqrt(edge_color[-1]),
                )
            )
            if not override_alpha:
                patch.set_alpha(dark_alpha_converter(patch.get_alpha()))

        bars = ax.containers
        # for bar in bars:
        #     if ErrorbarContainer

        errorbars = [
            bar
            for bar in ax.containers
            if isinstance(bar, matplotlib.container.ErrorbarContainer)
        ]
        for errbar in errorbars:
            # this handles errorbar color
            for sub_bar in errbar:
                try:
                    for sub_thing in sub_bar:
                        # print(sub_thing)
                        c = sub_thing.get_color()
                        c_b = mcolors.to_rgba(brighten_color(mcolors.to_hex(c), 0.5), 1)
                        sub_thing.set_color(c_b)
                        # sub_thing.set_alpha(dark_alpha_converter(sub_thing.get_alpha()))
                except:
                    pass

        if ax.legend_ is not None:
            # print(ax.legend_.get_edgecolor())
            old_legends.append(copy.copy(ax.legend_))
            # ax.legend_.set_edgecolor("#B6BCCF")
            # print("edgecolor: ", ax.legend_.get_edgecolor())
            legend_frame = ax.legend_.get_frame()
            # legend_frame.set_edgecolor("#B6BCCF")
            legend_frame.set_edgecolor("none")

            legend_frame.set_facecolor("#343444")
            legend_frame.set_alpha(0.72)

            legend_patches = ax.legend_.get_patches()

            # there is no nice "get_errorbars()" function, so we have to do this recursive search
            handle_legend_errbars(
                ax.legend_.get_children(), max_depth=5, override_alpha=override_alpha
            )

            manage_lines(ax.legend_.get_lines(), override_alpha)

            # print("legend_patches: ", legend_patches)
            for patch in legend_patches:
                # print("patches color: ", patch.get_facecolor())
                c = patch.get_facecolor()
                # alpha = patch.get_alpha()
                # print("pathc alpha: ", alpha)
                if not override_alpha:
                    patch.set_alpha(dark_alpha_converter(patch.get_alpha()))

                c_b = mcolors.to_rgba(brighten_color(mcolors.to_hex(c), 0.5), 1)
                patch.set_facecolor(c_b)

        text_list = ax.findobj(match=plt.Text)
        for text in text_list:
            # this includes number labels for axese
            # if it's the default dark color OR black, change it

            rgba_color = mcolors.to_rgba(text.get_color())
            if (
                rgba_color == default_dark_color and text.get_gid() != "keep_color"
            ) or rgba_color[:3] == (0, 0, 0):
                text.set_color("#B6BCCF")
            else:
                text.set_color(
                    mcolors.to_rgba(
                        brighten_color(mcolors.to_hex(rgba_color), 0.5),
                        np.sqrt(rgba_color[-1]),
                    )
                )

            arrow_list = text.findobj(match=matplotlib.patches.FancyArrowPatch)
            for arrow in arrow_list:
                arrow.set(edgecolor="red")

        if ax.name == "3d":
            # 3d plots don't need face color
            ax.set_facecolor("none")
            # for bar in ax.collections:
            #     bar.set_edgecolor('#B6BCCF')
            # ax.patch.set_facecolor("#B6BCCF")
            # ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 0.1))
            # ax.x_axis.set_pane_color((1.0, 1.0, 1.0, 0.1))
            # ax.y_axis.set_pane_color((1.0, 1.0, 1.0, 0.1))

            # ax.xaxis.pane.fill = False
            # ax.yaxis.pane.fill = False
            # ax.zaxis.pane.fill = False
            # print(ax.get_facecolor())

            # ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.1))
            # ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.1))
            # ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.1))

            ax.xaxis.pane.set_edgecolor("w")
            ax.yaxis.pane.set_edgecolor("w")
            ax.zaxis.pane.set_edgecolor("w")

        # collections_list = ax.collections
        # for obj in collections_list:
        #     if isinstance(obj, matplotlib.collections.PathCollection):
        #         print(obj.get_facecolor()[0])

    annotation_list = fig.findobj(match=matplotlib.patches.FancyArrowPatch)
    # print(annotation_list)
    for annotation in annotation_list:
        annotation.set(edgecolor="red")

    fig.patch.set_facecolor("#2E303E")

    # update_colors(dark=True)
    fig.patch.set_facecolor("none")
    fig.savefig(os.path.join(loc, f"{name}_dark.svg"))

    ############ light

    # update_colors(dark=False)
    # fig = fig_cpy

    # fig = pickle.load(buf)

    if pickleable is True:
        fig2.patch.set_facecolor("none")
        for ax in fig2.axes:
            # ax.set_facecolor('none')
            ax.set_facecolor(mcolors.to_rgba("#FDFEFF", 0.60))

        fig2.savefig(os.path.join(loc, f"{name}_light.svg"))

        fig2.patch.set_facecolor("white")
        fig2.savefig(os.path.join(loc, f"{name}_light.pdf"))
    else:
        fig.patch.set_facecolor("none")

        for ax in fig.axes:
            # light mode
            ax.set_facecolor("none")
            ax.spines["bottom"].set_color("#333333")
            ax.spines["left"].set_color("#333333")
            ax.spines["right"].set_color("#333333")
            ax.spines["top"].set_color("#333333")
            ax.xaxis.label.set_color("#333333")
            ax.yaxis.label.set_color("#333333")
            ax.tick_params(axis="x", colors="#333333")
            ax.tick_params(axis="y", colors="#333333")
            if ax.legend_ is not None:
                # ax.legend(edgecolor="#333333")
                ax.legend_ = old_legends.pop(0)
            text_list = ax.findobj(match=plt.Text)
            for text in text_list:
                if text.get_color() != "white":
                    text.set_color("#333333")
            if ax.name == "3d":
                # 3d plots don't need face color
                ax.set_facecolor("none")

        fig.patch.set_facecolor("none")

        fig.savefig(os.path.join(loc, f"{name}_light.svg"))
        fig.savefig(os.path.join(loc, f"{name}.pdf"))


def _get_ipython_safe():
    try:
        from IPython import get_ipython as _get

        return _get()
    except Exception:
        return None


def is_notebook() -> bool:
    ip = _get_ipython_safe()
    if ip is None:
        return False
    shell = ip.__class__.__name__
    if shell == "ZMQInteractiveShell":
        return True  # Jupyter notebook or qtconsole
    elif shell == "TerminalInteractiveShell":
        return False  # Terminal running IPython
    else:
        return False  # Other type (?)


def matplotlib_ipython_svg_mode():
    if is_notebook():
        ipython = _get_ipython_safe()
        if ipython is not None:
            ipython.run_line_magic("config", "InlineBackend.figure_formats = ['svg']")


def ipython_autoreload():
    if is_notebook():
        ipython = _get_ipython_safe()
        if ipython is not None:
            ipython.run_line_magic("load_ext", "autoreload")
            ipython.run_line_magic("autoreload", "2")


def matplotlib_ipython_png_mode():
    if is_notebook():
        ipython = _get_ipython_safe()
        if ipython is not None:
            ipython.run_line_magic("config", "InlineBackend.figure_formats = ['png']")


def phd_style(
    dark_mode: bool = False,
    jupyterStyle: bool = False,
    axese_width: int = 0,
    text: int = 0,
    tick_length: int = 0,
    data_width: int = 0,
    grid: bool = False,
    svg_mode=True,
):
    """
    Sets the plotting style to my preference
    """
    axese_width_j = 0
    text_j = 0
    tick_length_j = 0
    data_width_j = 0
    if jupyterStyle:
        axese_width_j = 0.6
        text_j = 5
        tick_length_j = 1
        data_width_j = 1.5

    items = []
    for item_org, item_j in zip(
        [axese_width, text, tick_length, data_width],
        [axese_width_j, text_j, tick_length_j, data_width_j],
    ):
        if item_org == 0:
            items.append(item_j)
        else:
            items.append(item_org)

    rc = {
        # "axes.facecolor": "#fafafa",
        "axes.facecolor": "#ffffff",
        "font.family": "sans-serif",
        "font.family": "DejaVu Sans",
        "font.style": "normal",
        "pdf.fonttype": 42,
        "patch.linewidth": 3,
        "axes.edgecolor": "#333333",
        "axes.labelcolor": "#333333",
        "axes.spines.right": False,
        "axes.spines.top": False,
        "axes.spines.left": True,
        "axes.spines.bottom": True,
        "axes.axisbelow": True,
        "axes.linewidth": 0.6 + items[0],
        "axes.titlesize": 9 + items[1],
        "text.color": "#333333",
        "axes.grid": grid,
        "lines.linewidth": 0.75 + items[3],
        "lines.dash_capstyle": "round",
        "patch.linewidth": 0.25,
        # "grid.linestyle": "-",
        # "grid.linewidth": 0.75,
        # "grid.color": "#ffffff",
        "axes.labelsize": 8 + items[1],
        "xtick.color": "#333333",
        "ytick.color": "#333333",
        "xtick.labelsize": 6 + items[1],
        "ytick.labelsize": 6 + items[1],
        "xtick.major.size": 3 + items[2],
        "ytick.major.size": 3 + items[2],
        "xtick.major.width": 0.6 + items[0],
        "ytick.major.width": 0.6 + items[0],
        "xtick.major.pad": 3,
        "ytick.major.pad": 3,
        "xtick.minor.size": 0,
        "ytick.minor.size": 0,
        "legend.fontsize": 7 + items[1],
        "legend.frameon": True,
        "legend.edgecolor": "#333333",
        "axes.xmargin": 0.03,
        "axes.ymargin": 0.03,
        "figure.facecolor": "white",
        "figure.dpi": 250,
        "errorbar.capsize": 1,
        "savefig.bbox": "tight",
        "grid.alpha": 0.2,
    }

    if dark_mode:
        rc = {
            # "axes.facecolor": "black",
            "axes.facecolor": "#3d3f4f",
            "axes.facecolor": "#2E303E",
            "font.family": "sans-serif",
            "font.family": "DejaVu Sans",
            "font.style": "normal",
            "pdf.fonttype": 42,
            "patch.linewidth": 3,
            "axes.edgecolor": "#dbdbdb",
            "axes.labelcolor": "#dbdbdb",
            "axes.spines.right": False,
            "axes.spines.top": False,
            "axes.spines.left": True,
            "axes.spines.bottom": True,
            "axes.axisbelow": True,
            "axes.linewidth": 0.6 + items[0],
            "axes.titlesize": 9 + items[1],
            "text.color": "#444147",
            "axes.grid": grid,
            "lines.linewidth": 0.75 + items[3],
            "lines.dash_capstyle": "round",
            "patch.linewidth": 0.25,
            # "grid.linestyle": "-",
            # "grid.linewidth": 0.75,
            # "grid.color": "#ffffff",
            "axes.labelsize": 8 + items[1],
            "xtick.color": "#dbdbdb",
            "ytick.color": "#dbdbdb",
            "xtick.labelsize": 6 + items[1],
            "ytick.labelsize": 6 + items[1],
            "xtick.major.size": 3 + items[2],
            "ytick.major.size": 3 + items[2],
            "xtick.major.width": 0.6 + items[0],
            "ytick.major.width": 0.6 + items[0],
            "xtick.major.pad": 3,
            "ytick.major.pad": 3,
            "xtick.minor.size": 0,
            "ytick.minor.size": 0,
            "legend.fontsize": 7 + items[1],
            "legend.frameon": True,
            "legend.edgecolor": "#dbdbdb",
            "axes.xmargin": 0.03,
            "axes.ymargin": 0.03,
            "figure.facecolor": "#2E303E",
            "figure.dpi": 250,
            "errorbar.capsize": 1,
            "savefig.bbox": "tight",
            "grid.alpha": 0.3,
        }

    if svg_mode:
        matplotlib_ipython_svg_mode()
    else:
        matplotlib_ipython_png_mode()
        # to match the sizing of svg mode better
        matplotlib.style.use({"figure.dpi": 250})
    ipython_autoreload()

    plt.rc("text.latex", preamble=r"\usepackage{mathpazo}")
    matplotlib.style.use(rc)
    if dark_mode:
        colors, palette = color_palette(dark=True)
    else:
        colors, palette = color_palette()
    # sns.set_palette(palette)
    return colors, palette


import json


# how to use custom bokeh saving method:
# source = ColumnDataSource(data=dB_parm)

# plot = figure(width=800, height=400, x_range=(-100,140), y_range=(.0001, .1), y_axis_type="log")
# l = plot.line("x", "y", source=source, line_width=2, line_alpha=0.6, color="#66a1ff", legend_label="peacoq response function")

# callback = CustomJS(args=dict(source=source), code="""
#     //const legend = ["this", "that", "the other thing"]
#     const data = source.data;
#     const f = cb_obj.value
#     let name_x = f.toString()
#     let name_y = f.toString()
#     name_x += "_histx"
#     name_y += "_histy"
#     //const x = data['histx']
#     data["y"] = data[name_y]
#     data["x"] = data[name_x]
#     source.change.emit();
# """)
# slider = DarkSlider(start=64, end=94, value=94, step=2, title="attenuation (dB)", direction='rtl', margin=[10,20], sizing_mode="stretch_width")

# slider.js_on_change('value', callback)
# li = LegendItem(label='peacoq response function', renderers=[l])
# layout = column(slider, plot)

# save_bokeh_dark_json(layout, "test_1.json", apply=True)

# show(layout)


def save_bokeh_dark_json(object, save_name: str, tick_lw=1.5, apply=False) -> object:
    """create a dark bokeh theme, apply it to a json output file, and optionally
    apply it to the current document

    Args:
        object (_type_): bokeh object to save
        save_name (str): name of file to save
        tick_lw (float, optional): tick linewidth. Defaults to 1.5.
        apply (bool, optional): whether to apply dark theme to curdoc(). Defaults to False.

    Returns:
        Theme: dark theme
    """

    try:
        from bokeh.themes import Theme  # type: ignore
        from bokeh.embed import json_item  # type: ignore
        from bokeh.io import curdoc  # type: ignore
    except Exception as e:
        raise ImportError(
            "save_bokeh_dark_json requires bokeh. Install with: pip install 'snsphd[viz]'"
        ) from e

    dark_mode = Theme(
        json={
            "attrs": {
                "figure": {
                    "background_fill_color": "#3d3f4f",  # this is for mkdocs
                    "border_fill_color": "#24242d",
                    "outline_line_color": "#444444",
                },
                "Axis": {
                    "major_tick_line_alpha": 1,
                    "major_tick_line_color": "#b8b9bf",
                    "minor_tick_line_alpha": 1,
                    "minor_tick_line_color": "#b8b9bf",
                    "axis_line_alpha": 1,
                    "axis_line_color": "#b8b9bf",
                    "major_label_text_color": "#b8b9bf",
                    "major_label_text_font": "Helvetica",
                    # "major_label_text_font_size": "1.15em",
                    "axis_label_standoff": 10,
                    "axis_label_text_color": "#b8b9bf",
                    "axis_label_text_font": "Helvetica",
                    # "axis_label_text_font_size": "1.35em",
                    "axis_label_text_font_style": "normal",
                    "axis_line_width": 1.5,
                    "axis_line_cap": "round",
                    "major_tick_line_width": tick_lw,
                    "minor_tick_line_width": tick_lw,
                    "major_tick_line_cap": "round",
                    "minor_tick_line_cap": "round",
                    "major_tick_out": 7,
                    "major_tick_in": 0,
                },
                "Grid": {
                    # 'grid_line_dash': [6, 4],
                    "grid_line_alpha": 1,
                    "grid_line_width": 1.2,
                    "grid_line_color": "#575766",
                },
                "Title": {
                    "text_color": "white",
                    "background_fill_color": "#24242d",
                    "align": "left",
                    "text_font_style": "normal",
                    # "text_font_size": "14pt",
                    "offset": 0,
                },
                "Legend": {
                    "spacing": 8,
                    "glyph_width": 15,
                    "label_standoff": 8,
                    "label_text_color": "#e0e0e0",
                    "label_text_font": "Helvetica",
                    # "label_text_font_size": "1.025em",
                    "border_line_alpha": 0,
                    "background_fill_alpha": 0.25,
                    "background_fill_color": "#797c91",
                },
                "Toolbar": {
                    "autohide": False,
                    "logo": None,
                },
                "ColorBar": {
                    "title_text_color": "#e0e0e0",
                    "title_text_font": "Helvetica",
                    # "title_text_font_size": "1.025em",
                    "title_text_font_style": "normal",
                    "major_label_text_color": "#e0e0e0",
                    "major_label_text_font": "Helvetica",
                    # "major_label_text_font_size": "1.025em",
                    "background_fill_color": "#15191c",
                    "major_tick_line_alpha": 0,
                    "bar_line_alpha": 0,
                },
                "Line": {
                    "line_color": "#c08df0",
                    "line_width": 1.9,
                },
                "Slider": {
                    "bar_color": "#3d3f4f",
                },
            }
        }
    )

    item_text = json.dumps(json_item(object, theme=dark_mode))
    # if end of name is not '.json', add it
    if save_name[-5:] != ".json":
        save_name += ".json"
    with open(save_name, "w") as file:
        file.write(item_text)

    if apply:
        curdoc().theme = dark_mode

    return dark_mode


def DarkSlider(**kwargs):
    try:
        from bokeh.models import InlineStyleSheet, Slider  # type: ignore
    except Exception as e:
        raise ImportError(
            "DarkSlider requires bokeh. Install with: pip install 'snsphd[viz]'"
        ) from e

    sty = InlineStyleSheet(
        css=""".bk-slider-title { background-color: none; }
                                                    .noUi-target { border-color: #56586b !important; }
                                                    .noUi-connects { background-color: #56586b; }
                                                    .noUi-touch-area { background-color: #56586b;
                                                                       border-radius: 1px;
                                                                       box-shadow: 0 0 0 1px #2e2e2e;
                                                                       border-color: #56586b !important; }
                                                    .noUi-handle.noUi-handle-lower { border-radius: 1px;
                                                                                     background-color: #727487;
                                                                                     border-color: #9799ad !important;
                                                                                     box-shadow: none; }
                                                    .noUi-touch-area { display: none; }"""
    )

    return Slider(stylesheets=[sty], **kwargs)


def bokeh_theme(return_color_list=True) -> tuple[dict, list]:
    try:
        import bokeh  # type: ignore
    except Exception as e:
        raise ImportError(
            "bokeh_theme requires bokeh. Install with: pip install 'snsphd[viz]'"
        ) from e

    tick_and_line_color = "#4f4f4f"
    lw = 1.7
    theme_json = {
        "attrs": {
            "figure": {"background_fill_color": "#f7f8fa", "outline_line_color": None},
            "Axis": {
                "axis_line_color": tick_and_line_color,
                "axis_line_width": 1.5,
                "axis_line_cap": "round",
                "major_tick_line_width": lw,
                "minor_tick_line_width": lw,
                "major_tick_line_cap": "round",
                "minor_tick_line_cap": "round",
                "major_tick_out": 7,
                "major_tick_in": 0,
                "major_tick_line_color": tick_and_line_color,
                "minor_tick_line_color": tick_and_line_color,
                "axis_label_text_font_size": "14pt",
                "major_label_text_font_size": "14pt",
                # "axis_label_text_font": "Open Sans Semibold",
                # "major_label_text_font": "Open Sans Semibold",
            },
            "legend_label": {
                "border_line_color": "black",
                "background_fill_color": "#EEEEEE",
                "border_line_width": 0.75,
                "background_fill_alpha": 0.75,
                "legend_font_size": "20pt",
            },
            "Grid": {
                "grid_line_alpha": 0.06,
                "grid_line_color": "black",
                "grid_line_width": 1.3,
                "grid_line_dash": "solid",
            },
            # "WheelZoomTool": {
            #     "dimension": 'width'
            # },
            "ToolbarBase": {
                "autohide": False,
                "logo": None,
            },
            "Text": {
                "text_font_style": "regular",
                "text_font_size": "48pt",
            },
            "Title": {
                "background_fill_color": "#FFFFFF",
                "text_color": "#3c3c3c",
                "align": "left",
                # "text_font": "Open Sans Semibold",
                "text_font_style": "normal",
                "text_font_size": "14pt",
                "offset": 0,
            },
            "Line": {
                "line_width": 2.2,
                # "line_color": '#b00c00'
            },
        }
    }

    colors, palette = color_palette()
    theme = bokeh.themes.Theme(json=theme_json)
    bokeh.themes
    bokeh.io.curdoc().theme = theme
    if return_color_list:
        return (colors, palette)
    else:
        return colors


# def altair_theme():
#     """
#     Sets a theme for the plotting library Altair to match the style of my PhD.
#     """
#
#     colors, palette = color_palette()
#     def _theme():
#         return {
#             'config': {
#                 'background': 'white',
#                     'group': {
#                     'fill': 'white',
#                     },
#                 'view': {
#                     'strokeWidth': 3,
#                     'height': 300,
#                     'width': 400,
#                     'fill': '#EEEEEE'
#                     },
#                 'mark': {
#                     'strokeWidth': 2,
#                     'stroke': 'black'
#                 },
#                 'axis': {
#                     'domainColor': colors['black'],
#                     'domainWidth': 0.5,
#                     'labelColor': colors['black'],
#                     'labelFontSize': 8,
#                     'labelFont': 'Myriad Pro',
#                     'titleFont': 'Myriad Pro',
#                     'titleFontWeight': 400,
#                     'titleFontSize': 8,
#                     'grid': True,
#                     'gridColor': 'white',
#                     'gridWidth': 0.75,
#                     'ticks': True,
#                     'tickColor': 'white',
#                     'tickOffset': 8,
#                     'tickWidth': 1.5
#                 },
#                 'Grid': {
#                     'grid_line_dash': [6,4]
#                 }
#                 'range': {
#                     'category': palette
#                 },
#                 'legend': {
#                     'labelFontSize': 8,
#                     'labelFont': 'Myriad Pro',
#                     'titleFont': 'Myriad Pro',
#                     'titleFontSize': 8,
#                     'titleFontWeight': 400
#                 },
#                 'title' : {
#                     'font': 'Myriad Pro',
#                     'fontWeight': 400,
#                     'fontSize': 8,
#                     'anchor': 'middle'
#                 }
#                   }
#                 }
#
#     alt.themes.register('phd', _theme)# enable the newly registered theme
#     alt.themes.enable('phd')
#     return colors, palette


def color_selector(style):
    """
    Select the color palette of your choice.

    Parameters
    ----------
    style: str "mut" or "pboc"
        A string identifier for the style. "mut" gives colors for single and double mutants.
        "pboc" returns the PBoC2e color palette.

    Returns
    -------
    colors: dict
        Dictionary of colors. If "dna", "double", or "inducer" is the selected style,
        keys will be the mutants in upper case. Double mutant keys will be DNA-IND. For
        pboc, the keys will be the typical color descriptors.

    """
    # Ensure the provided style name makes sense.
    if style.lower() not in ["mut", "pboc"]:
        raise ValueError(
            "Provided style must be 'pboc' or 'mut'. {} provided.".format(style)
        )

    # Set the color styles and return.
    if style.lower() == "mut":
        colors = {
            "Y20I": "#738FC1",
            "Q21A": "#7AA974",
            "Q21M": "#AB85AC",
            "F164T": "#A97C50",
            "Q294K": "#5D737E",
            "Q294V": "#D56C55",
            "Q294R": "#B2AF58",
            "Y20I-F164T": "#2d98da",
            "Y20I-Q294K": "#34495e",
            "Y20I-Q294V": "#8854d0",
            "Q21A-F164T": "#4b6584",
            "Q21A-Q294K": "#EE5A24",
            "Q21A-Q294V": "#009432",
            "Q21M-F164T": "#1289A7",
            "Q21M-Q294K": "#6F1E51",
            "Q21M-Q294V": "#006266",
            "WT": "#3C3C3C",
        }

    elif style.lower() == "pboc":
        colors = {
            "green": "#7AA974",
            "light_green": "#BFD598",
            "pale_green": "#DCECCB",
            "yellow": "#EAC264",
            "light_yellow": "#F3DAA9",
            "pale_yellow": "#FFEDCE",
            "blue": "#738FC1",
            "light_blue": "#A9BFE3",
            "pale_blue": "#C9D7EE",
            "red": "#D56C55",
            "light_red": "#E8B19D",
            "pale_red": "#F1D4C9",
            "purple": "#AB85AC",
            "light_purple": "#D4C2D9",
            "dark_green": "#7E9D90",
            "dark_brown": "#905426",
        }
    return colors


def titlebox(
    ax, text, color, bgcolor=None, size=8, boxsize="10%", pad=0.02, loc=10, **kwargs
):
    """Sets a colored box about the title with the width of the plot"""
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("top", size=boxsize, pad=pad)
    cax.get_xaxis().set_visible(False)
    cax.get_yaxis().set_visible(False)
    cax.spines["top"].set_visible(True)
    cax.spines["right"].set_visible(True)
    plt.setp(cax.spines.values(), color=color)
    if bgcolor != None:
        cax.set_facecolor(bgcolor)
    else:
        cax.set_facecolor("white")
    at = AnchoredText(text, loc=loc, frameon=False, prop=dict(size=size, color=color))
    cax.add_artist(at)


def ylabelbox(ax, text, color, bgcolor=None, size=6, boxsize="15%", pad=0.02, **kwargs):
    """Sets a colored box about the title with the width of the plot"""
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("left", size=boxsize, pad=pad)
    cax.get_xaxis().set_visible(False)
    cax.get_yaxis().set_visible(False)
    cax.spines["top"].set_visible(True)
    cax.spines["right"].set_visible(True)
    plt.setp(cax.spines.values(), color=color)
    if bgcolor != None:
        cax.set_facecolor(bgcolor)
    else:
        cax.set_facecolor("white")

    at = AnchoredText(
        text,
        loc=10,
        frameon=False,
        prop=dict(rotation="vertical", size=size, color=color),
    )
    cax.add_artist(at)
