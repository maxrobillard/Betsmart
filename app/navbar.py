import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


def Navbar():
    LOGO = "/static/img/esiee.png"
    items=[
        dbc.Row([dbc.DropdownMenuItem("Kaczmarczyk Victor",href="https://www.linkedin.com/in/victor-kaczmarczyk-747a85196/",external_link=True)]),
        dbc.Row([dbc.DropdownMenuItem("Robillard Maxime",href="https://www.linkedin.com/in/maxime-robillard/",external_link=True)]),
        ]
    navbar = dbc.Nav(
                    [
                        dbc.Row([
                            dbc.Col([
                                dbc.NavItem(dbc.Col(html.A([html.Img(src=LOGO, height="50px")], href="https://www.esiee.fr"), width={"size":1},)),
                                dbc.NavItem(dbc.Col(dbc.NavbarBrand("Paris sportif sûr",), width={"size":10})),
                                ],className="nav navbar-nav pull-left"),
                            dbc.Col([
                                dbc.NavItem(dbc.NavLink("Accueil", href="/",external_link=True,)),
                                dbc.NavItem(dbc.NavLink("Recherche", href="/search",external_link=True,)),
                                dbc.NavItem(dbc.NavLink("Scrapper", href="/scrape",external_link=True,)),
                                dbc.NavItem(dbc.DropdownMenu(items,label="Auteurs",color='primary',direction="down"),style={"margin-top":"8px"})
                                ],className="nav navbar-nav pull-right")

                        ],style={"margin-left":"30px","width":"90%"})
                    ],
                    className="navbar navbar-inverse navbar-fixed-top headroom",

            )
    return navbar
