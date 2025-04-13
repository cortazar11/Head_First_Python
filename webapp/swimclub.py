import statistics
import hfpy_utils
import json
import os

FOLDER="swimdata/"
CHARTS="charts/"
JSONDATA="records.json"


def event_lookup(event):

    conversions= {
        "Free": "freestyle",
        "Back": "backstroke",
        "Breast": "breaststroke",
        "Fly": "butterfly",
        "IM": "individual medley"

    }

    *_, distance, stroke = event.removesuffix(".txt").split("-")
    return f"{distance} {conversions[stroke]}"

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
    #min_secs, hundreths=str(round((average/100),2)).split(".")
    min_secs, hundreths=f"{(average/100):.2f}".split(".")
    min_secs=int(min_secs)
    minutes=min_secs//60
    seconds=min_secs-minutes*60
    average= f"{minutes}:{seconds}.{hundreths}"

    return swimmer,age,distance,stroke,times,average, converts # Return as a tuple


def produce_bar_chart(fn, location=CHARTS):
    """Given the name of a swimmer's file, produce a HTML/SVG-based bar chart.
     
    Save the chart to the CHARTS folder. Return the path to the bar chart file.
    """
    swimmer, age, distance, stroke, times, average, converts = read_swim_data(fn)
    from_max = max(converts)
    times.reverse()
    converts.reverse()
    title = f"{swimmer} (Under {age}) {distance} {stroke}"
    header = f"""<!DOCTYPE html>
                    <html>
                        <head>
                            <title>{title}</title>
                            <link rel="stylesheet" href="/static/webapp.css"/>
                        </head>
                        <body>
                            <h2>{title}</h2>"""
    body = ""
    for n, t in enumerate(times):
        bar_width = hfpy_utils.convert2range(converts[n], 0, from_max, 0, 350)
        body = body + f"""
                            <svg height="30" width="400">
                                <rect height="30" width="{bar_width}" style="fill:rgb(0,0,255);" />
                            </svg>{t}<br />"""
    with open(JSONDATA) as jf:
        records = json.load(jf)
    COURSES = ("LC Men", "LC Women", "SC Men", "SC Women")
    times = []
    for course in COURSES:
        times.append(records[course][event_lookup(fn)])
    footer = f"""
                            <p>Average time: {average}</p>
                            <p>M: {times[0]} ({times[2]})<br />W: {times[1]} ({times[3]})</p>
                        </body>
                    </html>"""
    page = header + body + footer
    #save_to = os.path.join(location, fn.removesuffix('.txt') + '.html')
    save_to = f"{location}{fn.removesuffix('.txt')}.html"
    with open(save_to, "w") as sf:
        print(page, file=sf)

    return save_to


