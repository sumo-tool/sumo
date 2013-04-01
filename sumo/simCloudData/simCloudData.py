import random
import datetime
from sumo.core.constants import *
from sumo.simCloudData.simVariables import *


#######################
# Returns a number of non real instances
#######################
def get_instances(instances_count):

	instances_list = list()
	regions = []
	states = []
	instance_types = []
	os_types = []	

	if len(INSTANCE_REGIONS) > 0:
		regions = get_random_instance_regions(instances_count,INSTANCE_REGIONS)		         
	elif len(INSTANCE_REGIONS) == 0 and RANDOM_REGION == 1:
		for i in range(instances_count):
				regions.append(EC2_REGIONS[random.randint(0,len(EC2_REGIONS)-1)])
	
	if len(INSTANCE_OS_TYPES) > 0:
		os_types = get_random_instance_os_types(instances_count,INSTANCE_OS_TYPES)
	elif len(INSTANCE_OS_TYPES) == 0 and RANDOM_OS_TYPE == 1:
		for i in range(instances_count):
			os_types.append(EC2_OS_TYPES[random.randint(0,len(EC2_OS_TYPES)-1)])

	if len(INSTANCE_TYPES) > 0:
		instance_types = get_random_instance_types(instances_count,INSTANCE_TYPES)
	elif len(INSTANCE_TYPES) == 0 and RANDOM_TYPE == 1:		
		for i in range(instances_count):
			instance_types.append(EC2_INSTANCE_TYPES[random.randint(0,len(EC2_INSTANCE_TYPES)-1)])

	if len(INSTANCE_STATES) > 0:
		states = get_random_instance_states(instances_count,INSTANCE_STATES)

	for i in range(instances_count):
	
		inst = {}
		inst['id'] = "i-sim%s"%i
		
		if len(regions) > 0:
			inst['region'] = regions[i]
		else:
			inst['region'] = DEFAULT_REGION

		if len(states) > 0:
			inst['state'] = states[i]
		else:
			inst['state'] = DEFAULT_STATE

		if len(os_types) > 0:
			inst['os'] = os_types[i]
		else:		
			inst['os'] = DEFAULT_OS_TYPE

		if len(instance_types) > 0:		
			inst['type'] = instance_types[i]
		else:		
			inst['type'] = DEFAULT_TYPE

		instances_list.append(inst)

	return instances_list


#######################
# Returns non real aws instance statistics
#######################
def get_instance_metric(start, end, step_size, metric_name, usage_category, instance_id):

	datapoints = []     
	stamp = start  
	limits = USAGE_LIMITS[usage_category]

	while stamp < end:
           
		stamp = stamp + datetime.timedelta(seconds=step_size)

		if metric_name=="CPUUtilization":
			value = random.uniform(limits[0],limits[1])
		else:
			value = random.uniform(limits[0],limits[1])*BYTES_UNIT

		parts = str(stamp).split(" ")
		da = parts[0].split("-")
		te = parts[1].split(":")

		stamp_datetime="datetime.datetime(%s,%s,%s,%s,%s)"%(da[0],da[1],da[2],te[0],te[1]) 
          
		datapoints.append( { "Timestamp": stamp_datetime , "Average": value, "Minimum": value , "Maximum": value, "Unit": str(UNIT_OF_METRIC[metric_name]),"id":str(instance_id) } )               

	return datapoints


#######################
# Returns number of instances' os types with percentage of each type based on percent_array
#######################
def get_random_instance_os_types(number, percent_array):

	os_types = []
	types = []

	if len(EC2_OS_TYPES) != len(percent_array):
		print "Wrong length of percent_array arguments. Should match EC2_OS_TYPE's length."            
		return []
        
	for pid in range(len(EC2_OS_TYPES)):
		for i in range(int(number*percent_array[pid])):
			os_types.append(EC2_OS_TYPES[pid])

	for i in range(len(os_types)):
		index = int(random.uniform(0,len(os_types)-1))
		types.append(os_types[index])
		os_types.pop(index)

	return types 


#######################
# Returns number of instances' regions with percentage of each region based on percent_array
#######################
def get_random_instance_regions(number, percent_array):

	init_regions = []
	regions = []
      
	if len(EC2_REGIONS) != len(percent_array):
		print "Wrong length of percent_array arguments. Should match EC2_REGIONS's length."            
		return []
        
	for pid in range(len(EC2_REGIONS)):
		for i in range(int(number*percent_array[pid])):
			init_regions.append(EC2_REGIONS[pid])

	for i in range(len(init_regions)):
		index = int(random.uniform(0,len(init_regions)-1))
		regions.append(init_regions[index])
		init_regions.pop(index)

	return regions 


#######################
# Returns number of instances' types with percentage of each type based on percent_array
#######################
def get_random_instance_types(number, percent_array):

	init_types = []
	types = []
      
	if len(EC2_INSTANCE_TYPES) != len(percent_array):
		print "Wrong length of percent_array arguments. Should match EC2_INSTANCE_TYPES's length."            
		return []
        
	for pid in range(len(EC2_INSTANCE_TYPES)):
		for i in range(int(number*percent_array[pid])):
			init_types.append(EC2_INSTANCE_TYPES[pid])

	for i in range(len(init_types)):
		index = int(random.uniform(0,len(init_types)-1))
		types.append(init_types[index])
		init_types.pop(index)

	return types 


#######################
# Returns number of instances' states with percentage of each state based on percent_array
#######################
def get_random_instance_states(number, percent_array):

	init_states = []
	states = []
      
	if len(EC2_INSTANCE_STATES) != len(percent_array):
		print "Wrong length of percent_array arguments. Should match EC2_INSTANCE_STATES's length."            
		return []
        
	for pid in range(len(EC2_INSTANCE_STATES)):
		for i in range(int(number*percent_array[pid])):
			init_states.append(EC2_INSTANCE_STATES[pid])

	for i in range(len(init_states)):
		index = int(random.uniform(0,len(init_states)-1))
		states.append(init_states[index])
		init_states.pop(index)

	return states 


