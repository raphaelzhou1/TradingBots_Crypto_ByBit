import os
import json
import requests
import time
import datetime
import pandas as pd
from pconst import const
from consts import *
from client_bybit import *
from IPython.core.display import display


def get_equations_filename(symbol_str):
    return r'data/' + symbol_str.lower() + '_' + const.SUFFIX + '.csv'


def get_orders_filename(symbol_str):
    return r'data/' + symbol_str.lower() + '_' + const.ORDERS + '.csv'


def check_order_open_close(out_df, x, o_now, o_buy):
    delta1441 = out_df.at[x, const.avg1441_col_name] - out_df.at[x - 1, const.avg1441_col_name]
    delta181 = out_df.at[x, const.avg181_col_name] - out_df.at[x - 1, const.avg181_col_name]
    delta31 = out_df.at[x, const.avg31_col_name] - out_df.at[x - 1, const.avg31_col_name]
    delta7 = out_df.at[x, const.avg7_col_name] - out_df.at[x - 1, const.avg7_col_name]
    # dt = round(out_df.at[x, const.dt_col_name])
    price = out_df.at[x, const.value_col_name]

    o_change = False

    kd3d4 = price * const.d3_d4_useful_koef  # see const.py for details
    if not o_now:
        # if abs(delta1441) > kd3d4:

        if delta1441 > 0 and delta181 > 0 and delta31 > 0 and delta7 > 0:
            o_change = True
            o_now = True
            o_buy = True
            return o_now, o_buy, o_change

        if delta1441 < 0 and delta181 < 0 and delta31 < 0 and delta7 < 0:
            o_change = True
            o_now = True
            o_buy = False
            return o_now, o_buy, o_change

    else:
        # if abs(delta1441) < kd3d4:
        #     o_change = True
        #     o_now = False
        #     return o_now, o_buy, o_change

        if o_buy:
            if delta1441 < 0 and delta181 < 0 and delta31 < 0 and delta7 < 0:
                o_change = True
                o_now = False
                return o_now, o_buy, o_change
        else:
            if delta1441 > 0 and delta181 > 0 and delta31 > 0 and delta7 > 0:
                o_change = True
                o_now = False
                return o_now, o_buy, o_change

    return o_now, o_buy, o_change


def fill_equation_values(out_df, x, o_now, o_buy, mean_value, min_value, max_value):
    if o_now:
        if o_buy:
            out_df.at[x, const.order_col_name] = max_value
        else:
            out_df.at[x, const.order_col_name] = min_value
    else:
        out_df.at[x, const.order_col_name] = mean_value

    return out_df


