def moving_averages(pulse_rate, samples_per_second):

    i = 0
    window = 0

    #Find the number of samples in the last 15 seconds and round to 0 decimal places
    number_samples = samples_per_second*15
    number_samples = round(number_samples)

    #Find length of the pulse rate array
    len_pulse_rate = len(pulse_rate)
    
    #If there arent enough values for moving average print 0
    if len(pulse_rate) < number_samples:

        #Create a new list containing only the data from the last 15 seconds
        #Calculate length of list
        moving_pulse_rate = pulse_rate[0:len_pulse_rate]
        length_moving_pulse_rate = len(moving_pulse_rate)

        #Loop through the list to find total of the last 15 seconds
        while i < length_moving_pulse_rate:
            current_value = moving_pulse_rate[i]
            window = window + current_value
            i = i + 1
       #Calculate Moving Average
        moving_average = window/length_moving_pulse_rate
        
        
    #If there are enough values for moving average print print it
    elif len(pulse_rate) >= number_samples:

        #Create a new list containing only the data from the last 15 seconds
        #Calculate length of list
        moving_pulse_rate = pulse_rate[(len_pulse_rate-number_samples):len_pulse_rate]
        length_moving_pulse_rate = len(moving_pulse_rate)

        #Loop through the list to find total of the last 15 seconds
        while i < length_moving_pulse_rate:
            current_value = moving_pulse_rate[i]
            window = window + current_value
            i = i + 1
       #Calculate Moving Average
        moving_average = window/number_samples

    return moving_average




#Example variables and return moving averages array
example_pulse_rate = [22,45,76,87,54,23,66,88,22,25,77,89,45,13,17,56,22,38,99,78,100000000]
samples_1_second = 1
moving_average = moving_averages(example_pulse_rate, samples_1_second)

#Print data and arrays
print("Example pulse rate array: ")
print(example_pulse_rate)
print()
print("Samples per second: " + str(samples_1_second))
print()
print("Current Moving Average: " )
print(moving_average)
