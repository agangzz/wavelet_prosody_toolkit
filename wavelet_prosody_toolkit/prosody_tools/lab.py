

def read_textgrid(filename, sample_rate=200):
    import tgt
    try:
        tg = tgt.read_textgrid(filename) #, include_empty_intervals=True)
    except:
        print("reading "+filename+" failed")

        return
    tiers = []
    labs = {}

    for tier in tg.get_tier_names():
        if (tg.get_tier_by_name(tier)).tier_type()!='IntervalTier':
            continue
        tiers.append(tg.get_tier_by_name(tier))
      
        lab = []
        for a in tiers[-1].annotations:

            try:
                # this was for some past experiment
                if a.text in ["p1","p2","p3","p4","p5","p6","p7"]:
                    lab[-1][-1]=lab[-1][-1]+"_"+a.text
                else:
                #lab.append([a.start_time*sample_rate,a.end_time*sample_rate,a.text.encode('utf-8')])
                    lab.append([a.start_time*sample_rate,a.end_time*sample_rate,a.text])
            except:
                pass
            #print tiers[-1].encode('latin-1')
        labs[tier.lower()] = lab
    try:
        for i in range(len(labs['prosody'])):
            if labs['prosody'][i][2][-2:] not in ["p1","p2","p3","p4","p5","p6","p7"]:
                labs['prosody'][i][2]+="_p0"
    except:
        pass
    #for t in tg.tiers:
        #print t
    #    print tg.tiers[0].encode('latin-1')
  
    return labs


def htk_to_ms(htk_time):
    """
    Convert time in HTK (100 ns) units to 5 ms
    """
    if type(htk_time)==type("string"):
        htk_time = float(htk_time)
    return htk_time / 50000.0


def read_htk_label(fname, scale = "word", htk_time=True, only_words=False):
    """
    Read HTK label, assume: "start end phone word", where word is optional.
    Convert times from HTK units to MS
    """
    import codecs
    
    try:
      
        f = codecs.open(fname,"r", "utf-8")
        #f = open(fname, "r")
    except:
        #raw_input()
        raise Exception("htk label file %s not found" % fname)
    
    label = f.readlines()
    f.close()

    label = [line.split() for line in label] ## split lines on whitespace
  
    segments = []
    words = []
    prev_end = 0.0
    prev_start = 0.0
    prev_word = "!SIL"
    prev_segment = ""
    orig_start=0
    orig_end = 0
    word = ""
    for line in label:
        if len(line)==4 and line[2] == 'skip':
            continue
        word = False
        if len(line)==3:
            (start,end,segment) = line
            if start == "nan":
                continue
	   
        elif len(line)==4:
            (start,end,segment,word) = line
            
        else:

            print("Bad line length:")
            print(line)

            continue
            #sys.exit(1)
        if htk_time == True:
            end = htk_to_ms(int(end))
            start = htk_to_ms(int(start))
        else:
            # 5ms frame
            pass
            end = float(end)*200
            start = float(start)*200
        if start == end:
            continue
        prev_end = start

        segments.append([int(start), int(end), segment]) #

        # handle the last word too
       
        """
        if word or segments[-1][2] in ["SIL", "pause", '#']:
            try:
                if prev_word not in ["!SIL", "pause"] and prev_word[0]!= "!" and prev_word[0]!="_"  and prev_word[0]!='#':
                    words.append([int(prev_start), int(prev_end),prev_word]) #, prev_word])
            except:
                pass
        """
        if word:
            
            words.append([int(prev_start), int(prev_end),prev_word])
            prev_start = start
            prev_word = word
            word = ""
    if len(label[-1])==4:
        words.append([htk_to_ms(float(label[-1][0])), htk_to_ms(float(label[-1][1])), label[-1][3]])
    labs = {}
    if len(words) > 0:
        labs["words"] = words
    labs["segments"] = segments
   
   
    return labs

    
def plot_labels(labels,shift = 0,  fig="", text = True, ypos = -0.5, color="black", boundary=True, size =9,prominences=[], rate = 1.):
    import numpy as np
    import pylab
    if fig == "":
        fig = pylab

    #print labels
    if len(prominences) == 0:
        prominences = np.ones(len(labels))
    else:
        prominences = np.sqrt(np.array(prominences)+0.25) #/np.max(prominences)
    import matplotlib as mpl
    mpl.rcParams['font.family'] = 'fantasy'
    mpl.rcParams['font.fantasy'] = 'Ubuntu' #'Arial'
    
    import matplotlib.patches as patches
    
    fig.add_patch(patches.Rectangle((labels[0][0], 0), labels[-1][1]-labels[0][0], size*0.3,color="white",alpha=0.35))
    i = 0
    for (start, end, segment) in labels:
        start*=rate
        end*=rate
        if text and segment[0] != "!":
            # fig.text(start+1-shift,5, token) #, color="grey")
            # fig.text(start-1+(end-start)/5-shift,ypos, segment, color=color, fontsize= 15)

            try:

                #fig.text(start+(end-start)/2,ypos, segment, color=color,fontsize=size+(prominences[i]-0.5)*10,ha='center',alpha=prominences[i]) #, color="grey")
                fig.text(start+(end-start)/2,ypos, segment, color=color,fontsize=size*(prominences[i]+0.5)*1,ha='center',alpha=0.75) #, color="grey")
            except:
                pass
            
            if boundary:
                fig.axvline(x=start, color='gray',linestyle="-",alpha=0.5)
                fig.axvline(x=end, color='gray',linestyle="-",alpha=0.5)
          
        i+=1

if __name__ == "__main__":
    import sys

    read_textgrid(sys.argv[1])