def fill_order_values(
        ord_df, o_open, o_buy,
        open_order_id, beg_dt, beg_val,
        close_order_id, end_dt, end_val,
        qty, qty_in_usd
):
    len = ord_df[const.type_col_name].size
    if o_open:
        pos = len  # add new row
    else:
        pos = len - 1  # insert values into last row

    if o_open:
        if o_buy:
            ord_df.at[pos, const.type_col_name] = const.order_side_buy
        else:
            ord_df.at[pos, const.type_col_name] = const.order_side_sell

        ord_df.at[pos, const.open_ord_id_col_name] = open_order_id
        ord_df.at[pos, const.open_dt_col_name] = beg_dt
        ord_df.at[pos, const.open_price_col_name] = beg_val

        ord_df.at[pos, const.close_ord_id_col_name] = ' '
        ord_df.at[pos, const.close_dt_col_name] = 0.0
        ord_df.at[pos, const.close_price_col_name] = 0.0
        ord_df.at[pos, const.delta_price_col_name] = 0.0
        ord_df.at[pos, const.delta_price_prc_col_name] = 0.0
        ord_df.at[pos, const.profit_col_name] = 0.0
        ord_df.at[pos, const.profit_prc_col_name] = 0.0
        ord_df.at[pos, const.sum_profit_col_name] = 0.0
        ord_df.at[pos, const.sum_profit_prc_col_name] = 0.0
        ord_df.at[pos, const.qty_col_name] = 0.0
        ord_df.at[pos, const.qty_in_usd_col_name] = 0.0
    else:
        ord_df.at[pos, const.close_ord_id_col_name] = close_order_id
        ord_df.at[pos, const.close_dt_col_name] = end_dt
        ord_df.at[pos, const.close_price_col_name] = end_val
        ord_df.at[pos, const.qty_col_name] = qty
        ord_df.at[pos, const.qty_in_usd_col_name] = qty_in_usd

        if o_buy:
            d_price = end_val - beg_val
        else:
            d_price = beg_val - end_val

        d_price_prc = (d_price / beg_val) * 100.0
        p_prc = d_price_prc - 0.4
        p = (p_prc / 100.0) * beg_val

        ord_df.at[pos, const.delta_price_col_name] = d_price
        ord_df.at[pos, const.delta_price_prc_col_name] = d_price_prc
        ord_df.at[pos, const.profit_col_name] = p
        ord_df.at[pos, const.profit_prc_col_name] = p_prc

        prev = pos - 1
        if prev >= 0:
            ord_df.at[pos, const.sum_profit_col_name] = ord_df.at[prev, const.sum_profit_col_name] + p
            ord_df.at[pos, const.sum_profit_prc_col_name] = ord_df.at[prev, const.sum_profit_prc_col_name] + p_prc
        else:
            ord_df.at[pos, const.sum_profit_col_name] = p
            ord_df.at[pos, const.sum_profit_prc_col_name] = p_prc

    return ord_df


def get_curr_prev5_minute_utc():
    curr_datetime = datetime.datetime.now()
    curr_datetime = datetime.datetime(
        curr_datetime.year, curr_datetime.month, curr_datetime.day, curr_datetime.hour, curr_datetime.minute, 0)
    prev_datetime = curr_datetime - datetime.timedelta(minutes=5)
    c_utc = curr_datetime.timestamp()
    p_utc = prev_datetime.timestamp()
    return c_utc, p_utc


def check_for_order_open(ord_df):
    open_order_id = ''
    len = ord_df[const.type_col_name].size
    if len <= 0:
        order_now = False
        order_buy = False
        beg_dt = 0.0
        beg_val = 0.0
    else:
        pos = len - 1

        close_dt = ord_df.at[pos, const.close_dt_col_name]
        ord_type = ord_df.at[pos, const.type_col_name]
        if close_dt == 0.0:  # last order not closed
            order_now = True
            if ord_type == const.order_side_buy:
                order_buy = True
            else:
                order_buy = False
            open_order_id = ord_df.at[pos, const.open_ord_id_col_name]
            beg_dt = ord_df.at[pos, const.open_dt_col_name]
            beg_val = ord_df.at[pos, const.open_price_col_name]
        else:
            order_now = False
            order_buy = False
            open_order_id = ''
            beg_dt = 0.0
            beg_val = 0.0

    return order_now, order_buy, open_order_id, beg_dt, beg_val


def check_and_close_when_autoclosed(out_df, ord_df, symbol, order_buy, open_order_id, beg_dt, beg_val, x):
    if order_buy:
        position_exists = client_position_check(const.order_side_buy, symbol)
    else:
        position_exists = client_position_check(const.order_side_sell, symbol)

    if not position_exists:
        end_dt = out_df.at[x, const.dt_col_name]
        end_val = out_df.at[x, const.value_col_name]

        ord_df = fill_order_values(
            ord_df, False, order_buy, open_order_id, beg_dt, beg_val,
            '1.1', end_dt, end_val, 1.1, 1.1
        )
        return True, ord_df

    return False, ord_df


