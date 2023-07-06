# import seaborn as sns
import numpy as np

# import os
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.path import Path
from matplotlib.patches import BoxStyle
from matplotlib.offsetbox import AnchoredText
import matplotlib
from IPython import get_ipython

# import altair as alt

# import altair as alt


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
    print("colors, swatches = viz.bokeh_theme()\n\
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
                # "axes.facecolor": "#ffffff",
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


def is_notebook() -> bool:
    try:
        shell = get_ipython().__class__.__name__
        if shell == "ZMQInteractiveShell":
            return True  # Jupyter notebook or qtconsole
        elif shell == "TerminalInteractiveShell":
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False  # Probably standard Python interpreter


def setup_svg_and_autoreload():
    if is_notebook():
        ipython = get_ipython()
        ipython.run_line_magic("config", "InlineBackend.figure_formats = ['svg']")
        ipython.run_line_magic("load_ext", "autoreload")
        ipython.run_line_magic("autoreload", "2")


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
        "grid.alpha": 0.3,
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
        setup_svg_and_autoreload()

    plt.rc("text.latex", preamble=r"\usepackage{mathpazo}")
    matplotlib.style.use(rc)
    if dark_mode:
        colors, palette = color_palette(dark=True)
    else:
        colors, palette = color_palette()
    # sns.set_palette(palette)
    return colors, palette


# def load_bokeh():


def bokeh_theme() -> tuple[dict, list]:
    import bokeh

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
    
    return (colors, palette)
    


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
