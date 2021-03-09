from math import log, isclose
from .dryair import da_heat_capacity
from .water import * # Пересмотреть импорт что бы не импортить namedtuple
import exceptions.ExceptionPO

__all__ = ['humidity_ratio',
		   'humidity_ratio_by_enthalpy',
		   'humid_air_enthalpy',
		   'relative_humidity',
		   'dew_point_temperature',
           'wet_bulb_temperature',
		   'partial_pressure_of_vapor',
		   'humid_air_entropy',
           'humid_air_exergy',
		   'humidity_ratio_by_entropy',
           'isentropic_proc_temperature'
		  ]
# Молярная масса водяного пара
R_w = 18.016
# Молярная масса воздуха
R_a = 28.96
# перевод в Цельсии в Кельвины
c_to_K = lambda t : 273.15 + t

# Функция для расчета влагосодержания воздуха возвращает температуру и влагосодержание
# p - давление окружающей среды
# t - температура влажного воздуха
# R - отностительная влажность от 0 до 1
def humidity_ratio(p_input, t_input, RInput):
    # Некорректная передача значения R - выход из функции без дальнейшего расчета
    if RInput < 0 or RInput > 1 :
        print('R : выходит за предел от 0 до 1')
        return
    # Достижение и превышение давления насыщеия (кипения воды)
    if (water_saturated_pressure(t_input)) >= p_input and RInput != 1.0 :
        return (R_w / R_a) * ((RInput * p_input) / (p_input - RInput * p_input))

    return (R_w / R_a) * ((RInput * water_saturated_pressure(t_input)) / (p_input - RInput * water_saturated_pressure(t_input)))


# Функция для расчета влагосодержания
# p - давление окружающей среды в Па
# t - температура влажного воздуха
# R - энтальпия
def humidity_ratio_by_enthalpy(t_input, p_input, hInput) :
    dOut = 0

    if water_saturated_pressure(t_input) >= p_input :
        if t_input >= 0.02 :
            dOut = (hInput - da_heat_capacity(t_input, p_input) * t_input) / (
                    water_l_heat_capacity(water_saturated_temperature(p_input)) *
                    water_saturated_temperature(p_input) +
                    water_heat_of_evaporation(water_saturated_temperature(p_input)) +
                    water_v_heat_capacity(t_input) * (t_input - water_saturated_temperature(p_input)))
        else :
            dOut = (hInput - da_heat_capacity(t_input, p_input) * t_input) / (
                    water_i_heat_capacity() * t_input - heat_of_melt() +
                    heat_of_sublimation())
    else :
        if t_input >= 0.02 :
            dOut = (hInput - da_heat_capacity(t_input, p_input) * t_input) / (
                    water_l_heat_capacity(t_input) * t_input + water_heat_of_evaporation(t_input))
        else :
            dOut = (hInput - da_heat_capacity(t_input, p_input) * t_input) / (
                    water_i_heat_capacity() * t_input - heat_of_melt() + heat_of_sublimation())
    return dOut


def humid_air_enthalpy(t_input, p_input, d_input):
    if relative_humidity(d_input, t_input, p_input) * (water_saturated_pressure(dew_point_temperature(p_input, d_input))) \
            < (water_saturated_pressure(dew_point_temperature(p_input, d_input))):

        if dew_point_temperature(p_input, d_input) >= 0.02 :
            hOut = da_heat_capacity(t_input, p_input) * t_input + d_input * \
                   (water_l_heat_capacity(dew_point_temperature(p_input, d_input)) *
                    dew_point_temperature(p_input, d_input) +
                    water_heat_of_evaporation((dew_point_temperature(p_input, d_input))) +
                    water_v_heat_capacity((t_input + dew_point_temperature(p_input, d_input) * 0.5)) *
                    (t_input - dew_point_temperature(p_input, d_input)))
            
        else :
            hOut = da_heat_capacity(t_input, p_input) * t_input + d_input * (
                    water_i_heat_capacity() * dew_point_temperature(p_input, d_input) - heat_of_melt() +
                    heat_of_sublimation() + water_v_heat_capacity(
                (t_input + dew_point_temperature(p_input, d_input) * 0.5)) * (
                                t_input - dew_point_temperature(p_input, d_input)))
    else :
        if dew_point_temperature(p_input, d_input) >= 0.02 and t_input > 0:
            hOut = da_heat_capacity(t_input, p_input) * t_input + d_input * (
                    water_l_heat_capacity(t_input) * t_input + water_heat_of_evaporation(t_input))

        else :
            hOut = da_heat_capacity(t_input, p_input) * t_input + d_input * (
                    water_i_heat_capacity() * t_input - heat_of_melt() + heat_of_sublimation())
    return hOut


# Функция для определения относительной влажности
def relative_humidity(d_input, t_input, p_input):
    return (p_input * d_input) / (water_saturated_pressure(t_input) * ((R_w / R_a) + d_input))


