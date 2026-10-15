import json, math

def num(x): return isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x)
def pos(x): return num(x) and x>0
def jround(x): return math.floor(x+0.5)
def r1(x): return jround(x*10)/10
def jsnum(x):
    if isinstance(x,float) and x==int(x): return str(int(x))
    return str(x)
def comma(x):
    if isinstance(x,float) and x==int(x): x=int(x)
    return f"{x:,}"

PF=0.6

def watt_plan(va):
    if not pos(va): return {"error":"the VA rating must be above zero"}
    return {"watts":r1(va*PF)}

def render_watt(r,va):
    return ("The "+comma(va)+" VA sticker honestly means about "+comma(r["watts"])
            +" watts - the box prints volt-amps big and the 0.6 power factor that deflates them small.")

def runtime_plan(half_w,half_m,load):
    if not pos(half_w): return {"error":"the half-load watts must be above zero"}
    if not pos(half_m): return {"error":"the half-load minutes must be above zero"}
    if not pos(load): return {"error":"the load must be above zero"}
    rating=half_w*2
    minutes=half_m*half_w/load
    if load>rating: verdict="it is over the honest rating, and the unit may not hold it at all"
    elif load>half_w: verdict="it is past half load, where the curve bends down"
    else: verdict="it sits at or under half load, where inverse minutes stay optimistic"
    return {"rating":r1(rating),"minutes":r1(minutes),"verdict":verdict}

def render_runtime(r,half_w,half_m,load):
    return ("The spec sheet's "+jsnum(half_m)+" minutes was measured at "+comma(half_w)+" watts; your "+comma(load)
            +"-watt draw cuts it to about "+jsnum(r["minutes"])+" minutes against the "+comma(r["rating"])+"-watt honest rating - "+r["verdict"]+".")

def age_plan(minutes,age):
    if not pos(minutes): return {"error":"the minutes must be above zero"}
    if not num(age): return {"error":"the battery age must be a number"}
    if age<0: return {"error":"the battery age cannot be negative"}
    factor=max(0.4,1-0.12*age)
    return {"factor":r1(factor*100),"aged":r1(minutes*factor)}

def render_age(r,minutes,age):
    return ("At "+jsnum(age)+(" year" if age==1 else " years")+" old the lead battery keeps about "+jsnum(r["factor"])+"% of its day-one legs - your "
            +jsnum(minutes)+" minutes is honestly "+jsnum(r["aged"])+".")

cases=[]
def add(tool,args):
    if tool=="watt": r=watt_plan(*args); fn=render_watt
    elif tool=="runtime": r=runtime_plan(*args); fn=render_runtime
    else: r=age_plan(*args); fn=render_age
    case={"tool":tool,"args":args,"result":r}
    if "error" not in r: case["render"]=fn(r,*args)
    cases.append(case)

for a in [(1500,),(1000,),(900,),(2200,),(1350,),(850,)]:
    add("watt",a)
for a in [(450,10,600),(400,12,300),(500,8,700),(550,6,900),(450,10,1200),(450,10,450),(600,9,1200),(600,9,1201)]:
    add("runtime",a)
for a in [(7.5,3),(16,5),(10,1),(12,0),(20,8),(9.5,2.5)]:
    add("age",a)
add("watt",[0]); add("watt",["big"])
add("runtime",[0,10,600]); add("runtime",[450,0,600]); add("runtime",[450,10,0]); add("runtime",["half",10,600])
add("age",[0,3]); add("age",[7.5,-1]); add("age",["seven",3])

json.dump(cases,open("expected.json","w"),separators=(",",":"))
print(len(cases),"cases")
