from nose.tools import eq_

from ..extract import extract


def test_extract():
    text = """<!-- <ref> -->
    [[File:Tree of life by Haeckel.jpg|thumb|[[Ernst Haeckel]]'s Tree of Life (1879)]]
    The term ''[[wikt:biology|biology]]'' is derived from the [[Greek Language|Greek]]
    word {{lang|grc|[[wikt:βίος|βίος]]}}, ''bios'', "[[life]]" and the suffix
    {{lang|grc|[[wikt:-λογία|-λογία]]}}, ''-logia'', "study of."<ref>{{cite web
    |url=http://topics.info.com/Who-coined-the-term-biology_716 |title=Who coined
    the term biology? |work=Info.com|accessdate=2012-06-03}}</ref>
    <ref name=OnlineEtDict>{{cite web|title=biology
    |url=http://www.etymonline.com/index.php?term=biology&allowed_in_frame=0
    |publisher=[[Online Etymology Dictionary]]}}</ref>
    The Latin form<ref name="pete"/> of the term first<ref name=bob /> appeared
    in 1736 when Swedish scientist
    [[Carl Linnaeus]] (Carl von Linné) used ''biologi'' in his ''Bibliotheca
    botanica''. It was used again in 1766 in a work entitled ''Philosophiae
    naturalis sive physicae: tomus III, continens geologian, biologian,
    phytologian generalis'', by [[Michael Christoph Hanow|Michael Christoph
    Hanov]], a disciple of [[Christian Wolff (philosopher)|Christian Wolff]].
    The first German use, ''Biologie'', was used in a 1771 translation of
    Linnaeus' work. In 1797, Theodor Georg August Roose used the term in a
    book, ''Grundzüge der Lehre van der Lebenskraft'', in the preface. [[Karl
    Friedrich Burdach]] used the term in 1800 in a more restricted sense of
    the study of human beings from a morphological, physiological and
    psychological perspective (''Propädeutik zum Studien der gesammten
    Heilkunst''). The term came into its modern usage with the six-volume
    treatise ''Biologie, oder Philosophie der lebenden Natur'' (1802–22) by
    [[Gottfried Reinhold Treviranus]], who announced:<ref name=Richards>
    {{cite book|last=Richards|first=Robert J.|title=The Romantic Conception of
    Life: Science and Philosophy in the Age of Goethe|year=2002
    |publisher=University of Chicago Press|isbn=0-226-71210-9
    |url=http://books.google.cocover#v=onepage&q&f=false}}</ref>
    <ref name="Richards">foobar</ref>
    <references/>"""

    refs = list(extract(text))

    eq_(refs,
        ['<ref>{{cite web\n    |url=http://topics.info.com/Who-coined-the-' +
           'term-biology_716 |title=Who coined\n    the term biology? |work=' +
           'Info.com|accessdate=2012-06-03}}</ref>',
         '<ref name=OnlineEtDict>{{cite web|title=biology\n    |url=http://' +
           'www.etymonline.com/index.php?term=biology&allowed_in_frame=0\n   ' +
           ' |publisher=[[Online Etymology Dictionary]]}}</ref>',
         '<ref name="pete"/>', '<ref name=bob />',
         '<ref name=Richards>\n    {{cite book|last=Richards|first=Robert J.' +
           '|title=The Romantic Conception of\n    Life: Science and ' +
           'Philosophy in the Age of Goethe|year=2002\n    |publisher=' +
           'University of Chicago Press|isbn=0-226-71210-9\n    ' +
           '|url=http://books.google.cocover#v=onepage&q&f=false}}</ref>',
         '<ref name="Richards">foobar</ref>'])
