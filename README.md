# Externals Libs:

- robotframework     https://pypi.org/project/robotframework/
- pillow             https://pypi.org/project/Pillow/
- psutil             https://pypi.org/project/psutil/

##Settings Keywords:
- Suite Setup  Start Background Scan  
- Suite Teardown    Stop Background Scan 
 
##Acceptance Test Keywords:  
- Read FDE DLog  \<TextStr>  <5>  
- Read FDE DLog Crashes  
- Preboot Bypass Logon  \<false>  
- SSO Chain Logon  \<true>  
- Start Notepad  
- Verify Notepad Running  
- Verify CPE Agent Running  
- Start CPInfo  
- Verify CPInfo files  
- Create Wakeup XML  
- Schedule Wakeup Task  \<User>   \<Passwd>  
- Change OS user password  \<User>   \<Passwd>  
- Read Client Status  \<70>  
- Read Encryption State  \<2>    \<AES-CBC>  
- Read wol status  \<false>
- Read wil status  \<false>  
- Read EPS Screensaver Text   \<TestText>  
- Read Win 3D Screensaver Text    \<TestText>  
- Hibernate  
- Reboot  
- CheckPoint Security Screensaver     \<false>  
- CheckPoint Security Screensaver Text    \<TestText>  

##Other keywords:  
- Create Scancode Bin  \<User>  \<Password>  \<32>  
- Run Scancode Bin  
- Read Disk Size  
- Create CrashDump  
- Read Release Build  
- Check If Win Activated  
- Open CPE Agent  
- Screenshot  
- Write new file  \<1GB>     \<10>  