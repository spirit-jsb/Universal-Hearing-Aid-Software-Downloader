#############################################################
#                                                           #
#                   Copyright Bluebotlabz                   #
#                                                           #
#############################################################
import html
import requests
import libhearingdownloader
import xml.etree.ElementTree as xml
utilityVersion = "v1.6.3"
verboseDebug = False



print("==================================================")
print("=            Oticon Genie 2 Downloader           =")
print("="*(47-len(utilityVersion)) + " " + utilityVersion + " =")

disclaimer = [
    "DISCLAIMER",
    "",
    "I (Bluebotlabz), do not take any responsability for what you do using this software",
    "Oticon is a trademark of Oticon A/S",
    "Demant is a trademark of Demant A/S",
    "Oticon is a subsidiary of Demant A/S",
    "Oticon Genie 2 is created by Oticon A/S",
    "All rights and credit go to their rightful owners. No copyright infringement intended.",
    "",
    "Bluebotlabz and this downloader are not affiliated with or endorsed by Oticon or Demant A/S",
    "Depending on how this software is used, it may breach the EULA of the downloaded software",
    "This is an UNOFFICIAL downloader and use of the software downloaded using it may be limited"
]

# Display disclaimer
libhearingdownloader.printDisclaimer(disclaimer)

print ("Downloading version index")
headers = {
    "Content-Type": "application/soap+xml; charset=utf-8"
}

# Download version data
rawXmlData = requests.post("https://updater.oticon.com/UpdateWebService.svc", headers=headers, data='<s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope" xmlns:a="http://www.w3.org/2005/08/addressing"><s:Header><a:Action s:mustUnderstand="1">http://tempuri.org/IUpdateWebService/CheckForUpdate</a:Action><a:MessageID>urn:uuid:00000000-0000-0000-0000-000000000000</a:MessageID><a:ReplyTo><a:Address>http://www.w3.org/2005/08/addressing/anonymous</a:Address></a:ReplyTo><a:To s:mustUnderstand="1">https://updater.oticon.com/UpdateWebService.svc</a:To></s:Header><s:Body><CheckForUpdate xmlns="http://tempuri.org/"><request xmlns:b="http://schemas.datacontract.org/2004/07/Wdh.Genesis.SoftwareUpdater.Common" xmlns:i="http://www.w3.org/2001/XMLSchema-instance"><b:ClientId>00000000-0000-0000-0000-000000000000</b:ClientId><b:Languages xmlns:c="http://schemas.microsoft.com/2003/10/Serialization/Arrays"/><b:Locale>GB</b:Locale><b:Manufacturer>Oticon</b:Manufacturer><b:OEM>Oticon</b:OEM><b:OS>Microsoft Windows NT 10.0.22621.0</b:OS><b:RequestVersion>1</b:RequestVersion><b:Software><b:InstalledSoftware><b:Build>116</b:Build><b:Major>9</b:Major><b:Minor>3</b:Minor><b:Name>Genie2</b:Name><b:Revision>0</b:Revision></b:InstalledSoftware><b:InstalledSoftware><b:Build>19</b:Build><b:Major>27</b:Major><b:Minor>2</b:Minor><b:Name>OticonUpdater</b:Name><b:Revision>0</b:Revision></b:InstalledSoftware></b:Software></request></CheckForUpdate></s:Body></s:Envelope>')
data = xml.fromstring(html.unescape(rawXmlData.text))

packageXMLNS = '{http://www.wdh.com/xml/2012/06/25/updatemanifest.xsd}'
filesToDownload = []

for fileData in data.find('{http://www.w3.org/2003/05/soap-envelope}' + "Body").find('{http://tempuri.org/}' + "CheckForUpdateResponse").find('{http://tempuri.org/}' + "CheckForUpdateResult").find(packageXMLNS + "UpdateManifest").find(packageXMLNS + "DownloadJob").find(packageXMLNS + "Files"):
    filesToDownload.append(fileData.find(packageXMLNS + "FileName").text)

downloadURI = data.find('{http://www.w3.org/2003/05/soap-envelope}' + "Body").find('{http://tempuri.org/}' + "CheckForUpdateResponse").find('{http://tempuri.org/}' + "CheckForUpdateResult").find(packageXMLNS + "UpdateManifest").find(packageXMLNS + "DownloadJob").find(packageXMLNS + "ServerUri").text