def update_eq_order(out_df, ord_df, symbol, qty_in_usd):
    out_len = out_df[const.dt_col_name].size
    x = out_len - 1

    curr_min_utc, prev5_min_utc = get_curr_prev5_minute_utc()
    last_dt_utc = out_df.at[x, const.dt_col_name]

    last_dt = datetime.datetime.fromtimestamp(last_dt_utc).strftime(const.TIME_FORMAT)
    curr_min_dt = datetime.datetime.fromtimestamp(curr_min_utc).strftime(const.TIME_FORMAT)

    print('..[' + last_dt + ',' + curr_min_dt + '].', end='')

    ord_change = False
    order_now, order_buy, open_order_id, beg_dt, beg_val = check_for_order_open(ord_df)

    mean_value = out_df[const.value_col_name].mean()
    min_value = out_df[const.value_col_name].min()
    max_value = out_df[const.value_col_name].max()

    out_df.at[0, const.order_col_name] = mean_value
    out_df.at[1, const.order_col_name] = mean_value

    order_now, order_buy, ord_change = check_order_open_close(out_df, x, order_now, order_buy)

    if ord_change and not order_now:  # not close if closed
        auto_closed, ord_df = check_and_close_when_autoclosed(
            out_df, ord_df, symbol, order_buy, open_order_id, beg_dt, beg_val, x)
        ord_change = not auto_closed

    #   out_df = fill_equation_values(out_df, x, order_now, order_buy, mean_value, min_value, max_value)

    if ord_change:
        if order_now:
            if order_buy:
                order_buy_str = const.order_side_buy
            else:
                order_buy_str = const.order_side_sell

            beg_val = out_df.at[x, const.value_col_name]

            success_open, open_order_id, beg_dt, qty, qty_in_usd, beg_val = \
                client_position_open(order_buy_str, symbol, qty_in_usd, beg_val)

            if success_open:
                ord_df = fill_order_values(
                    ord_df, order_now, order_buy, open_order_id, beg_dt, beg_val, ' ', 0.0, 0.0, qty, qty_in_usd
                )
        else:
            if order_buy:
                order_buy_str = const.order_side_buy
            else:
                order_buy_str = const.order_side_sell

            end_val = out_df.at[x, const.value_col_name]

            success_close, close_order_id, end_dt, qty, qty_in_usd, end_val = \
                client_position_close(order_buy_str, symbol, qty_in_usd, end_val)

            if success_close:
                ord_df = fill_order_values(
                    ord_df, order_now, order_buy, open_order_id, beg_dt, beg_val,
                    close_order_id, end_dt, end_val, qty, qty_in_usd
                )

    return out_df, ord_df


def update_orders_by_symbol(symbol_str, qty_in_usd):
    print('Update orders ' + symbol_str + ' ', end='')

    eq_file_name = get_equations_filename(symbol_str)
    eq_df = pd.read_csv(eq_file_name)
    print('..load eq.', end='')

    ord_file_name = get_orders_filename(symbol_str)
    if os.path.exists(ord_file_name):
        ord_df = pd.read_csv(ord_file_name)
    else:
        ord_df = pd.DataFrame(columns=[const.type_col_name,
                                       const.open_ord_id_col_name, const.open_dt_col_name, const.open_price_col_name,
                                       const.close_ord_id_col_name, const.close_dt_col_name, const.close_price_col_name,
                                       const.qty_col_name, const.qty_in_usd_col_name,
                                       const.delta_price_col_name, const.delta_price_prc_col_name,
                                       const.profit_col_name, const.profit_prc_col_name,
                                       const.sum_profit_col_name, const.sum_profit_prc_col_name])
    print('..load ord.', end='')

    eq_df, ord_df = update_eq_order(eq_df, ord_df, symbol_str, qty_in_usd)
    print('..update ord.', end='')

    ord_df.to_csv(ord_file_name, index=False, header=True)
    print('..save ord.', end='')

    eq_df.to_csv(eq_file_name, index=False, header=True)
    print('..save eq.', end='')

    print('Completed !')
