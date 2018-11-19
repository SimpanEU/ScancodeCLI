*** Settings ***
Resource    libs.robot
Suite Setup  Start Background Scan
Suite Teardown    Stop Background Scan

*** Test Cases ***
Test Keywords
    Read Disk Size
    Create CrashDump

Parse Log Information
    Read FDE DLog  TextStr    5
    Read FDE DLog Crashes
    Preboot Bypass Logon  false
    SSO Chain Logon  true

System Tests
    Read Release Build
    Check If Win Activated
    Start Notepad
    Verify Notepad Running
    Verify CPE Agent Running
    # Start CPInfo
    # Verify CPInfo files
    Create Wakeup XML
    # Schedule Wakeup Task  Win10    Password1!
    # Change OS user password  User  pass123
    # Hibernate
    # Reboot

Read Registry Values
    # Read Client Status  70
    # Read Encryption State  2    AES-CBC
    Read wol status  false
    Read wil status  false
    # Read EPS Screensaver Text       Simpan
    # Read Win 3D Screensaver Text       Simpan

Server Settings
    CheckPoint Security Screensaver     false
    CheckPoint Security Screensaver Text    Simpan

FDE Speed Test
    Write new file  1GB     1

Windows Automation
    Open Tray
    Check FDE Status
    Screenshot
   # Collect Policies (Not imp.)