import pandas as pd
from attackcti import attack_client
import csv
import sys
import os
maxInt = sys.maxsize

while True:
    # Decrease the maxInt value by factor 10 as long as the OverflowError occurs
    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)

CODE_TACTICS = ['TA0043', 'TA0042', 'TA0001', 'TA0002', 'TA0003', 'TA0004', 'TA0005', 'TA0006', 'TA0007', 'TA0008', 'TA0009', 'TA0011', 'TA0010', 'TA0040']
NAME_TACTICS = ['Reconnaissance', 'Resource Development', 'Initial Access', 'Execution', 'Persistence', 'Privilege Escalation', 'Defense Evasion', 'Credential Access', 'Discovery', 'Lateral Movement', 'Collection', 'Command and Control', 'Exfiltration', 'Impact']

CODE_TECHNIQUES = ['T1595', 'T1592', 'T1589', 'T1590', 'T1591', 'T1598', 'T1597', 'T1596', 'T1593', 'T1594', 'T1583', 'T1586', 'T1584', 'T1587', 'T1585', 'T1588', 'T1608', 'T1189', 'T1190', 'T1133', 'T1200', 'T1566', 'T1091', 'T1195', 'T1199', 'T1078', 'T1059', 'T1609', 'T1610', 'T1203', 'T1559', 'T1106', 'T1053', 'T1129', 'T1072', 'T1569', 'T1204', 'T1047', 'T1098', 'T1197', 'T1547', 'T1037', 'T1176', 'T1554', 'T1136', 'T1543', 'T1546', 'T1574', 'T1525', 'T1556', 'T1137', 'T1542', 'T1505', 'T1205', 'T1548', 'T1134', 'T1484', 'T1611', 'T1068', 'T1055', 'T1612', 'T1622', 'T1140', 'T1006', 'T1480', 'T1211', 'T1222', 'T1564', 'T1562', 'T1070', 'T1202', 'T1036', 'T1578', 'T1112', 'T1601', 'T1599', 'T1027', 'T1647', 'T1620', 'T1207', 'T1014', 'T1553', 'T1218', 'T1216', 'T1221', 'T1127', 'T1535', 'T1550', 'T1497', 'T1600', 'T1220', 'T1557', 'T1110', 'T1555', 'T1212', 'T1187', 'T1606', 'T1056', 'T1111', 'T1621', 'T1040', 'T1003', 'T1528', 'T1558', 'T1539', 'T1552', 'T1087', 'T1010', 'T1217', 'T1580', 'T1538', 'T1526', 'T1619', 'T1613', 'T1482', 'T1083', 'T1615', 'T1046', 'T1135', 'T1201', 'T1120', 'T1069', 'T1057', 'T1012', 'T1018', 'T1518', 'T1082', 'T1614', 'T1016', 'T1049', 'T1033', 'T1007', 'T1124', 'T1210', 'T1534', 'T1570', 'T1563', 'T1021', 'T1080', 'T1560', 'T1123', 'T1119', 'T1185', 'T1115', 'T1530', 'T1602', 'T1213', 'T1005', 'T1039', 'T1025', 'T1074', 'T1114', 'T1113', 'T1125', 'T1071', 'T1092', 'T1132', 'T1001', 'T1568', 'T1573', 'T1008', 'T1105', 'T1104', 'T1095', 'T1571', 'T1572', 'T1090', 'T1219', 'T1102', 'T1020', 'T1030', 'T1048', 'T1041', 'T1011', 'T1052', 'T1567', 'T1029', 'T1537', 'T1531', 'T1485', 'T1486', 'T1565', 'T1491', 'T1561', 'T1499', 'T1495', 'T1490', 'T1498', 'T1496', 'T1489', 'T1529']
NAME_TECHNIQUES = ['Active Scanning', 'Gather Victim Host Information', 'Gather Victim Identity Information', 'Gather Victim Network Information', 'Gather Victim Org Information', 'Phishing for Information', 'Search Closed Sources', 'Search Open Technical Databases', 'Search Open Websites/Domains', 'Search Victim-Owned Websites', 'Acquire Infrastructure', 'Compromise Accounts', 'Compromise Infrastructure', 'Develop Capabilities', 'Establish Accounts', 'Obtain Capabilities', 'Stage Capabilities', 'Drive-by Compromise', 'Exploit Public-Facing Application', 'External Remote Services', 'Hardware Additions', 'Phishing', 'Replication Through Removable Media', 'Supply Chain Compromise', 'Trusted Relationship', 'Valid Accounts', 'Command and Scripting Interpreter', 'Container Administration Command', 'Deploy Container', 'Exploitation for Client Execution', 'Inter-Process Communication', 'Native API', 'Scheduled Task/Job', 'Shared Modules', 'Software Deployment Tools', 'System Services', 'User Execution', 'Windows Management Instrumentation', 'Account Manipulation', 'BITS Jobs', 'Boot or Logon Autostart Execution', 'Boot or Logon Initialization Scripts', 'Browser Extensions', 'Compromise Client Software Binary', 'Create Account', 'Create or Modify System Process', 'Event Triggered Execution', 'Hijack Execution Flow', 'Implant Internal Image', 'Modify Authentication Process', 'Office Application Startup', 'Pre-OS Boot', 'Server Software Component', 'Traffic Signaling', 'Abuse Elevation Control Mechanism', 'Access Token Manipulation', 'Domain Policy Modification', 'Escape to Host', 'Exploitation for Privilege Escalation', 'Process Injection', 'Build Image on Host', 'Debugger Evasion', 'Deobfuscate/Decode Files or Information', 'Direct Volume Access', 'Execution Guardrails', 'Exploitation for Defense Evasion', 'File and Directory Permissions Modification', 'Hide Artifacts', 'Impair Defenses', 'Indicator Removal on Host', 'Indirect Command Execution', 'Masquerading', 'Modify Cloud Compute Infrastructure', 'Modify Registry', 'Modify System Image', 'Network Boundary Bridging', 'Obfuscated Files or Information', 'Plist File Modification', 'Reflective Code Loading', 'Rogue Domain Controller', 'Rootkit', 'Subvert Trust Controls', 'Signed Binary Proxy Execution', 'Signed Script Proxy Execution', 'Template Injection', 'Trusted Developer Utilities Proxy Execution', 'Unused/Unsupported Cloud Regions', 'Use Alternate Authentication Material', 'Virtualization/Sandbox Evasion', 'Weaken Encryption', 'XSL Script Processing', 'Adversary-in-the-Middle', 'Brute Force', 'Credentials from Password Stores', 'Exploitation for Credential Access', 'Forced Authentication', 'Forge Web Credentials', 'Input Capture', 'Two-Factor Authentication Interception', 'Multi-Factor Authentication Request Generation', 'Network Sniffing', 'OS Credential Dumping', 'Steal Application Access Token', 'Steal or Forge Kerberos Tickets', 'Steal Web Session Cookie', 'Unsecured Credentials', 'Account Discovery', 'Application Window Discovery', 'Browser Bookmark Discovery', 'Cloud Infrastructure Discovery', 'Cloud Service Dashboard', 'Cloud Service Discovery', 'Cloud Storage Object Discovery', 'Container and Resource Discovery', 'Domain Trust Discovery', 'File and Directory Discovery', 'Group Policy Discovery', 'Network Service Scanning', 'Network Share Discovery', 'Password Policy Discovery', 'Peripheral Device Discovery', 'Permission Groups Discovery', 'Process Discovery', 'Query Registry', 'Remote System Discovery', 'Software Discovery', 'System Information Discovery', 'System Location Discovery', 'System Network Configuration Discovery', 'System Network Connections Discovery', 'System Owner/User Discovery', 'System Service Discovery', 'System Time Discovery', 'Exploitation of Remote Services', 'Internal Spearphishing', 'Lateral Tool Transfer', 'Remote Service Session Hijacking', 'Remote Services', 'Taint Shared Content', 'Archive Collected Data', 'Audio Capture', 'Automated Collection', 'Browser Session Hijacking', 'Clipboard Data', 'Data from Cloud Storage Object', 'Data from Configuration Repository', 'Data from Information Repositories', 'Data from Local System', 'Data from Network Shared Drive', 'Data from Removable Media', 'Data Staged', 'Email Collection', 'Screen Capture', 'Video Capture', 'Application Layer Protocol', 'Communication Through Removable Media', 'Data Encoding', 'Data Obfuscation', 'Dynamic Resolution', 'Encrypted Channel', 'Fallback Channels', 'Ingress Tool Transfer', 'Multi-Stage Channels', 'Non-Application Layer Protocol', 'Non-Standard Port', 'Protocol Tunneling', 'Proxy', 'Remote Access Software', 'Web Service', 'Automated Exfiltration', 'Data Transfer Size Limits', 'Exfiltration Over Alternative Protocol', 'Exfiltration Over C2 Channel', 'Exfiltration Over Other Network Medium', 'Exfiltration Over Physical Medium', 'Exfiltration Over Web Service', 'Scheduled Transfer', 'Transfer Data to Cloud Account', 'Account Access Removal', 'Data Destruction', 'Data Encrypted for Impact', 'Data Manipulation', 'Defacement', 'Disk Wipe', 'Endpoint Denial of Service', 'Firmware Corruption', 'Inhibit System Recovery', 'Network Denial of Service', 'Resource Hijacking', 'Service Stop', 'System Shutdown/Reboot']

