import pandas as pd
from tile_generator import tile_generator

from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure
from bokeh.transform import dodge, factor_cmap
import bokeh.palettes as bp


def preprocessing(df, features):
    for feat in features:
        df[feat+'_num'] = df[feat].replace({' ': ''}, regex=True)
        df[feat+'_num'] = pd.to_numeric(df[feat+'_num'])
    return df


def plot_grid_map(df,
                  features_list,
                  map_title='Плиточная карта',
                  tile_names="subj_rus",
                  map_width=1000,
                  map_height=700,
                  bar_plot=False,
                  shuffle=True,
                  pixels=30,
                  is_pallete_custom=False,
                  pallete_name='Spectral',
                  pallete_custom=['#aaaacc',
                                  '#666688'],
                  output_filname='index.html',
                  fed_distr_color = True):

    output_file(output_filname, title=map_title)

    df['row'] = max(df['row']) - df['row']

    features_list_num = []

    df = preprocessing(df, features_list)
    [features_list_num.append(feat + '_num') for feat in features_list]

    im_arr = []
    for i in range(df.shape[0]):
        if bar_plot:
            im_arr.append(tile_generator(df[features_list_num].loc[i], False, shape=[100,1]))
        else:
            im_arr.append(tile_generator(df[features_list_num].loc[i], shuffle, shape=[pixels,pixels]))
    df['image'] = im_arr

    source = ColumnDataSource(df)

    p = figure(title=map_title,
               plot_width=map_width,
               plot_height=map_height,
               tools="",
               toolbar_location=None,
               x_range=(-1, 19),
               y_range=(-1, 11)
               )

    cmap = {
        "Северо-Западный федеральный округ": "#1f78b4",
        "Центральный федеральный округ": "#d93b43",
        "Дальневосточный федеральный округ": "#1f78f4",
        "Приволжский федеральный округ": "#599d7A",
        "Сибирский федеральный округ": "#999d9a",
        "Южный федеральный округ": "#f1d4Af",
        "Уральский федеральный округ": "#e08d49"
    }

    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.xaxis.visible=False
    p.yaxis.visible=False

    if is_pallete_custom:
        # Filling probably missing colors
        while len(features_list) > len(pallete_custom):
            pallete_custom.append(pallete_custom[-1])
        pallete_i = len(features_list)
        pallete = pallete_custom
    else:
        pallete_base = bp.all_palettes.get(pallete_name)
        pallete_i = max(3, len(features_list))
        pallete = pallete_base.get(pallete_i)

    # these layers -- to make a legend
    for i in range(len(features_list)):
        if len(features_list) < pallete_i:
            p.rect('col', 'row', 0.1, 0.1, source=source, alpha=1, color=pallete[i*2], legend=features_list[i]+' ')
        else:
            p.rect('col', 'row', 0.1, 0.1, source=source, alpha=1, color=pallete[ i ], legend=features_list[i]+' ')

    # 'image' has no hover option, that's why we use rect underlayer
    if fed_distr_color:
        p.rect('col', 'row', 0.9, 0.9, source=source, alpha=1,
               color=factor_cmap('fed_district_full', palette=list(cmap.values()), factors=list(cmap.keys())))
        p.rect('col', 'row', 0.9, 0.9, source=source, alpha=0.8, color='#ffffff')
    else:
        p.rect('col', 'row', 0.9, 0.9, source=source, alpha=1, color='#eeeeee')

    p.image(image=df['image'], x=df['col']-0.45, y=df['row']-0.45, dw=0.9, dh=0.7, palette=pallete)

    x = dodge("col", -0.4, range=p.x_range)
    text_props = {"source": source, "text_align": "left", "text_baseline": "middle"}
    r = p.text(x=x, y=dodge("row", 0.35, range=p.y_range), text=tile_names, **text_props, text_color="#000000")
    r.glyph.text_font_size="7pt"

    # p.legend.orientation = "horizontal"
    p.legend.location ="bottom_right"

    tooltips = [
        ("Округ: ", "@fed_district_full"),
        ("Субъект: ", "@subj_full")
    ]

    for feat in features_list:
        name = feat + ' '
        val = '@{' + feat + '}'
        tooltips.append((name, val))

    p.add_tools(HoverTool(tooltips = tooltips))

    show(p)
