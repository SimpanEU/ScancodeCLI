*** Settings ***
Resource    libs.robot
Suite Setup  Start Background Scan
Suite Teardown    Stop Background Scan

*** Test Cases ***
Parse Log Information
    Read FDE DLog  TextStr      MaxMinAgo
    Read FDE DLog crashes
    Preboot Bypass Logon  false
    SSO Chain Logon  false

System Tasks
    Create Dump     crashdump1.dmp
    Read Release Build
    Start Notepad
    Verify CPE Agent Running
    Verify CPInfo files
    Verify Notepad Running
    Check If Win Activated
    Create Wakeup XML
    Schedule Wakeup Task  Win10    Password1!
    # Start CPInfo
    # Change OS user password  User  pass123
    # Hibernate
    # Reboot

Read Registry Values
    Create Dump     crashdump2.dmp
    Read Client Status  70
    Read Encryption State  2    AES-CBC
    Read wol status  false
    Read wil status  false

FDE Speed Test
    Read Disk Size
    Write new file  1GB     1

Windows Automation
    Open Tray
    Check FDE Status
    Screenshot
    # Collect Policies (Not imp)