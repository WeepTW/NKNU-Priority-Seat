![GITHUB](https://github.com/WeepTW/NKNU-Priority-Seat/blob/main/icon.jpg "NKNU-Prioity-Seat")

# Introduction
##### 🎬 https://www.youtube.com/watch?v=UYg32Yh_MQM 🎬
2022NKNU MATH special subject(RPA)  
Automatically reserve the library rooms of National Kaohsiung Normal University.  
  

## Development guide

Check you have download `python` & `pip` then setting the path successfully, or the program will run not thing.  
* If you are using **LINE**, environmental setup will be down via requirements.txt automatically.  
* If you are using **PC**, check out you had run `setup.exe` in the begining,  
*    or you have to `decompress the file and using pyset_backup.cmd` first, then lanuching `NKNU-Priority-Seat.exe`  
Check you have add your information in `Info.xlsx`.  
###### Then begining!

### directory structure
```
NKNU-Priority-Seat
├── app.py (for Line Bot)
├── main.exe (for PC)
├── run
    └── view.py
    └── mod.py
    └── ...(deep learning with tesseract and pytorch) 
```

where all the api were located in view.py, which is 
    reservation(id, token, days=0, hour=now(), min=now()) -> str: rentTime | error messenage  
    cancel(id) -> str: number of cancelation  
    record(id) -> str: records of reservations  
    log(id) -> dict:[user['account'],user['reservation'],user['friends'],link]  