# MediaWiki References

Extracts references from MediaWiki with a focus on Wikipedia

This library provides a command-line utility for extracting references from MediaWiki XML database dumps. 


    $ mwrefs -h
    
    This script provides access to a set of utilities for processing references
    in Wikipedia.
    
    * extract -- All <ref> tags from articles
    * diffs -- Extracts changes in references historically.
    
    Usage:
        mwrefs (-h | --help)
        mwrefs <utility> [-h | --help]
    
    Options:
        -h | --help  Shows this documentation
        <utility>    The name of the utility to run
