/* LAB ONLY - Minimal YARA rule for HTML smuggling indicators. */
rule HTML_Smuggling_Indicator
{
    meta:
        author = "lab-blue-team"
        date = "2025-09-21"
        description = "Flags scripts referencing clipboard or base64 blobs (lab)"
    strings:
        $a = "navigator.clipboard.writeText"
        $b = "atob("
        $c = "EncodedCommand"
    condition:
        1 of ($a, $b, $c)
}
