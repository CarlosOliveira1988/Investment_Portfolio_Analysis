"""File used to set HTML Selectors related to FIIs in Status Invest."""

CURRENT_PRICE_SELECTOR = r"#main-2 > div.container.pb-7 > div.top-info.d-flex.flex-wrap.justify-between.mb-3.mb-md-5 > div.info.special.w-100.w-md-33.w-lg-20 > div > div:nth-child(1) > strong"
CURRENT_PRICE_CHANGE_SELECTOR = r"#main-2 > div.container.pb-7 > div.top-info.d-flex.flex-wrap.justify-between.mb-3.mb-md-5 > div.info.special.w-100.w-md-33.w-lg-20 > div > div.w-lg-100 > span > b"

MIN_PRICE_CURRENT_MONTH_SELECTOR = r"#main-2 > div.container.pb-7 > div.top-info.d-flex.flex-wrap.justify-between.mb-3.mb-md-5 > div:nth-child(2) > div > div.d-flex.justify-between > div > span.sub-value"
MAX_PRICE_CURRENT_MONTH_SELECTOR = r"#main-2 > div.container.pb-7 > div.top-info.d-flex.flex-wrap.justify-between.mb-3.mb-md-5 > div:nth-child(3) > div > div.d-flex.justify-between > div > span.sub-value"
PRICE_CHANGE_MONTH_SELECTOR = r"#main-2 > div.container.pb-7 > div.top-info.d-flex.flex-wrap.justify-between.mb-3.mb-md-5 > div:nth-child(5) > div > div.d-flex.justify-between > div > span.sub-value > b"

MIN_PRICE_52W_SELECTOR = r"#main-2 > div.container.pb-7 > div.top-info.d-flex.flex-wrap.justify-between.mb-3.mb-md-5 > div:nth-child(2) > div > div:nth-child(1) > strong"
MAX_PRICE_52W_SELECTOR = r"#main-2 > div.container.pb-7 > div.top-info.d-flex.flex-wrap.justify-between.mb-3.mb-md-5 > div:nth-child(3) > div > div:nth-child(1) > strong"
PRICE_CHANGE_12M_SELECTOR = r"#main-2 > div.container.pb-7 > div.top-info.d-flex.flex-wrap.justify-between.mb-3.mb-md-5 > div:nth-child(5) > div > div:nth-child(1) > strong"

DIVIDEND_YIELD_SELECTOR = r"#main-2 > div.container.pb-7 > div.top-info.d-flex.flex-wrap.justify-between.mb-3.mb-md-5 > div:nth-child(4) > div > div:nth-child(1) > strong"
DIVIDEND_12_MONTH_SELECTOR = r"#main-2 > div.container.pb-7 > div.top-info.d-flex.flex-wrap.justify-between.mb-3.mb-md-5 > div:nth-child(4) > div > div.d-flex.justify-between > div > span.sub-value"

P_L_SELECTOR = None
P_VP_SELECTOR = r"#main-2 > div.container.pb-7 > div:nth-child(5) > div > div:nth-child(2) > div > div:nth-child(1) > strong"
VPA_SELECTOR = None
LPA_SELECTOR = None

FIIS_HTML_SELECTOR_DICT = {
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
