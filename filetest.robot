*** Settings ***
Resource    libs.robot
Test Setup  Start Background Scan
Test Teardown    Stop Background Scan

*** Test Cases ***

Parse Log Information
    Read FDE DLog  srv      20
    Read FDE DLog crashes
    Preboot Bypass Logon  false
    SSO Chain Logon  false
System Information
    #Start CPInfo
    #Change OS user password  User  pass123
    Read Release Build
    Start Notepad
    Verify CPE Agent Running
    Verify CPInfo files
    Verify Notepad Running
    Check If Win Activated
Read Registry Values
    Read Client Status  70
    Read Encryption State  2    AES-CBC
    Read wol status  false
    Read wil status  false
System tasks
    Create Wakeup XML
    Schedule Wakeup Task  Win10    Password1!
    #Hibernate
    #Reboot
Encryption Speed Test
    Read Disk Size
    Create Dump Test
    Write new file  1GB     1
Windows Automation
    Open Tray
    Check FDE Status
    Collect Policies
    Screenshot