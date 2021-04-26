import os
from pconst import const

const.START_UTC = 1618174101

const.TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

const.BCHUSDT = 'BCHUSDT'
const.DOTUSDT = 'DOTUSDT'
const.LINKUSDT = 'LINKUSDT'
const.LTCUSDT = 'LTCUSDT'
const.XTZUSDT = 'XTZUSDT'

# const.BTCUSDT = 'BTCUSDT'
# const.ETHUSDT = 'ETHUSDT'
# const.ADAUSDT = 'ADAUSDT'
# const.UNIUSDT = 'UNIUSDT'

const.SUFFIX = 'equations'
const.ORDERS = 'orders'

const.avg7_hwnd = 3
const.avg31_hwnd = 15
const.avg181_hwnd = 90
const.avg1441_hwnd = 720

const.open_col_name = 'open'
const.close_col_name = 'close'

const.dt_col_name = 'dt'
const.value_col_name = 'value'
const.delta1_col_name = 'delta1'
const.delta2_col_name = 'delta2'
const.avg7_col_name = 'avg7'
const.avg31_col_name = 'avg31'
const.avg181_col_name = 'avg181'
const.avg1441_col_name = 'avg1441'
const.order_col_name = 'order'

const.type_col_name = 'type'
const.open_dt_col_name = 'open_dt'
const.open_price_col_name = 'open_price'
const.close_dt_col_name = 'close_dt'
const.close_price_col_name = 'close_price'
const.delta_price = 'delta_price'
const.delta_price_prc = 'delta_price_prc'
const.profit = 'profit'
const.profit_prc = 'profit_prc'
const.sum_profit = 'sum_profit'
const.sum_profit_prc = 'sum_profit_prc'

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

const.order_stop_lost_koef_buy = 0.99
const.order_stop_lost_koef_sell = 1.01

const.order_take_profit_koef_buy = 1.1
const.order_take_profit_koef_sell = 0.9
