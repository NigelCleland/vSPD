* Enter the run name here *******************
$setglobal    runName     Test	  

* Mode = 1 --> Developer license mode, Mode = 0 --> Runtime license mode **************
$setglobal    Mode        0

 
$setglobal    ProgramPath     "%system.fp%"
$setglobal    InputPath       "%system.fp%..\Input\"
$setglobal    OvrdPath        "%system.fp%"
$setglobal    OutputPath      "%system.fp%..\Output\"


$setglobal    VSPDInputOvrdData     'VSPDRunFile'
$setglobal    VSPDInputOvrdFormat    2
$setglobal    VSPDInputFileName     'VSPDRunFile'