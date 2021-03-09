import os

# словарь данных теплоемкостей по давлениям и температуре
# первичный ключ давление, вторичный температура
_da_heat_capacity = {}
# Загрузка файла содержащего теплоемкости сухого воздуха по темпераутре и давлению
# данные заносяся в словарь _da_heat_capacity
file_abs_path = os.path.dirname(__file__)
# Загрузка данных теплоемкостей по давлнеию и температуре
__all__ = ['da_heat_capacity']
with open(file_abs_path + '\\tables\\DryAirHeatCapacity.dat', 'r') as f :
    p = 0
    t = 0
    c = 0
    for line in f :
        if line.startswith('#') :
            p = line.replace('#', '').replace('\n', '')
            _da_heat_capacity[float(p)] = {}
        else :
            t, c = line.replace('\n', '').split('\t')
            _da_heat_capacity[float(p)].update({float(t): float(c)})


def da_heat_capacity(tInput: 'Температура воздуха в С', 
					pInput: 'Давление воздуха в Па')-> 'Теплоемкость сухого воздуха в кДж/(кг*К)':
	pInput = pInput*10**-5
	for p in _da_heat_capacity.keys():
		if p >= pInput :
			for t in _da_heat_capacity[p] :
				if t > 1500:
					#1500 - 1.2347
					#2000 - 1.2605
					#Данные с refprop
					
					return 1.2476
				if t >= tInput :
					# давление меньшее за переданое
					p0 = list(_da_heat_capacity)[(list(_da_heat_capacity).index(p)) - 1]
					# температура меньшая за переданую
					t0 = list(_da_heat_capacity[p])[(list(_da_heat_capacity[p]).index(t)) - 1]
					# теплоемкость по меньшему давлению и меньшей температуре
					c0_p0 = _da_heat_capacity[p0][t0]
					# теплоемкость по меньшему давлению и большей температуре
					c1_p0 = _da_heat_capacity[p0][t]
					# теплоемкость по большему давлению и меньшей температуре
					c0_p1 = _da_heat_capacity[p][t0]
					# теплоемкость по большему давлению и большей температуре
					c1_p1 = _da_heat_capacity[p][t]
                    # искомая теплоемкость при заданай температуре и меньшем давлении
					c_x_p0 = c0_p0 + (
								((c1_p0 - c0_p0) * (tInput - t0)) / (t - t0))
					# искомая теплоемкость при заданой температуре и большем давлении
					c_x_p1 = c0_p1 + (
								((c1_p1 - c0_p1) * (tInput - t0)) / (t - t0))
					# искомая теплоемкось по заданому давлению и температуре
					c_x = c_x_p0 + (c_x_p1 - c_x_p0) * (pInput - p0) / (p - p0)
					return c_x