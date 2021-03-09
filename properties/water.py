import os
from collections import namedtuple
from exceptions import LowTempException, HighTempException

__all__ = ['water_v_heat_capacity',
		   'water_l_heat_capacity', 
		   'water_heat_of_evaporation',
		   'heat_of_sublimation',
		   'heat_of_melt',
		   'water_i_heat_capacity',
		   'water_saturated_pressure',
		   'water_saturated_temperature']
file_abs_path = os.path.dirname(__file__)	   
# Теплоемкость воды в жидком состоянии
_lw_heat_capacity = []
# Теплоемкость воды в парообразном состоянии
_vw_heat_capacity = []
# Теплота парообразования воды
_w_heat_of_evaporation = []
# Давление насыщенного водяного пара
_vw_saturated_pressure = []
# Загрузка данных теплоемкости водяного пара
with open(file_abs_path + '\\tables\\WaterVapourHeatCapacity.dat', 'r') as f :
	water_property = namedtuple('water_property', 't c')
	for line in f :
		line = line.replace('\n', '')
		t, p = line.split('\t')
		_vw_heat_capacity.append(water_property(float(t), float(p)))
# Загрузка данных теплоемкости воды
with open(file_abs_path + '\\tables\\WaterHeatCapacity.dat', 'r') as f :
	water_property = namedtuple('water_property', 't c')
	for line in f :
		line = line.replace('\n', '')
		t, p = line.split('\t')
		_lw_heat_capacity.append(water_property(float(t), float(p)))
# Загрузка данных давления насыщенного водяного пара
with open(file_abs_path + '\\tables\\HeatofEvaporation.dat', 'r') as f :
	water_property = namedtuple('water_property', 't r')
	for line in f :
		line = line.replace('\n', '')
		t, r = line.split('\t')
		_w_heat_of_evaporation.append(water_property(float(t), float(r)))
# Загрузка данных давления насыщенного водяного пара
with open(file_abs_path + '\\tables\\WaterVapourSaturationPressure.dat', 'r') as f :
	water_property = namedtuple('water_property', 't p')
	for line in f:
		line = line.replace('\n', '')
		t, p = line.split('\t')
		_vw_saturated_pressure.append(water_property(float(t), float(p)))
		
def water_v_heat_capacity(tInput) :
	'''
	Фукция определения значения теплоемкости водяного пара
	из таблицы зависимости t c. Значение определяется интерполяцией.
	|t1|t2|t3|
	|c1|cx|c3|
	'''
	if _vw_heat_capacity[0].t > float(tInput):
		lowtemp = LowTempException(f'\nНе удалось определить темплоемкость водяного пара.\nМинимальное значение температуры : {_vw_heat_capacity[0].t}')
		raise lowtemp
	elif _vw_heat_capacity[-1].t < float(tInput):
		hightemp = HighTempException(f'\nНе удалось определить темплоемкость водяного пара.\nМаксимальное значение температуры : {_vw_heat_capacity[-1].t}')
		raise hightemp
	
	for _water in _vw_heat_capacity :
		if _water.t >= float(tInput) :
			index = _vw_heat_capacity.index(_water)
			t1 = _vw_heat_capacity[index - 1].t
			t2 = float(tInput)
			t3 = _water.t
			cp1 = _vw_heat_capacity[index - 1].c
			cp3 = _water.c
			cpx = cp1 + (((cp3 - cp1) * (t2 - t1)) / (t3 - t1))
			return cpx

def water_l_heat_capacity(tInput):
	'''
	Фукция определения значения теплоемкости воды
	из таблицы зависимости t c. Значение определяется интерполяцией.
	|t1|t2|t3|
	|c1|cx|c3|
	'''
	if _vw_heat_capacity[0].t > float(tInput):
		lowtemp = LowTempException(f'\nНе удалось определить темплоемкость водяного пара.\nМинимальное значение температуры : {_vw_heat_capacity[0].t}')
		raise lowtemp
	elif _vw_heat_capacity[-1].t < float(tInput):
		hightemp = HighTempException(f'\nНе удалось определить темплоемкость водяного пара.\nМаксимальное значение температуры : {_vw_heat_capacity[-1].t}')
		raise hightemp
	for _water in _lw_heat_capacity :
		if _water.t >= float(tInput) :
			index = _lw_heat_capacity.index(_water)
			t1 = _lw_heat_capacity[index - 1].t
			t2 = float(tInput)
			t3 = _water.t
			cp1 = _lw_heat_capacity[index - 1].c
			cp3 = _water.c
			cpx = cp1 + (((cp3 - cp1) * (t2 - t1)) / (t3 - t1))
			return cpx
			
			
