import dash
from dash import html, dcc, callback_context
import feffery_antd_components as fac
from dash.dependencies import Input, Output
import config
import json
from urllib.parse import unquote

app = dash.Dash(__name__)

# 初始主题
app.layout = html.Div(id='main-container', children=[
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='theme-status'),  # 用于存储当前主题状态
    # 导航栏
    fac.AntdHeader(
        id='navbar',
        children=[
            html.Div([
                fac.AntdImage(
                    src=config.LOGO_PATH,
                    preview=False,
                    style={
                        'height': '30px',
                        'width': '30px',
                        'borderRadius': '50%',  # 圆形遮罩
                        'overflow': 'hidden',
                        'marginRight': '10px'
                    }
                ),
                html.Span('Photo Gallery', style={'fontSize': '20px'})
            ], style={'display': 'flex', 'alignItems': 'center'}),
            fac.AntdSwitch(
                id='theme-switch',
                checkedChildren='🌙',
                unCheckedChildren='☀️',
                style={'marginLeft': 'auto'}
            )
        ],
        style={'padding': '10px', 'display': 'flex', 'alignItems': 'center'}
    ),
    # 内容区
    html.Div(id='page-content', style={'padding': '20px', 'textAlign': 'center'})
], style={'minHeight': '100vh'})

# 添加一个新的回调来获取当前主题状态
@app.callback(
    Output('theme-status', 'data'),
    Input('theme-switch', 'checked')
)
def update_theme_status(is_dark_mode):
    return is_dark_mode

# 回调函数用于切换主题
@app.callback(
    [Output('main-container', 'style'),
     Output('navbar', 'style'),],
    Input('theme-switch', 'checked')
)
def toggle_theme(is_dark_mode):
    if is_dark_mode:
        common_style = {
            'backgroundColor': '#1c1c1e',
            'color': 'white',
            'minHeight': '100vh',
            'backgroundImage': 'linear-gradient(135deg, #1c1c1e 0%, #2c2c2e 100%)'
        }
        navbar_style = {
            'backgroundColor': '#1c1c1e',
            'color': 'white',
            'backgroundImage': 'linear-gradient(135deg, #1c1c1e 0%, #2c2c2e 100%)'
        }

    else:
        common_style = {
            'backgroundColor': '#f0f2f5',
            'color': 'black',
            'minHeight': '100vh',
            'backgroundImage': 'linear-gradient(135deg, #f0f2f5 0%, #ffffff 100%)'
        }
        navbar_style = {
            'backgroundColor': '#f0f2f5',
            'color': 'black',
            'backgroundImage': 'linear-gradient(135deg, #f0f2f5 0%, #ffffff 100%)'
        }

    return common_style, {**navbar_style, 'padding': '10px', 'display': 'flex', 'alignItems': 'center'}


def album_card_style(is_dark_mode):
    if is_dark_mode:
        card_style = {
            'backgroundColor': 'rgba(40, 40, 40, 0.9)',  # 更深的背景色
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.3)',  # 更柔和的阴影
            'border': 'none',  # 去掉边框
            'borderRadius': '8px',
            'color': 'white'  # 文字颜色为白色
        }
    else:
        card_style = {
            'backgroundColor': 'rgba(255, 255, 255, 0.4)',  # 原有的背景色
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',  # 原有的阴影
            'borderRadius': '8px',
            'color': 'black'  # 文字颜色为黑色
        }
    
    return card_style
@app.callback(
    [Output('navbar', 'children')],
    [Input('url', 'pathname')]
)
def update_navbar(pathname):
    if pathname == '/':
        return [html.Div([
            fac.AntdImage(
                src=config.LOGO_PATH,
                preview=False,
                style={
                    'height': '30px',
                    'width': '30px',
                    'borderRadius': '50%',
                    'overflow': 'hidden',
                    'marginRight': '10px'
                }
            ),
            html.Span('Photo Gallery', style={'fontSize': '20px'}),
            fac.AntdSwitch(
                id='theme-switch',
                checkedChildren='🌙',
                unCheckedChildren='☀️',
                style={'marginLeft': 'auto'}
            )
        ], style={'display': 'flex', 'alignItems': 'center', 'width': '100%'})]
    else:
        album_name = unquote(pathname.strip('/'))
        return [html.Div([
            fac.AntdBreadcrumb(
                items=[
                    {'title': '主页', 'href': '/'},
                    {'title': album_name}
                ],
                style={'marginBottom': '0'}
            ),
            fac.AntdSwitch(
                id='theme-switch',
                checkedChildren='🌙',
                unCheckedChildren='☀️',
                style={'marginLeft': 'auto'}
            )
        ], style={'display': 'flex', 'alignItems': 'center', 'width': '100%'})]

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname'), Input('theme-status', 'data')]
)
def display_page(pathname, is_dark_mode):
    with open('albums.json', 'r', encoding='utf-8') as f:
        albums_data = json.load(f)
        
    card_style = album_card_style(is_dark_mode=is_dark_mode)

    if pathname == '/':
        return html.Div([
            dcc.Link([
                fac.AntdCard(
                        fac.AntdCardMeta(
                            description=album['desc'],
                            title=album['title'],
                        ),
                        coverImg={
                            'alt': 'demo picture',
                            'src': album['images'][0],
                        },
                        hoverable=True,
                        style={**card_style, 'height': '400px', 'margin': '10px', 'display': 'inline-block'},
                        headStyle={'display':'none'},
                )
            ],
            href=f'/{album_name}'
            )
            for album_name, album in albums_data.items()
        ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(auto-fill, minmax(300px, 1fr))', 'gap': '20px', 'justifyContent': 'center'})
    else:
        album_name = unquote(pathname.strip('/'))
        if album_name in albums_data:
            album = albums_data[album_name]
            return html.Div([
                html.H2(album['title'], style={'textAlign': 'center'}),
                html.P(album['desc'], style={'textAlign': 'center', 'marginBottom': '40px'}),
                fac.AntdRow(
                    [
                        fac.AntdCol(
                            fac.AntdImage(
                                src=image_url,
                                preview=True,
                                style={'width': '100%', 'marginBottom': '10px'}
                            ),
                            span=6  # 这里可以根据需要调整列宽
                        )
                        for image_url in album['images']
                    ],
                    gutter=[16, 16],  # 设置网格间距
                    justify='center'
                )
            ])
        else:
            return html.Div("相册未找到", style={'color': 'red'})
        
        

if __name__ == '__main__':
    app.run_server(debug=True)
