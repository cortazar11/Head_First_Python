import statistics
FOLDER="swimdata/"
def read_swim_data (filename):
    """
    Reads swim data from a file and returns swimmer's name, age, distance, stroke, times, and average time.
    Given the name of a swimmwer file, extract all required data,
    then return it to the caller as a tuple
    """
    swimmer,age,distance,stroke=filename.removesuffix(".txt").split("-")
    with open(FOLDER+filename) as file:
        lines = file.readlines()
        times=lines[0].strip().split(",")
    converts=[]
    for t in times:
        if ":" in t:
            minutes, rest=t.split(":")
            seconds, hundreths=rest.split(".")
        else:
            minutes=0
            seconds, hundreths=t.split(".")
        converts.append(int(minutes)*60*100+int(seconds)*100+int(hundreths))
    average=statistics.mean(converts)
    min_secs, hundreths=str(round((average/100),2)).split(".")
    min_secs=int(min_secs)
    minutes=min_secs//60
    seconds=min_secs-minutes*60
    average= f"{minutes}:{seconds}.{hundreths}"

    return swimmer,age,distance,stroke,times,average, converts # Return as a tuple