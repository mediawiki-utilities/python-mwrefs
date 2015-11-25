supported = {'en', 'it'}

bibliography = {
    'en': {
        'bibliography',
        'references',
        'reference',
        'further reading',
        'notes',
        'sources',
        'footnotes',
        'citations',
        'publications',
        'publication history',
        'literature',
    },
    'it': {'bibliografia'},
}

citation = {
    'en': {'Citation', 'cite', 'vcite'},
}

"""
What I mean for:
* References: a section containing footnotes for works cited in the text.
* Bibliography: a section containing articles and journals.
* Further reading: like `Bibliography`, but contains references not used in the text.
* Footnotes: a section containing explainations to concepts.

From now on, words in backquotes (`) are to be interpreted as concept using the above definitions, while words in double quotes (") are to be interpreted as terms found in the text of the articles.

"References" (term) is commonly used as `Bibliography` (concept), i.e. articles and journals without backref to the text.
And, of course, "Bibliography" (term) is sometimes used as `References` (concept).
* https://en.wikipedia.org/w/index.php?title=Anabaptists&oldid=49953891 "References" interpreted as `Bibliography`
* https://en.wikipedia.org/w/index.php?title=Alcopop&oldid=296736852 "References" interpreted as `Bibliography`
* https://en.wikipedia.org/w/index.php?title=Amu%20Darya&oldid=66374611 "References" interpreted as `Bibliography`

"Citations" (term) sometimes used as synonym for "References" or "Bibliography" (terms):
* https://en.wikipedia.org/w/index.php?title=Augustine_of_Canterbury&oldid=676642624 "Citations" used as `References`, "References" used as `Bibliography`
* https://en.wikipedia.org/w/index.php?title=Anemometer&oldid=674186492#Citations "Citations" used as `References`

"Notes and References" and "References and Notes" (terms) are used as synonyms for "References" (term):
* https://en.wikipedia.org/w/index.php?title=Ackermann%20function&oldid=335603599#Notes_and_references "Notes and References" converted to "References" (term) and interpreted as `References`
* https://en.wikipedia.org/w/index.php?title=albanians&oldid=391045161#Notes_and_references "Notes and References" is a wrapper around "Notes" (interpreted as `footnotes`) and "References" (interpreted as `References`)
* https://en.wikipedia.org/w/index.php?title=assassination&oldid=678057527#Notes_and_references interpreted as `References`

"Sources" seems to be interpreted as `Bibliography` or `References`, and sometimes then converted by users to "References" or "Bibliography"
* https://en.wikipedia.org/w/index.php?title=artemis&diff=next&oldid=565871969 "Sources" has been converted to "References and sources"
* https://en.wikipedia.org/w/index.php?title=Amakusa&direction=next&oldid=667294099 "Sources" used as `Bibliography`
* https://en.wikipedia.org/w/index.php?title=A%20Doll's%20House&oldid=676505492#Sources "Sources" used as `Bibliography`
* https://en.wikipedia.org/w/index.php?title=A.%20E.%20Housman&diff=next&oldid=678259900#Sources "Sources" used `Bibliography`

"Footnotes" is commonly interpreted as `References`, with the following terms: "References" and "Citations"
* https://en.wikipedia.org/w/index.php?title=Augustine%20of%20Canterbury&oldid=459457206#Footnotes "Footnotes" is used as `References`; "Footnotes" is then converted to "Citations", used as `References`
* https://en.wikipedia.org/w/index.php?title=Amoxicillin&diff=next&oldid=423375138 "Footnotes" used as and converted to `References`
* https://en.wikipedia.org/w/index.php?title=Anabaptists&oldid=49953891#Footnotes_and_references "Footnotes" interpreted as `References`. The next revision converts "Footnotes" to "Footnotes and References".
* https://en.wikipedia.org/w/index.php?title=Alcopop&oldid=296736852#Footnotes "Footnotes" used as `References`
* https://en.wikipedia.org/w/index.php?title=Archaeopteryx&diff=next&oldid=326796096 "Footnotes" interpreteda s and then converted to `References` (term and concept)
* https://en.wikipedia.org/w/index.php?title=Al%20Capp&oldid=590148186#Footnotes "Footnotes" interpreted as `References`. It is then converted to "Notes"
* https://en.wikipedia.org/w/index.php?title=Amu%20Darya&oldid=66374611#Footnotes "Footnotes" interpreted as `References`. Later converted to "Notes"
* https://en.wikipedia.org/w/index.php?title=Albert%20Brooks&oldid=150996845#Footnotes "Footnotes" used as and then converted to `References` (term and concept)

"Literature" is used most of the times as a subsection for things like "Culture", and in some cases is a replacement for "bibliography":
* https://en.wikipedia.org/w/index.php?title=Alexandria&oldid=678355005 "Literature" used as subsection of "Culture"
* https://en.wikipedia.org/w/index.php?title=Bible&oldid=23508742#Literature "Literature" used as `Bibliography`
* https://en.wikipedia.org/w/index.php?title=Board_game&oldid=7131437#Literature "Literature" used as "Bibliography", then converted to "References" (used as "Bibliography")
* https://en.wikipedia.org/w/index.php?title=Ahuitzotl&oldid=118183827 "Literature" interpreted as `Bibliography`

"Publications" and "Publication history" are used as a subsection for the "Biography" with the works of the person described.

"Reference" is almost always converted to "References" in a successive revision.


"Notes" is sometimes interpreted as `References` or `Footnotes`
* https://en.wikipedia.org/w/index.php?title=Ahuitzotl&oldid=118183827 "Notes" used as `Footnotes`
* https://en.wikipedia.org/w/index.php?title=Archaeoastronomy&oldid=678777218#Notes "Notes" used as `References`
* https://en.wikipedia.org/w/index.php?title=Alexander_of_Hales&oldid=661215939#Other_historical_works "Notes" interpreted as `References`

"See also" and "Related pages" usually contain links to other wikipedia pages.
"""

