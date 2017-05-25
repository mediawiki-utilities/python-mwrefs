import mwcli

router = mwcli.Router(
    "mwrefs",
    "A set of utilities for extracting and processing <ref>s in " +
    " MediaWiki projects.",
    {'diffs': "Extracts changes to <ref>s from XML dumps",
     'extract': "Extracts all <ref>s from XML dumps",
     'fetch_references': "Gets the reference documents for a revision from " +
                         "the a MediaWiki API"}
)

main = router.main
