# usage for windows


### 创建任务(每小时执行一次)
```bat
schtasks /create /sc hourly /mo 1  /tn "Daily Push" /tr D:\Code\Github\sTools\DailyPush\daily_push.vbs
```     
    
### 创建任务(每30分钟执行一次)
```bat
schtasks /create /sc minute /mo 30 /tn "Daily Push" /tr D:\Code\Github\sTools\DailyPush\daily_push.vbs
```     

### 立即执行任务
```bat
schtasks /run /tn "Daily Push" 
```    

### 删除任务
```bat2
schtasks /delete /tn "Daily Push"
```     
