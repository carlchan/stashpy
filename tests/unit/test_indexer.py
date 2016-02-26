import unittest
from datetime import datetime

import stashpy

sentinel = object()

class MockEsConn:
    def __init__(self, *args):
        self.puts = []

    def put(self, index, type, uid, contents, callback):
        self.puts.append((index, type, uid, contents))
        return sentinel

class IndexerTests(unittest.TestCase):

    def test_simple_indexing(self):
        doc = {'name':'Lilith', 'age': 4}
        indexer = stashpy.ESIndexer('localhost', 9200, connection=MockEsConn)
        return_val = indexer.index(doc)
        self.assertEqual(return_val, sentinel)
        index,type,uid,indexed_doc = indexer.es_connection.puts[0]
        self.assertDictEqual(doc, indexed_doc)
        self.assertEqual(index, datetime.strftime(datetime.now(), "stashpy-%Y-%m-%d"))


    def test_index_pattern_in_doc(self):
        doc = {'name':'Lilith', 'age': 4, '_index_':'Kita-%Y'}
        indexer = stashpy.ESIndexer('localhost', 9200, connection=MockEsConn)
        return_val = indexer.index(doc)
        self.assertEqual(return_val, sentinel)
        index,type,uid,indexed_doc = indexer.es_connection.puts[0]
        self.assertDictEqual(doc, indexed_doc)
        self.assertEqual(index, datetime.strftime(datetime.now(), "Kita-%Y"))

    def test_index_pattern_not_date(self):
        doc = {'name':'Lilith', 'age': 4, '_index_':'Kita-2016'}
        indexer = stashpy.ESIndexer('localhost', 9200, connection=MockEsConn)
        return_val = indexer.index(doc)
        self.assertEqual(return_val, sentinel)
        index,type,uid,indexed_doc = indexer.es_connection.puts[0]
        self.assertDictEqual(doc, indexed_doc)
        self.assertEqual(index, datetime.strftime(datetime.now(), "Kita-2016"))