from matplotlib import pyplot as plt
import matplotlib.animation as animation

#take time array from manager.getTimes
def getStrings(times):
    algoNames = []

    #adding the correct strings to the 
    for i in range(len(times)):
        if times[i]:
            match i:
                case 0:
                    algoNames.append("Bubble Sort")
                case 1:
                    algoNames.append("Merge Sort")
                case 2:
                    algoNames.append("Insertion Sort")
                case 3:
                    algoNames.append("Quick Sort")
                case 4:
                    algoNames.append("Radix Sort")
                case 5:
                    algoNames.append("Linear Search")
    
    #getting rid of the zeros for the graph
    while(0 in times):
        times.remove(0)
    
    #Attaching names to corresponding time values
    both = dict()
    for i in range(len(times)):
        both[algoNames[i]] = times[i]

    return both

def showGraph(dictionary):
    #Splitting up names and times again
    names = dictionary.keys()
    times = dictionary.values()

    #Getting range of values for graph animation
    time_ranges = []
    for time in times:
        time_ranges.append([i if i<time else time for i in range(max(times))])
    
    fig = plt.figure(figsize=(10,9)) #size of the graph in inches
    axes = fig.add_subplot(1,1,1)
    axes.set_ylim(0, max(times) + max(times)/20) #just so the top of the graph has a bit of a buffer

    #update the graph each interval with a new value
    def animate(i):
        if i < len(time_ranges[0]): #to avoid out of bounds error(i doesn't stop counting up)
            plt.bar(names, [row[i] for row in time_ranges], color="BLUE")
    

    i = 0
    anim = animation.FuncAnimation(fig, animate, interval = 1000/max(times), cache_frame_data=False)
    
    #labels
    plt.ylabel("Execution Time(microseconds)")
    plt.title("Comparing Execution Time of Different Algorithms")
    plt.show()