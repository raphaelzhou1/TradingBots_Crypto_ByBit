import os
from pconst import const

const.START_UTC = 1624225585

const.TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

const.BTCUSDT    = 'BTCUSDT'
const.AAVEUSDT   = 'AAVEUSDT'
const.ADAUSDT    = 'ADAUSDT'
const.BCHUSDT    = 'BCHUSDT'
const.DOGEUSDT   = 'DOGEUSDT'
const.DOTUSDT    = 'DOTUSDT'
const.ETHUSDT    = 'ETHUSDT'
const.LINKUSDT   = 'LINKUSDT'
const.LTCUSDT    = 'LTCUSDT'
const.SUSHIUSDT  = 'SUSHIUSDT'
const.XRPUSDT    = 'XRPUSDT'
const.XEMUSDT    = 'XEMUSDT'
const.XTZUSDT    = 'XTZUSDT'
const.UNIUSDT    = 'UNIUSDT'

const.SUFFIX = 'equations'
const.ORDERS = 'orders'

const.avg8_wnd = 7
const.avg32_hwnd = 31
const.avg48_hwnd = 47
const.avg64_hwnd = 63
const.avg96_hwnd = 95
const.avg128_hwnd = 127

const.avgS_hwnd = 599

const.check_extremum_wnd = 32

const.open_col_name = 'open'
const.close_col_name = 'close'

const.dt_col_name = 'dt'
const.value_col_name = 'value'
const.delta1_col_name = 'delta1'
const.delta2_col_name = 'delta2'
const.avg8_col_name = 'avg8'
const.avg32_col_name = 'avg32'
const.avg48_col_name = 'avg48'
const.avg64_col_name = 'avg64'
const.avg96_col_name = 'avg96'
const.avg128_col_name = 'avg128'
const.avg_fast_col_name = 'avg_fast'
const.avg_slow_col_name = 'avg_slow'
const.order_col_name = 'order'

const.type_col_name = 'type'
const.open_ord_id_col_name = 'open_ord_id'
const.open_dt_col_name = 'open_dt'
const.open_price_col_name = 'open_price'
const.close_ord_id_col_name = 'close_ord_id'
const.close_dt_col_name = 'close_dt'
const.close_price_col_name = 'close_price'
const.qty_col_name = 'qty'
const.qty_in_usd_col_name = 'qty_in_usd'
const.delta_price_col_name = 'delta_price'
const.delta_price_prc_col_name = 'delta_price_prc'
const.profit_col_name = 'profit'
const.profit_prc_col_name = 'profit_prc'
const.sum_profit_col_name = 'sum_profit'
const.sum_profit_prc_col_name = 'sum_profit_prc'

const.order_status_created = 'Created'
const.order_status_rejected = 'Rejected'
const.order_status_new = 'New'
const.order_status_partially_filled = 'PartiallyFilled'
const.order_status_filled = 'Filled'
const.order_status_cancelled = 'Cancelled'
const.order_status_pendingCancel = 'PendingCancel'

const.order_type_limit = 'Limit'
const.order_type_market = 'Market'

const.order_side_buy = 'Buy'
const.order_side_sell = 'Sell'

const.order_time_in_force_good_till_cancel = 'GoodTillCancel'
const.order_time_in_force_immediate_or_cancel = 'ImmediateOrCancel'
const.order_time_in_force_fill_or_kill = 'FillOrKill'
const.order_time_in_force_post_only = 'PostOnly'

const.order_stop_lost_koef_buy = 0.975
const.order_stop_lost_koef_sell = 1.025
const.max_avg_error = 0.01

const.order_take_profit_koef_buy = 1.03
const.order_take_profit_koef_sell = 0.97

const.order_create_plus_koef_buy = 1.001
const.order_create_plus_koef_sell = 0.999

# |d3+d4| must be > (1% of price per 1 hour) = (1/60)*(price/100) = price * (1/6000))
# delta calulates per minute
# 1% per 1 hour = 1/60
# abs(d3 + d4) > price * 0.000167
# 0.000047
const.d3_d4_useful_koef = 0.000167
