import random 
def generate_dummy_data(sensor_names: list[str]) -> dict[str, float]:
	random_values = [random.random() for _ in sensor_names]
	
	return {s: r for s, r in zip(sensor_names, random_values)}



