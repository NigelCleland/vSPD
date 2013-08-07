if exist report.txt                     erase report.txt /q
if exist vSPDcase.inc                   erase vSPDcase.inc /q
if exist runVSPDSetupProgress.txt       erase runVSPDSetupProgress.txt /q
if exist runVSPDSolveProgress.txt       erase runVSPDSolveProgress.txt /q
if exist runVSPDMergeProgress.txt       erase runVSPDMergeProgress.txt /q
if exist runVSPDReportProgress.txt      erase runVSPDReportProgress.txt /q
if exist "Z:\home\nigel\python\vSPD\Programs\..\Output\Test"        rmdir "Z:\home\nigel\python\vSPD\Programs\..\Output\Test" /s /q
mkdir "Z:\home\nigel\python\vSPD\Programs\..\Output\Test"
