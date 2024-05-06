





FILE_NAME = "catalina.out"

threadInfo = {}

def main():
    print(FILE_NAME)
    
    with open(FILE_NAME) as fobj:
        for line in fobj.readlines():
            line = line.strip()
            if not line:
                if len(threadInfo) == 0:
                    continue
                print(threadInfo)
                threadInfo.clear()
                continue
            if line.startswith("\""):
                threadInfo["name"] = line.split("\"")[1]
                continue
            if line.startswith("java.lang.Thread.State:"):
                threadInfo["state"] = line.replace("java.lang.Thread.State: ", "")
                continue
            
            
if "__main__" == __name__:
    main()


