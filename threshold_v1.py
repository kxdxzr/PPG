def get_threshold(pulse_rate):
    
    threshold = max(pulse_rate) - (max(pulse_rate)-min(pulse_rate))*0.1
    
    counter = 0
    below_threshold = True
    peaks = []
    time_peaks = []


    for i in pulse_rate:
        
        if i >= threshold and below_threshold == True:
            counter = counter + 1
            below_threshold = False
            time_between_peaks = len(peaks)
            time_peaks.append(time_between_peaks)
            peaks = []
            

        elif i < threshold:
            below_threshold = True
            peaks.append(i)


    bpm = counter*60/15
    period = 0.02*time_peaks[]
    
    return threshold, bpm, time_peaks