ALL_TTPS = ['TA0043', 'TA0042', 'TA0001', 'TA0002', 'TA0003', 'TA0004', 'TA0005', 'TA0006', 'TA0007', 'TA0008', 'TA0009', 'TA0011', 'TA0010', 'TA0040', 'T1595', 'T1592', 'T1589', 'T1590', 'T1591', 'T1598', 'T1597', 'T1596', 'T1593', 'T1594', 'T1583', 'T1586', 'T1584', 'T1587', 'T1585', 'T1588', 'T1608', 'T1189', 'T1190', 'T1133', 'T1200', 'T1566', 'T1091', 'T1195', 'T1199', 'T1078', 'T1059', 'T1609', 'T1610', 'T1203', 'T1559', 'T1106', 'T1053', 'T1129', 'T1072', 'T1569', 'T1204', 'T1047', 'T1098', 'T1197', 'T1547', 'T1037', 'T1176', 'T1554', 'T1136', 'T1543', 'T1546', 'T1574', 'T1525', 'T1556', 'T1137', 'T1542', 'T1505', 'T1205', 'T1548', 'T1134', 'T1484', 'T1611', 'T1068', 'T1055', 'T1612', 'T1622', 'T1140', 'T1006', 'T1480', 'T1211', 'T1222', 'T1564', 'T1562', 'T1070', 'T1202', 'T1036', 'T1578', 'T1112', 'T1601', 'T1599', 'T1027', 'T1647', 'T1620', 'T1207', 'T1014', 'T1553', 'T1218', 'T1216', 'T1221', 'T1127', 'T1535', 'T1550', 'T1497', 'T1600', 'T1220', 'T1557', 'T1110', 'T1555', 'T1212', 'T1187', 'T1606', 'T1056', 'T1111', 'T1621', 'T1040', 'T1003', 'T1528', 'T1558', 'T1539', 'T1552', 'T1087', 'T1010', 'T1217', 'T1580', 'T1538', 'T1526', 'T1619', 'T1613', 'T1482', 'T1083', 'T1615', 'T1046', 'T1135', 'T1201', 'T1120', 'T1069', 'T1057', 'T1012', 'T1018', 'T1518', 'T1082', 'T1614', 'T1016', 'T1049', 'T1033', 'T1007', 'T1124', 'T1210', 'T1534', 'T1570', 'T1563', 'T1021', 'T1080', 'T1560', 'T1123', 'T1119', 'T1185', 'T1115', 'T1530', 'T1602', 'T1213', 'T1005', 'T1039', 'T1025', 'T1074', 'T1114', 'T1113', 'T1125', 'T1071', 'T1092', 'T1132', 'T1001', 'T1568', 'T1573', 'T1008', 'T1105', 'T1104', 'T1095', 'T1571', 'T1572', 'T1090', 'T1219', 'T1102', 'T1020', 'T1030', 'T1048', 'T1041', 'T1011', 'T1052', 'T1567', 'T1029', 'T1537', 'T1531', 'T1485', 'T1486', 'T1565', 'T1491', 'T1561', 'T1499', 'T1495', 'T1490', 'T1498', 'T1496', 'T1489', 'T1529']
STIX_IDENTIFIERS = ['x-mitre-tactic--daa4cbb1-b4f4-4723-a824-7f1efd6e0592', 'x-mitre-tactic--d679bca2-e57d-4935-8650-8031c87a4400', 'x-mitre-tactic--ffd5bcee-6e16-4dd2-8eca-7b3beedf33ca', 'x-mitre-tactic--4ca45d45-df4d-4613-8980-bac22d278fa5', 'x-mitre-tactic--5bc1d813-693e-4823-9961-abf9af4b0e92', 'x-mitre-tactic--5e29b093-294e-49e9-a803-dab3d73b77dd', 'x-mitre-tactic--78b23412-0651-46d7-a540-170a1ce8bd5a', 'x-mitre-tactic--2558fd61-8c75-4730-94c4-11926db2a263', 'x-mitre-tactic--c17c5845-175e-4421-9713-829d0573dbc9', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--d108ce10-2419-4cf9-a774-46161d6c6cfe', 'x-mitre-tactic--f72804c5-f15a-449e-a5da-2eecd181f813', 'x-mitre-tactic--9a4e74ab-5008-408c-84bf-a10dfbc53462', 'x-mitre-tactic--5569339b-94c2-49ee-afb3-2222936582c8', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e', 'x-mitre-tactic--7141578b-e50b-4dcc-bfa4-08a8dd689e9e']

