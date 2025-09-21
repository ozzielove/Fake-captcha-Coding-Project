/* LAB ONLY - Minimal YARA rule. TODO: VERIFY tuning before production. */
rule PS_EncodedCommand_Indicator
{
    meta:
        author = "lab-blue-team"
        date = "2025-09-21"
        description = "Flags presence of EncodedCommand indicators"
    strings:
        $a = "-EncodedCommand"
        $b = " -enc "
    condition:
        any of them
}
