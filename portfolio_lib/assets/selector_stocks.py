"""File used to set HTML Selectors related to Stocks in Status Invest."""

CURRENT_PRICE_SELECTOR = r"#main-2 > div:nth-child(4) > div > div.pb-3.pb-md-5 > div > div.info.special.w-100.w-md-33.w-lg-20 > div > div:nth-child(1) > strong"
CURRENT_PRICE_CHANGE_SELECTOR = r"#main-2 > div:nth-child(4) > div > div.pb-3.pb-md-5 > div > div.info.special.w-100.w-md-33.w-lg-20 > div > div.w-lg-100 > span > b"

MIN_PRICE_CURRENT_MONTH_SELECTOR = r"#main-2 > div:nth-child(4) > div > div.pb-3.pb-md-5 > div > div:nth-child(2) > div > div.d-flex.justify-between > div > span.sub-value"
MAX_PRICE_CURRENT_MONTH_SELECTOR = r"#main-2 > div:nth-child(4) > div > div.pb-3.pb-md-5 > div > div:nth-child(3) > div > div.d-flex.justify-between > div > span.sub-value"
PRICE_CHANGE_MONTH_SELECTOR = r"#main-2 > div:nth-child(4) > div > div.pb-3.pb-md-5 > div > div:nth-child(5) > div > div.d-flex.justify-between > div > span.sub-value > b"

MIN_PRICE_52W_SELECTOR = r"#main-2 > div:nth-child(4) > div > div.pb-3.pb-md-5 > div > div:nth-child(2) > div > div:nth-child(1) > strong"
MAX_PRICE_52W_SELECTOR = r"#main-2 > div:nth-child(4) > div > div.pb-3.pb-md-5 > div > div:nth-child(3) > div > div:nth-child(1) > strong"
PRICE_CHANGE_12M_SELECTOR = r"#main-2 > div:nth-child(4) > div > div.pb-3.pb-md-5 > div > div:nth-child(5) > div > div:nth-child(1) > strong"

DIVIDEND_YIELD_SELECTOR = r"#main-2 > div:nth-child(4) > div > div.pb-3.pb-md-5 > div > div:nth-child(4) > div > div:nth-child(1) > strong"
DIVIDEND_12_MONTH_SELECTOR = r"#main-2 > div:nth-child(4) > div > div.pb-3.pb-md-5 > div > div:nth-child(4) > div > div.d-flex.justify-between > div > span.sub-value"

P_L_SELECTOR = r"#indicators-section > div.indicator-today-container > div > div:nth-child(1) > div > div:nth-child(2) > div > div > strong"
P_VP_SELECTOR = r"#indicators-section > div.indicator-today-container > div > div:nth-child(1) > div > div:nth-child(4) > div > div > strong"
VPA_SELECTOR = r"#indicators-section > div.indicator-today-container > div > div:nth-child(1) > div > div:nth-child(9) > div > div > strong"
LPA_SELECTOR = r"#indicators-section > div.indicator-today-container > div > div:nth-child(1) > div > div:nth-child(11) > div > div > strong"

STOCKS_HTML_SELECTOR_DICT = {
    "Valor atual": CURRENT_PRICE_SELECTOR,
    "Variação no dia": CURRENT_PRICE_CHANGE_SELECTOR,
    "Min. no mês": MIN_PRICE_CURRENT_MONTH_SELECTOR,
    "Máx. no mês": MAX_PRICE_CURRENT_MONTH_SELECTOR,
    "Variação no mês": PRICE_CHANGE_MONTH_SELECTOR,
    "Min. 52 semanas": MIN_PRICE_52W_SELECTOR,
    "Máx. 52 semanas": MAX_PRICE_52W_SELECTOR,
    "Variação 12 meses": PRICE_CHANGE_12M_SELECTOR,
    "Dividend yield": DIVIDEND_YIELD_SELECTOR,
    "Dividendos 12 meses": DIVIDEND_12_MONTH_SELECTOR,
    "P/L": P_L_SELECTOR,
    "P/VP": P_VP_SELECTOR,
    "VPA": VPA_SELECTOR,
    "LPA": LPA_SELECTOR,
}
