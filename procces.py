import psutil
import os
import signal

def DictToString(dist):
    lists = []
    for name in dist:
        lists.append(str(dist[name]) + ":" + name)
    return "\n".join(lists)

def monitor_processes():
    proccess = ["Registry", "svchost.exe", "dllhost.exe", "dwm.exe", "SearchProtocolHost.exe",
                "ArmourySwAgent.exe", "conhost.exe", "AsusSupportService.exe",
                "ArmouryCrate.DenoiseAI.exe", "ArmouryHtmlDebugServer.exe",
                "ArmouryCrate.UserSessionHelper.exe", "conhost.exe",
                "NVIDIA Overlay.exe", "ShellExperienceHost.exe", "WUDFHost.exe",
                "ArmourySocketServer.exe", "System Idle Process", "System", "smss.exe", "csrss.exe",
                "SystemSettingsBroker.exe", "services.exe", "lsass.exe", "fontdrvhost.exe", 
                "UserOOBEBroker.exe", "StartMenuExperienceHost.exe", "IntelCpHDCPSvc.exe", 
                "WidgetService.exe", "SystemSettings.exe", "AsusCertService.exe", 
                "MemCompression", "igfxCUIServiceN.exe", "spoolsv.exe", "wlanext.exe", 
                "AsusPTPService.exe", "AsusSoftwareManager.exe", "AsusAppService.exe", 
                "Ascon.CSC.DiagnosticService.exe", "ArmouryCrateControlInterface.exe", 
                "ArmouryCrate.Service.exe", "AsusSwitch.exe", "AsusSystemAnalysis.exe", 
                "AsusSystemDiagnosis.exe", "mDNSResponder.exe", "WsidService.exe", 
                "DtsApo4Service.exe", "ElevationService.exe", "GameSDK.exe", "esif_uf.exe", 
                "OneApp.IGCC.WinService.exe", "IpOverUsbSvc.exe", "RtkAudUService64.exe", 
                "LightingService.exe", "MpDefenderCoreService.exe", "IntelAudioService.exe", 
                "PolynomAppServer.exe", "ROGLiveService.exe", "RvControlSvc.exe", 
                "TeamViewer_Service.exe", "UTSCSI.EXE", "ASUSSmartDisplayControl.exe", 
                "MsMpEng.exe", "WMIRegistrationService.exe", "RstMwService.exe", 
                "WmiPrvSE.exe", "DriverInstall.exe", "InstallAssistService.exe", "dasHost.exe", 
                "SecurityHealthService.exe", "jhi_service.exe", "unsecapp.exe", 
                "WmiPrvSE.exe", "firefox.exe", "SearchHost.exe", "NisSrv.exe", 
                "service_update.exe", "AcPowerNotification.exe", "MBAMService.exe", 
                "PresentationFontCache.exe", "MoUsoCoreWorker.exe", "AsusOptimizationStartupTask.exe", 
                "winlogon.exe", "schedul2.exe", "taskhostw.exe", "nvsphelper64.exe", 
                "sihost.exe", "ApplicationFrameHost.exe", "SearchIndexer.exe", 
                "LockApp.exe", "crash_handler.exe", "AsusOSD.exe", "audiodg.exe", "browser.exe",
                "AsusOptimization.exe", "nvcontainer.exe", "AsusSoftwareManagerAgent.exe", 
                "asus_framework.exe", "asus_framework.exe", "NVDisplay.Container.exe",
                "AppleMobileDeviceService.exe", "wininit.exe", "RuntimeBroker.exe",
                "TextInputHost.exe", "ctfmon.exe", "plugin_host-3.3.exe", "plugin_host-3.8.exe",
                "CHXSmartScreen.exe", "AacAmbientLighting.exe", "msteamsupdate.exe",
                "Widgets.exe", "mbamtray.exe"]
    
    output = {}

    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] not in proccess:
            PID = proc.info['pid']
            NAME = proc.info['name']

            #print(f"Process ID: {PID} - {NAME}")
            output[NAME] = PID
    
    return output

def kill_proccess(PID):
    try:
        os.kill(PID, signal.SIGILL)
        return "Процесс завершён успешно!"
    except psutil.NoSuchProcess:
        return f"Процесс с PID {PID} не существует."
    except psutil.AccessDenied:
        return f"Нет прав для завершения процесса с PID {PID}."
    except Exception as e:
        return f"Произошла ошибка: {e}"





