import os, json, shutil
from kh2lib.kh2lib import kh2lib
lib = kh2lib()

TITLE = "KH2 Memory Allocator V0.1"

arddir = os.path.join(os.getcwd(), "extracted_ards")
spawndir = os.path.join("spawnscripts")

assets = []

for ard in os.listdir(spawndir)[:1]:
    ard = "tt01.ard"
    programs = []
    for fn in os.listdir(os.path.join(spawndir, ard)):
        programs.append(os.path.join(spawndir, ard, fn))

        
    a = {
        "name": "ard/{}".format(ard),
        "method": "binarc",
        "source": [
            {
                "name": "evt.script",
                "type": "AreaDataScript",
                "method": "areadatascript",
                "source": [            
                    {
                        "name": programs[i].replace("\\", "/"),
                    }
                    for i in range(len(programs))
                ]
            }
        ]
    }

    assets.append(a)

import yaml
yaml.dump({"title": TITLE, "assets": assets}, open("mod.yml", "w"))