TACTICS_TECHNIQUES_RELATIONSHIP_DF = pd.DataFrame({'TA0043': pd.Series(['T1595', 'T1592', 'T1589', 'T1590', 'T1591', 'T1598', 'T1597', 'T1596', 'T1593', 'T1594']),
                                        'TA0042': pd.Series(['T1583', 'T1586', 'T1584', 'T1587', 'T1585', 'T1588', 'T1608']),
                                        'TA0001': pd.Series(['T1189', 'T1190', 'T1133', 'T1200', 'T1566', 'T1091', 'T1195', 'T1199', 'T1078']),
                                        'TA0002': pd.Series(['T1059', 'T1609', 'T1610', 'T1203', 'T1559', 'T1106', 'T1053', 'T1129', 'T1072', 'T1569', 'T1204', 'T1047']),
                                        'TA0003': pd.Series(['T1098', 'T1197', 'T1547', 'T1037', 'T1176', 'T1554', 'T1136', 'T1543', 'T1546', 'T1133', 'T1574', 'T1525', 'T1556', 'T1137', 'T1542', 'T1053', 'T1505', 'T1205', 'T1078']),
                                        'TA0004': pd.Series(['T1548', 'T1134', 'T1547', 'T1037', 'T1543', 'T1484', 'T1611', 'T1546', 'T1068', 'T1574', 'T1055', 'T1053', 'T1078']),
                                        'TA0005': pd.Series(['T1548', 'T1134', 'T1197', 'T1612', 'T1622', 'T1140', 'T1610', 'T1006', 'T1484', 'T1480', 'T1211', 'T1222', 'T1564', 'T1574', 'T1562', 'T1070', 'T1202', 'T1036', 'T1556', 'T1578', 'T1112', 'T1601', 'T1599', 'T1027', 'T1647', 'T1542', 'T1055', 'T1620', 'T1207', 'T1014', 'T1553', 'T1218', 'T1216', 'T1221', 'T1205', 'T1127', 'T1535', 'T1550', 'T1078', 'T1497', 'T1600', 'T1220']),
                                        'TA0006': pd.Series(['T1557', 'T1110', 'T1555', 'T1212', 'T1187', 'T1606', 'T1056', 'T1556', 'T1111', 'T1621', 'T1040', 'T1003', 'T1528', 'T1558', 'T1539', 'T1552']),
                                        'TA0007': pd.Series(['T1087', 'T1010', 'T1217', 'T1580', 'T1538', 'T1526', 'T1619', 'T1613', 'T1622', 'T1482', 'T1083', 'T1615', 'T1046', 'T1135', 'T1040', 'T1201', 'T1120', 'T1069', 'T1057', 'T1012', 'T1018', 'T1518', 'T1082', 'T1614', 'T1016', 'T1049', 'T1033', 'T1007', 'T1124', 'T1497']),
                                        'TA0008': pd.Series(['T1210', 'T1534', 'T1570', 'T1563', 'T1021', 'T1091', 'T1072', 'T1080', 'T1550']),
                                        'TA0009': pd.Series(['T1557', 'T1560', 'T1123', 'T1119', 'T1185', 'T1115', 'T1530', 'T1602', 'T1213', 'T1005', 'T1039', 'T1025', 'T1074', 'T1114', 'T1056', 'T1113', 'T1125']),
                                        'TA0011': pd.Series(['T1071', 'T1092', 'T1132', 'T1001', 'T1568', 'T1573', 'T1008', 'T1105', 'T1104', 'T1095', 'T1571', 'T1572', 'T1090', 'T1219', 'T1205', 'T1102']),
                                        'TA0010': pd.Series(['T1020', 'T1030', 'T1048', 'T1041', 'T1011', 'T1052', 'T1567', 'T1029', 'T1537']),
                                        'TA0040': pd.Series(['T1531', 'T1485', 'T1486', 'T1565', 'T1491', 'T1561', 'T1499', 'T1495', 'T1490', 'T1498', 'T1496', 'T1489', 'T1529'])
                                        })

