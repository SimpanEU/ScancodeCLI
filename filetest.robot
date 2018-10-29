*** Settings ***
Resource    libs.robot

Suite Setup  Start Background Scan
Suite Teardown    Stop Background Scan

*** Test Cases ***

Parse Log Information
    Read FDE DLog  srv      20
    Read FDE DLog crashes
    Preboot Bypass Logon  true
    SSO Chain Logon  false
#
System Information
    Start CPInfo
    Change OS user password  User  pass123
    Read Release Build
    Start Notepad
    Verify CPE Agent Running
    Verify CPInfo files
    Verify Notepad Running
    Check If Win Activated
Read Registry Values
    Read Client Status  70
    Create Dump Test
    Read Encryption State  2    AES-CBC
    Read wol status  false
    Read wil status  true
System tasks
    Create Wakeup XML
    Schedule Wakeup Task  Win7    Password1!
    Hibernate
    Reboot
    TPM Status
Encryption Speed Test
    Read Disk Size
    Write new file  1GB     1

Windows Automation
    Open Tray
    Check FDE Status
    Collect Policies
    Screenshot