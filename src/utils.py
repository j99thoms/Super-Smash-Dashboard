import re
import pandas as pd
import dash_bootstrap_components as dbc
from dash import html
from dash_iconify import DashIconify

IMG_DIR = "assets/img"
TXT_DIR = "assets/txt"

def get_icon(icon, height=16):
    return DashIconify(icon=icon, height=height)

def get_logo():
    logo = html.A(
        children=[html.Img(src=f'{IMG_DIR}/logo.png')],
        className='logo',
        href="/",
        target="_self",
    )
    return logo

def get_attribute_info_block():
    attribute_info_paragraphs = get_attribute_info()

    smash_wiki_credits = "These attribute descriptions are based on the descriptions which can be found on "
    smash_wiki_hyperlink = html.A(
                                "SmashWiki", 
                                href="https://www.ssbwiki.com/",
                                target="_blank"
                            )

    attr_info = dbc.Col([
        html.Div(
            id="attribute-info-block",
            children=[
                html.Div([
                    html.Div([
                        html.H4(
                            [html.U("Attribute Info")], 
                            style={"text-align": "center"}
                        ),
                        *attribute_info_paragraphs,
                        html.Div([
                            smash_wiki_credits,
                            smash_wiki_hyperlink,
                            "."
                        ], style={"margin-top": "30px", "font-size": "85%"})
                    ],
                    style={"width": "98%", "float": "right"}),
                ],
                style={"width": "98%", "float": "left", "margin-top": "10px"}),
            ],
        )
    ])
    
    return attr_info

def get_introduction_block():
    introduction_paragraphs = get_introduction()

    intro_block = html.Div(
        id="introduction-container",
        children=[
            html.Div(
                children=[
                    html.Div(
                        children=introduction_paragraphs,
                        style={"width": "98%", "height": "100%", "float": "right"}
                    )
                ],
                style={"width": "98%", "height": "100%", "float": "left", "margin-top": "10px"}
            )
        ]
    )

    return intro_block

def get_attribute_info():
    with open(f"{TXT_DIR}/attribute_info.txt", "r") as text:
        lines = text.readlines()

    paragraphs = []
    p_children = []

    for line in lines:
        if line.endswith("\n"):
            if line.find("\n") != 0:
                for segment in parse_bolds(line[:-1]):
                    p_children.append(segment)
            else:
                paragraphs.append(
                    html.P(
                        children=p_children, 
                        className="attribute-info-paragraph"
                    )
                )
                p_children = []
        else:
            for segment in parse_bolds(line):
                p_children.append(segment)

    if len(p_children) > 0:
        paragraphs.append(
            html.P(
                children=p_children, 
                className="attribute-info-paragraph"
            )
        )

    return paragraphs

def get_introduction():
    with open(f"{TXT_DIR}/introduction.txt", "r") as text:
        lines = text.readlines()

    paragraphs = []
    p_children = []

    for line in lines:
        if line.endswith("\n"):
            if line.find("\n") != 0:
                for segment in parse_bolds(line[:-1]):
                    p_children.append(segment)
            else:
                paragraphs.append(
                    html.P(
                        children=p_children,
                        className="introduction-paragraph"
                    )
                )
                p_children = []
        else:
            for segment in parse_bolds(line):
                p_children.append(segment)

    if len(p_children) > 0:
        paragraphs.append(
            html.P(
                children=p_children,
                className="introduction-paragraph"
            )
        )

    return paragraphs

def parse_bolds(line):
    # Regex pattern to match text surrounded by '**'
    bold_pattern = r'(\*\*.*\*\*)'
    
    if re.search(bold_pattern, line):
        first_delim = line.find("**")
        second_delim = line[first_delim + 2:].find("**") + first_delim + 2
        if first_delim > 0:
            parsed_line = [line[:first_delim]] + [html.B(line[first_delim + 2:second_delim])] + parse_bolds(line[second_delim + 2:])
        else:
            parsed_line = [html.B(line[first_delim + 2:second_delim])] + parse_bolds(line[second_delim + 2:])
    else:
        parsed_line = [line]

    return parsed_line

def get_screen_width(display_size_str):
    # display_size_str looks like "Breakpoint name: <=1500px, width: 1440px"
    screen_width = int(display_size_str.split(" ")[4].strip("px"))

    return screen_width

def get_character_data():
    character_attributes_df = pd.read_csv("../data/character_data.csv").drop(
        columns=['percent_incr_fall_speed']  # Unused column
    )

    return character_attributes_df

def get_correlations_df():
    attributes_df = get_character_data()

    corr_df = attributes_df.corr(numeric_only=True, method='pearson')
    corr_df = corr_df.reset_index().melt(id_vars='index').rename(
        columns={
            'index': 'Attribute 1',
            'variable': 'Attribute 2', 
            'value': 'Correlation'
        }
    )
    
    corr_df['Correlation'] = corr_df['Correlation'].round(4)
    corr_df['corr_text_2'] = corr_df['Correlation'].round(2)
    corr_df['corr_text_1'] = corr_df['Correlation'].round(1)
    corr_df['abs_corr'] = corr_df['Correlation'].abs()

    return corr_df

def get_dropdown_options():
    character_attributes_df = get_character_data()

    # The first column is 'character', the last column is 'img_url'
    attribute_names = character_attributes_df.columns.to_series().iloc[1:-1]

    dropdown_options = [
        {'value': attribute_name, 'label': attribute_name}
        for attribute_name in attribute_names
    ]
    
    return dropdown_options

def make_dash_table(df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
        
    return table