lift = attack_client()

tactics = lift.get_enterprise_tactics()
techniques = lift.get_enterprise_techniques()

header = ['Text']
for code in CODE_TACTICS:
    header.append(code)
for code in CODE_TECHNIQUES:
    header.append(code)

n = len(header) - 1

with open('./Entity-Extraction/rcATT/Dataset.csv', 'w', encoding="utf8") as dataset:
    writer = csv.writer(dataset, lineterminator = '\n')

    writer.writerow(header)

    i_tact = 0
    print('[🖋️ WRITING TACTICS]')
    for code in CODE_TACTICS:
        for tact in tactics:
            if tact['external_references'][0]['external_id'] == code:
                row = []
                row.append(tact['description'].replace("\n", " "))
                listofzeros = ['0'] * n
                listofzeros[i_tact] = '1'
                i_tact += 1

                for item in listofzeros:
                    row.append(item)
                
                writer.writerow(row)
        
    print('[🖋️ WRITING TECHNIQUES]')
    for code in CODE_TECHNIQUES:
        for tech in techniques:
            if tech['external_references'][0]['external_id'].split('.')[0] == code: # Also subtechniques but with label of main technique
                row = []
                row.append(tech['description'].replace("\n", " "))
                index = 15 + CODE_TECHNIQUES.index(code)
                listofzeros = ['0'] * n
                listofzeros[index - 1] = '1'                            # Index for the technique
                # Index for the tactic
                for code_tact in CODE_TACTICS:
                    for code_tech in TACTICS_TECHNIQUES_RELATIONSHIP_DF[code_tact]:
                        if code_tech == code:
                            listofzeros[CODE_TACTICS.index(code_tact)] = '1'

                for item in listofzeros:
                    row.append(item)

                writer.writerow(row)

                # Check if there is a url folder for that
                technique_name = tech['name'].replace("/", "_")
                url_dir_path = '../Entity-Extraction/rcATT/Dataset-Creation/URL_Content/' + technique_name + '/'
                if os.path.isdir(url_dir_path):
                    for url in os.listdir(url_dir_path):
                        url_row = []
                        url_path = url_dir_path + url
                        with open(url_path, 'r', encoding="utf8") as f:
                            content = f.read()
                            content = content.replace("\n", " ")
                            url_row.append(content)
                            for item in listofzeros:
                                url_row.append(item)
                            writer.writerow(url_row)

    print('[🖋️ ADDING rcATT DATASET]')
    with open('./Entity-Extraction/rcATT/Dataset-Creation/oldDataset.csv', 'r', encoding="utf8") as rcATT:
        reader = csv.reader(rcATT)
        rcATT_header = []
        rcATT_header = next(reader)

        # Problem: my header is 233 long and rcATT is 228 long, so I have to find what are the new techniques/tactics
        new_ttp_header = header[1:]
        old_ttp_header = rcATT_header[1:]

        old_ttp = []

        for rcATT_head in old_ttp_header:
            if rcATT_head not in new_ttp_header:
                old_ttp.append(rcATT_head)

        for i, line in enumerate(reader):
            rcATT_row = []
            text = line[0]
            old_ttp_indeces = line[1:]
            # Find all indeces where there is a '1'
            old_indeces = [i for i,j in enumerate(old_ttp_indeces) if '1' in j.lower()]

            # Find the corresponding index in the new format
            new_ttp_indeces = ['0'] * n
            for old_index in old_indeces:
                ttp_name = old_ttp_header[old_index]
                # Only if it's not one of the deprecated ones we add it to our list
                if ttp_name not in old_ttp:
                    new_index = new_ttp_header.index(ttp_name)
                    new_ttp_indeces[new_index] = '1'
            
            rcATT_row.append(text)
            for item in new_ttp_indeces:
                rcATT_row.append(item)
            writer.writerow(rcATT_row)