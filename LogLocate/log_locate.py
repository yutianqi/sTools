# inputStr=input();
# print(inputStr);
logger = {}
appender = []
with open("log4j2.xml", 'r') as f: 
    lines = f.readlines()
    currentlogger = ""
    for line in lines:
        line = line.strip()
        if "Logger name=" in line:
            currentlogger = line.split("\"")[1]
            # print(currentlogger)
        if "AppenderRef" in line:
            appenderRef = line.split("\"")[1]
            # print(appenderRef)
            logger[currentlogger] = appenderRef

        if "<OssRollingFileAppender" in line:
            # print("--" + line)
            # print(line.split("\"")[1])
            # print(line.split("\"")[3])
            appender.append(line)
# print(logger)


html = etree.parse('log4j2.html',
			parser=etree.XMLParser(encoding='utf-8'))
print(root.tag)  										
print(etree.tostring(html)) 	
