# Extract everything if not extracted

# Check all the flags to make sure I don't set one used by the game
import os, json, shutil
from kh2lib.kh2lib import kh2lib
lib = kh2lib()

EXTRACT_ARDS=False
EXTRACT_SPAWNSCRIPTS=True


arddir = os.path.join(os.getcwd(), "extracted_ards")
if EXTRACT_ARDS:    
    if os.path.exists(arddir):
        shutil.rmtree(arddir)
    os.mkdir(arddir)

spawndir = os.path.join(os.getcwd(), "spawnscripts")
if os.path.exists(spawndir):
    shutil.rmtree(spawndir)
os.mkdir(spawndir)


ardinfo = {}
ignore_programs = {
    "ard04.ard": ["Program 0x4C"]
}

SKIPLINE = "	SetProgressFlag 0xFFF\n"

def shouldIgnore(ard, program):
    if ard in ignore_programs:
        if program in ignore_programs[ard]:
            return True
    return False

arddir_src = os.path.join(os.environ["USE_KH2_GITPATH"], "KH2", "ard")

for ard in os.listdir(arddir_src):
    fn = os.path.join(arddir_src, ard)

    out_pth = os.path.join(arddir, ard)
    if EXTRACT_ARDS:
        lib.editengine.bar_extract(fn, out_pth)
    
    evtname = None
    for f in [i for i in os.listdir(out_pth) if not i.endswith(".txt") and not i.endswith(".new")]:
        if f.startswith("btl."):
            evtname = f

    ardinfo[ard] = {
        "fn": fn,
        "out_pth": out_pth
    }
    if evtname == None:
        print("ARD {} has no btl".format(ard))
    else:
        evt_pth = os.path.join(out_pth, evtname)
        if EXTRACT_SPAWNSCRIPTS:
            lib.editengine.spawnscript_extract(evt_pth, evt_pth+".txt")
        
        lines = open(evt_pth+".txt")
        lines_new = []
        currentProgram = ''
        lines_program = []
        changesMade = False
        for line in lines:
            if line.startswith("Program"):
                if len(currentProgram) > 0:
                    if changesMade:
                        spawnscriptsdir = os.path.join(spawndir, ard)
                        if not os.path.exists(spawnscriptsdir):
                            os.mkdir(spawnscriptsdir)
                        programfn = os.path.join(spawnscriptsdir, "program-"+currentProgram.lower().replace(" ", "")[2:].strip())
                        with open(programfn, "w") as f:
                            f.write(''.join(lines_program))
                    lines_program = []
                    changesMade = False
                currentProgram = line.split(" ")[1]
            if len(currentProgram) > 0:
                if "Capacity" in line and not shouldIgnore(ard, currentProgram):
                    changesMade = True
                    #lines_program.append(SKIPLINE)
                    #lines_new.append(SKIPLINE)
                else:
                    lines_program.append(line)
                    lines_new.append(line)
        open(evt_pth+".txt.new","w").write("".join(lines_new))