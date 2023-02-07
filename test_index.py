import pytest
from index import Indexer



def file_as_set(filename):
    '''
    Returns all of the non-empty lines in the file, as strings in a set.
    '''
    line_set = set()
    with open(filename, "r") as file:
        line = file.readline()
        while line and len(line.strip()) > 0:
            line_set.add(line.strip())
            line = file.readline()
    return line_set

def test_file_contents():
    simple_index = Indexer("wikis/SimpleWiki.xml", "simple_titles.txt",
       "simple_docs.txt", "simple_words.txt")
    simple_index.run() # run the indexer to write to the files
    titles_contents = file_as_set("simple_titles.txt")
    assert len(titles_contents) == 2
    assert "200::Example page" in titles_contents
    assert "30::Page with links" in titles_contents

def test_process():
    simple_index=Indexer("wikis/SimpleWiki.xml", "simple_titles.txt","simple_docs.txt", "simple_words.txt")
    simple_index.parse()
    assert simple_index.process_document("Page with links",30,"<!--A link that only has text between the [[ and ]] links to the page>")[0:3] == ["page","link","link"]
    assert "and" not in simple_index.process_document("Page with links",30,"<!--A link that only has text between the [[ and ]] links to the page>")
    assert "links" not in simple_index.process_document("Page with links",30,"<!--A link that only has text between the [[ and ]] links to the page>")

def test_tf_idf():
    tfindex=Indexer("wikis/test_tf_idf.xml","titlestf.txt","docstf.txt","wordstf.txt")
    tfindex.parse()
    assert tfindex.process_document("Page 1",1,"the dog bit the man")[0:3] == ["page","1","dog"]
    assert tfindex.compute_tf().get("chees") == {2: 1.0, 3: 1.0}
    assert tfindex.compute_tf().get("ate") == {2: 1.0}
    assert tfindex.compute_tf().get("bit") == {1:1.0,3:0.5}

    assert round(tfindex.compute_idf().get("bit"),3) == 0.405
    assert round(tfindex.compute_idf().get("dog"),3) == 0.405
    assert round(tfindex.compute_idf().get("chees"),3) == 0.405

def test_file_contents():
    simple_index = Indexer("wikis/SimpleWiki.xml", "simple_titles.txt", "simple_docs.txt", "simple_words.txt")
    simple_index.run() # run the indexer to write to the files
    titles_contents = file_as_set("simple_titles.txt")
    assert len(titles_contents) == 2
    assert "200::Example page" in titles_contents
    assert "30::Page with links" in titles_contents

def test_page_rank():
    index1 = Indexer("wikis/PageRankExample1.xml", "simple_titles.txt", "simple_docs.txt", "simple_words.txt")
    simple_index = Indexer("wikis/SimpleWiki.xml", "simple_titles.txt", "simple_docs.txt", "simple_words.txt")
    simple_index.parse()
    assert round(simple_index.compute_page_rank().get(30),1)==0.5
    index1.parse()
    assert round(index1.compute_page_rank().get(1),4)==0.4326
    assert round(index1.compute_page_rank().get(2),4)==0.2340
    assert round(index1.compute_page_rank().get(3),4)==0.3333

def term_relevance():
    tfindex=Indexer("wikis/test_tf_idf.xml","titlestf.txt","docstf.txt","wordstf.txt")
    tfindex.parse()
    assert round(tfindex.compute_term_relevance().get("dog").get(1),4) == 0.4054
    assert round(tfindex.compute_term_relevance().get("chees").get(2),4) == 0.4054