def water_heat_of_evaporation(tInput):
	'''
	Фукция определения значения теплоты парообразования воды
	из таблицы зависимости t r. Значение определяется интерполяцией.
	|t1|t2|t3|
	|r1|rx|r3|
	'''
	if _w_heat_of_evaporation[0].t > float(tInput) :
		lowtemp = LowTempException(f'\nНе удалось определить теплоту парообразования воды.\nМинимальное значение температуры : {_w_heat_of_evaporation[0].t}')
		raise lowtemp
	elif _w_heat_of_evaporation[-1].t < float(tInput) :
		hightemp = HighTempException(f'\nНе удалось определить теплоту парообразования воды.\nМаксимальное значение температуры : {_w_heat_of_evaporation[-1].t}')
		raise hightemp
	for _water in _w_heat_of_evaporation:
		if _water.t >= float(tInput) :
			index = _w_heat_of_evaporation.index(_water)
			t1 = _w_heat_of_evaporation[index - 1].t
			t2 = float(tInput)
			t3 = _water.t
			r1 = _w_heat_of_evaporation[index - 1].r
			r3 = _water.r
			rx = r1 + (((r3 - r1) * (t2 - t1)) / (t3 - t1))
			return rx

def water_saturated_pressure(tInput):
	'''
	Фукция определения значения давление насыщенного водяного пара
	из таблицы зависимости t p. Значение определяется интерполяцией.
	|t1|t2|t3|
	|p1|px|p3|
	'''
	
	if _vw_saturated_pressure[0].t > float(tInput) :
		lowtemp = LowTempException(f'\nНе удалось определить давление насыщенного водяного пара.\nМинимальное значение температуры : {_vw_saturated_pressure[0].t}')
		raise lowtemp
	if _vw_saturated_pressure[-1].t < float(tInput):
 		return 22055000
	# elif _vw_saturated_pressure[-1].t < float(tInput) :
	# 	hightemp = HighTempException(f'\nНе удалось определить давление насыщенного водяного пара.\nМаксимальное значение температуры : {_vw_saturated_pressure[-1].t}')
	# 	raise hightemp
	for _water in _vw_saturated_pressure:
		if _water.t >= float(tInput) :
			index = _vw_saturated_pressure.index(_water)
			t1 = _vw_saturated_pressure[index - 1].t
			t2 = float(tInput)
			t3 = _water.t
			p1 = _vw_saturated_pressure[index - 1].p
			p3 = _water.p
			px = p1 + (((p3 - p1) * (t2 - t1)) / (t3 - t1))
			return px

def water_saturated_temperature(pInput):
	'''
	Фукция определения значения температуры насыщенного водяного пара
	из таблицы зависимости t p. Значение определяется интерполяцией.
	|p1|p2|p3|
	|t1|tx|t3|
	'''
	if _vw_saturated_pressure[0].p > float(pInput) :
		lowtemp = LowTempException(f'\nНе удалось определить температуру насыщенного водяного пара.\nМинимальное значение давления : {_vw_saturated_pressure[0].p}')
		raise lowtemp
	elif _vw_saturated_pressure[-1].p < float(pInput) :
		hightemp = HighTempException(f'\nНе удалось определить температуру насыщенного водяного пара.\nМаксимальное значение давления : {_vw_saturated_pressure[-1].p}')
		raise hightemp
	for _water in _vw_saturated_pressure:
		if _water.p >= float(pInput) :
			index = _vw_saturated_pressure.index(_water)
			p1 = _vw_saturated_pressure[index - 1].p
			p2 = float(pInput)
			p3 = _water.p
			t1 = _vw_saturated_pressure[index - 1].t
			t3 = _water.t
			tx = t1 + (((t3 - t1) * (p2 - p1)) / (p3 - p1))
			return tx						
			
def heat_of_sublimation():
	'''
	Теплота сублимации льда
	'''
	return 2835

def heat_of_melt():
	'''
	Теплота плавления льда
	'''
	return 334.11

def water_i_heat_capacity():
	'''
	Теплоемкость льда
	'''
	return 2
