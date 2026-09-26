# Browser Download Isolation

Downloads are bounded by byte size and an explicit extension allowlist before they become task artifacts. The browser runtime must additionally isolate its download directory, prevent path traversal, scan/validate artifacts before delivery, and never expose host filesystem paths to untrusted web content.