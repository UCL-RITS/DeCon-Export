"""
This is intended to work on a Confluence Space export, converting the contents into Markdown files.

Format and title conversion remains a problem.
"""

import xml.etree.ElementTree

from dataclasses import dataclass
import confluence_object_defs as cod

import urllib.parse
enc = urllib.parse.quote_plus

import yaml
import pypandoc

# The path to the unzipped Confluence space export
# This should probably be a path object instead or something
export_dir = "ARC_Export"

# Directory to dump all the output files into
# Similarly, should probably use path objects
dump_dir = "dump_dir"

def main():
    space = parse_space(export_dir + "/entities.xml")
    page_list_out = open("page_list.txt", 'w')
    for page in space["Page"]:
        #print(space["Page"][page].LowerTitle)
        #print(enc(space["Page"][page].Title))
        page_title = space["Page"][page].Title
        page_title_safe = safe_title(page_title)
        page_list_out.write(f"{page_title}\n")
        page_list_out.write(f"{page_title_safe}\n")
        
        p = space["Page"][page]
        with open(dump_dir + "/" + p.Id + ".yaml", 'w') as one_output_page_file:
            one_output_page_file.write(dump_page(space,p))
        if (space["Page"][page].ParentId == None) and (space["Page"][page].OriginalVersionId == None):
            print(f"Found root page: id={p.Id} title={p.Title}")
        # Debug: if you just want to dump the root page to see
        #    print(f"BodyContents: {p.BodyContentsIds}")
        #    print(dump_page(space,p))


def dump_page(space, page):
    # Might replace this with a Mako template or something
    header = yaml.dump(page)
    page_content = space["BodyContent"][page.BodyContentsIds[0]].Body

    if page_content == None:
        page_content = ""

    # Having some problems with passing nested <[[CDATA blocks through this at the moment >:/
    #page_content = page_to_markdown(page_content)

    return header + "---\n" + page_content

def page_to_markdown(content):
    import wiki2storage as w
    view_format = w.s2v(content)
    md = pypandoc.convert_text(view_format, 'gfm', format='html')
    return md


def parse_space(entity_file = "entities.xml"):
    space_dump_tree = xml.etree.ElementTree.ElementTree(file = entity_file)

    root = space_dump_tree.getroot()

    logf = open("log", 'a')

    objects = dict()
    failures = dict()
    for child in root:
        # These classes weren't in my existing list or didn't parse the same way as the others.
        if child.attrib["class"] == "BucketPropertySetItem":
            # These have an awkward composite ID and I don't think we have any use for them anyway
            continue
        if child.attrib["class"] == "Notification":
            # I don't see us doing anything useful with these
            continue
        if child.attrib["class"] == "LikeEntity":
            # I don't know what these are and I am choosing to ignore them (probably "likes" on pages)
            continue
        if child.attrib["class"] == "CustomContentEntityObject":
            # I don't know what these are and I should probably find out
            # I think they're usually those special comments that go in a place off to the side instead of down at the bottom.
            # Maybe it's an extensible object used for things Confluence extensions need to store
            continue
        if child.attrib["class"] not in objects:
            objects[child.attrib["class"]] = dict()
        fields = get_fields(child)

        try:
            objects[child.attrib["class"]][get_id(child)] = cod.__dict__[child.attrib["class"]](**fields)
        except TypeError as e:
            # These TypeErrors occur when a field we didn't know was optional turns out to be optional.
            # If they come up, it usually means you just have to add a default field value in the object defs
            #  and re-run. (I've used None as the default value in those cases.)
            logf.write(str(e) + "\n")
            if child.attrib["class"] not in failures:
                failures[child.attrib["class"]] = 1
            else:
                failures[child.attrib["class"]] += 1


    for className in objects.keys():
        print(f"Got {className}: {len(objects[className])}") 

    for className in failures.keys():
        print(f"Failed {className}: {failures[className]}")

    return objects
        

def get_id(obj):
    """
    Extract just the ID field of a Confluence object.
    """
    for prop in obj:
        if prop.tag == "id":
            return prop.text
    raise KeyError

def get_fields(obj):
    """
    Gets all the fields of a Confluence exported object, assembling in a dictionary.
    """
    props = dict()
    for prop in obj:
        if prop.tag == "id":
            props["Id"] = prop.text
        if prop.tag == "property":
            if prop.find("id") != None:
                props[cap_first(prop.attrib["name"])+"Id"] = prop.find("id").text
            else:
                props[cap_first(prop.attrib["name"])] = prop.text
        if prop.tag == "collection":
            l = list()
            for element in prop:
                l.append(element.find("id").text)
            props[cap_first(prop.attrib["name"])+"Ids"] = l
    return props

def cap_first(s):
    """
    Capitalises just the first letter of a string, since the usual
    str.capitalize method lowercases the entire rest of the string as well.
    """
    return s[0].upper() + s[1:]


# Yes, yes, this is a horrible textual crime.
def safe_title(t):
    ratio_character = "∶"
    fullwidth_solidus = "／"
    fullwidth_colon = "："  

    t = t.replace(":", fullwidth_colon)
    t = t.replace("/", fullwidth_solidus)

    return t


## Known classes of object
# Attachment
# BodyContent
# BucketPropertySetItem
# Comment
# ConfluenceBandanaRecord
# ConfluenceUserImpl
# ContentProperty
# CustomContentEntityObject
# Label
# Labelling
# LikeEntity
# Notification
# OutgoingLink
# Page
# Space
# SpaceDescription
# SpacePermission
# User2ContentRelationEntity


if __name__ == "__main__":
    main()