def dew_point_temperature(p_input, d_input) -> 'Возвращает значение волагосодержания':
    '''
    | Функция для нахождения температуры точк'и росы
    | p_input - давление в Па
    | d_input - влагосодержание в кг/кг
    '''
    p_s = (d_input * p_input) / 1 / (0.622 + d_input)
    return water_saturated_temperature(p_s)
	
def wet_bulb_temperature(p_input, t_input, d_input):
    h_input = humid_air_enthalpy(t_input, p_input, d_input)
    h = humid_air_enthalpy(dew_point_temperature(p_input, d_input), p_input, d_input)
    d = d_input

    while not isclose(h_input, h, abs_tol=1):
        d += 0.001
        wb_t = dew_point_temperature(p_input, d)
        h = humid_air_enthalpy(wb_t, p_input, d)
    else:
        return wb_t
# Функция парциальное давлене водяного пара
# p_input - полное давление в Па
# d_input - влагосодержание в кг/кг
# RInput - относительная влажность безразмер.
def partial_pressure_of_vapor(p_input, d_input, RInput):
    p = (d_input * (p_input)) / (0.622 + d_input)
    if p > p_input :
        p = round(p_input, 3)
    return p

# Расчет энтпроии влажного воздуха
def humid_air_entropy(t_input, p_input, v_param, type_param):
    p_0 = 101325
    T_0 = 273.15
    if type_param == 'R' :
        s_out = da_heat_capacity(t_input, p_input) * log((c_to_K(t_input)) / T_0) - \
               0.287 * log(((p_input) - v_param * water_saturated_pressure(t_input)) / (p_0)) \
               + humidity_ratio(p_input, t_input, v_param) * ((2500.64 / T_0)
               + water_v_heat_capacity(t_input) * log((c_to_K(t_input)) / T_0) -
               0.4615 * log((v_param * water_saturated_pressure(t_input)) / 610))
        return s_out
    if type_param == 'd' :
        s_out = da_heat_capacity(t_input, p_input) * log(c_to_K(t_input) / T_0) - \
               0.287 * log((p_input - relative_humidity(v_param, t_input, p_input)
               * water_saturated_pressure(t_input)) / p_0) + v_param * ((2500.64 / T_0) +
               water_v_heat_capacity(t_input) * log((c_to_K(t_input)) / T_0) -
               0.4615 * log((relative_humidity(v_param, t_input, p_input) *
               water_saturated_pressure(t_input)) / 610))
        return s_out
		
def humidity_ratio_by_entropy(t_input, p_input, RInput, s_input):
    p_0 = 101325
    T_0 = 273.15
    dOut = (s_input - da_heat_capacity(t_input, p_input) * log((c_to_K(t_input)) / T_0) +
            0.287 * log((p_input - RInput * water_saturated_pressure(t_input)) / p_0))/\
           ((2500.64 / T_0)+ water_v_heat_capacity(t_input) * log((c_to_K(t_input)) / T_0)
            - 0.4615 * log((RInput * water_saturated_pressure(t_input)) / 610))
    return dOut
	
def humid_air_exergy(t_input, p_input, d_input, tInputRef, pInputRef, dInputRef):
    e = (273.15 + tInputRef) * ((da_heat_capacity(t_input, p_input) +
        d_input * water_v_heat_capacity(t_input)) *
        ((c_to_K(t_input) / (c_to_K(tInputRef))) - 1 - log(c_to_K(t_input) / c_to_K(tInputRef))) +
        0.4615 * ((0.622 + d_input) * log((p_input * (0.622 + dInputRef)) / (pInputRef * (0.622 + d_input))) +
        d_input * log(d_input / dInputRef)))
    return e
# Проекция точки на поверхность при постоянной энтропии
def find_t(p_input, s_input, t_begin = -72.26, t_step = 0.01):
    _R = 1
    while True :
        s_out = da_heat_capacity(t_begin, p_input) * log(c_to_K(t_begin) / 273.15) -\
        0.287 * log(((p_input) - _R * water_saturated_pressure(t_begin)) / (p_input  - 610)) +\
        humidity_ratio(p_input, t_begin, _R) * ((2500.64 / 273.15) + water_v_heat_capacity(t_begin) *
        log((c_to_K(t_begin)) / 273.15) - 0.4615 * log((_R * water_saturated_pressure(t_begin)) / 610))
        t_begin += t_step
        if isclose(s_out, s_input, rel_tol=0.001) :
            return t_begin
def isentropic_proc_temperature(s_input, p_input, d_input, t_begin = -72.26, t_step = 0.01):
    while True :
        s_out = da_heat_capacity(t_begin, p_input) * log(c_to_K(t_begin) / 273.15) -\
        0.287 * log((p_input - relative_humidity(d_input, t_begin, p_input) *
        water_saturated_pressure(t_begin)) / (101325)) + d_input * ((2500.64 / 273.15) +
        water_v_heat_capacity(t_begin) * log(c_to_K(t_begin) / 273.15) -
        0.4615 * log((relative_humidity(d_input, t_begin, p_input) * water_saturated_pressure(t_begin)) / 610))
        t_begin += t_step
        if isclose(s_out, s_input, rel_tol=0.001):
            return t_begin
