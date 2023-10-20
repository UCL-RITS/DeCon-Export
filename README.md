# DeCon

Some work around getting data out of Confluence.

Some actions use the Confluence API and some of those require you to authenticate using a token.

 - `get_spaces.py` retrieves a list of all the Spaces your user can see in a Confluence wiki, and dumps it out to a `spaces.json` file.
 - `confluence_object_defs.py` contains dataclass definitions for types of object observed within Confluence XML exports.
 - `wiki2storage.py` uses the Confluence API to convert between Confluence's internal formats, as well as the presentable HTML-segment "view" format.
 - `space_export.py` is some very rough code for parsing the `entities.xml` file you get from a Confluence XML export into a collection of objects, and dumping out the pages as separate files. Several problems with using this remain unsolved.


## Problems

 - what to name dumped files
 - hierarchy of files
 - wiring the links back together
 - many things around attachments
 - rendering comments to pages
 - some problems observed around `<![CDATA[` use in body content, not fully diagnosed yet

