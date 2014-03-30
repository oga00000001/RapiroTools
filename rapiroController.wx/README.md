# Rapiro controller with motion editor
## File
 * server script
    * rapiro_server.py
    * rapiro.py

 * client script
    * wxClient.py

 * motion sample file
    * sample81.tx (#M8)

## Preset control
    Send string '#V'(Version Check) when connecting.

|       |  #E   | #Ver |
|-------|-------|------|
|STOP   | #M0   | #M00 |
|Foward | #M1   | #M01 |
|Back   | #M2   | #M02 |
|Left   | #M4   | #M04 |
|Right  | #M3   | #M03 |
|OFF    | #Z    | #H   |
|Analog | #A6   | #A6  |
|C      | #C    | #C   |
|Q      | #Q    | #Q   |
|5      | #M5   | #M05 |
|M6     | #M6   | #M06 |
|M7     | #M7   | #M07 |
|M8     | #M8   | #M08 |
|M9     | #M9   | #M09 |
|M10    | -     | -    |
    
## Motion editor
|    LABEL    | Command        |
|-------------|----------------|
|    M-Clear  |   Motion Clear |
|    M-Save   |   Motion Save  |
|    M-Play   |   Motion Play  |
|    F-Load   |   File Load    |
|    F-Save   |   File Save    |
