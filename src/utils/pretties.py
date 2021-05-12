import pandas as pd
import IPython.display as ip_disp


def max_data_frame_columns(n: int=None):
    pd.set_option('display.max_columns', n)

def display_html(html: str):
    ip_disp.display(ip_disp.HTML(html))

def display_md(md: str):
    ip_disp.display(ip_disp.Markdown(md))