if (verboseDebug):
    print(data.find('{http://www.w3.org/2003/05/soap-envelope}' + "Body").find('{http://tempuri.org/}' + "CheckForUpdateResponse").find('{http://tempuri.org/}' + "CheckForUpdateResult").find(packageXMLNS + "UpdateManifest").find(packageXMLNS + "Messages").find(packageXMLNS + "Message").text   + "--" +   data.find('{http://www.w3.org/2003/05/soap-envelope}' + "Body").find('{http://tempuri.org/}' + "CheckForUpdateResponse").find('{http://tempuri.org/}' + "CheckForUpdateResult").find(packageXMLNS + "UpdateManifest").find(packageXMLNS + "Version").text)

# Define list of valid versions and their download links (direct from CDN)
validVersions = [
    ("Direct From Server (RECOMMENDED)", "--"),
    (data.find('{http://www.w3.org/2003/05/soap-envelope}' + "Body").find('{http://tempuri.org/}' + "CheckForUpdateResponse").find('{http://tempuri.org/}' + "CheckForUpdateResult").find(packageXMLNS + "UpdateManifest").find(packageXMLNS + "Messages").find(packageXMLNS + "Message").text, "The latest Genie 2 Installer (OFFLINE) (from the updater)"),
    (data.find('{http://www.w3.org/2003/05/soap-envelope}' + "Body").find('{http://tempuri.org/}' + "CheckForUpdateResponse").find('{http://tempuri.org/}' + "CheckForUpdateResult").find(packageXMLNS + "UpdateManifest").find(packageXMLNS + "Messages").find(packageXMLNS + "Message").text, "The latest Genie 2 Installer (ONLINE) (from the updater)"),
    ("", "--"),
    ("Online Installers (shorter downloads, but they require an internet connection to install)", "--"),
    ("Genie 2 2022.1.0", "The latest(ish) Genie 2 2022.1.0 Installer (from the website)", "https://installcdn.oticon.com/22.1/15.19.13.0/Genie/Oticon/47b1876d/setup.exe"),
    ("Genie 2 2020.1", "The Genie 2 2020.1 Installer", "https://installcdn.oticon.com/20.1/9.3.116.0/Genie/Oticon/9fc0827f/setup.exe"),
    ("", "--"),
    ("Offline Installers (longer downloads, but they work without an internet connection to install)", "--"),
    ("Genie 2 2022.1.0", "The latest(ish) Genie 2 2022.1.0 Installer (OFFLINE INSTALLER, from the website)", "https://installcdn.oticon.com/full/22.1/15.19.13.0/OTG22_1237118OT_USB.zip"),
    ("Genie 2 2020.1", "The Genie 2 2020.1 Installer (OFFLINE INSTALLER)", "https://installcdn.oticon.com/full/20.1/9.3.116.0/OTG20_1214671OT_USB.zip")
]

# Select outputDir and targetVersion
outputDir = libhearingdownloader.selectOutputFolder()
targetVersion = libhearingdownloader.selectTargetVersion(validVersions)
print("\n\n")


if (targetVersion == 1):
    outputDir = libhearingdownloader.normalizePath( outputDir + data.find('{http://www.w3.org/2003/05/soap-envelope}' + "Body").find('{http://tempuri.org/}' + "CheckForUpdateResponse").find('{http://tempuri.org/}' + "CheckForUpdateResult").find(packageXMLNS + "UpdateManifest").find(packageXMLNS + "Messages").find(packageXMLNS + "Message").text + "/")

    # Download and save the files
    print("Downloading " + str(len(filesToDownload)) + " files\n")
    fileIndex = 1
    for fileToDownload in filesToDownload:
        libhearingdownloader.downloadFile(downloadURI + fileToDownload, outputDir + fileToDownload, "Downloading " + fileToDownload.split("/")[-1] + " (" + str(fileIndex) + "/" + str(len(filesToDownload)) + ")")
        fileIndex += 1
elif (targetVersion == 2):
    outputDir = libhearingdownloader.normalizePath( outputDir + data.find('{http://www.w3.org/2003/05/soap-envelope}' + "Body").find('{http://tempuri.org/}' + "CheckForUpdateResponse").find('{http://tempuri.org/}' + "CheckForUpdateResult").find(packageXMLNS + "UpdateManifest").find(packageXMLNS + "Messages").find(packageXMLNS + "Message").text + "/")

    # Download and save the files
    fileIndex = 1
    fileToDownload = "setup.exe"
    libhearingdownloader.downloadFile(downloadURI + fileToDownload, outputDir + fileToDownload, "Downloading " + fileToDownload.split("/")[-1])
else:
    # Create download folder
    outputDir += validVersions[targetVersion][0]

    # Download the file
    libhearingdownloader.downloadFile(validVersions[targetVersion][2], outputDir + validVersions[targetVersion][2].split("/")[-1], "Downloading " + validVersions[targetVersion][0])

print("\n\nDownload Complete!")