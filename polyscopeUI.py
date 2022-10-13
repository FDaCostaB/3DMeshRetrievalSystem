def setPolyscopeSetting(windowWidth, windowHeight, windowPosX=100, windowPosY=100):
    f = open(".polyscope.ini", "w")
    f.write("{\n\"windowHeight\": "+str(windowHeight)+",\n\"windowPosX\": "+str(windowPosX)+",\n\"windowPosY\": "+str(windowPosY)+",\n\"windowWidth\": "+str(windowWidth)+"\n}")
    f.close()