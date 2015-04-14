# -*- encoding:utf8 -*-

import settings
import re


class Parser(object):

    @classmethod
    def get_document_id(cls, target_keyword):
        # Convert keyword
        target_keyword = cls._convert_unicode(target_keyword)

        doc_dic = settings.DOCUMENTS
        for sets in doc_dic:
            keywords = sets['Keywords']
            if isinstance(keywords, list):
                for keyword in keywords:
                    if cls._is_match_keyword(target_keyword, cls._convert_unicode(keyword)):
                        return sets['DocumentID']
            else:
                if cls._is_match_keyword(target_keyword, cls._convert_unicode(keywords)):
                    return sets['DocumentID']
        return None

    @classmethod
    def get_documentid_keyword_list(cls):
        doc_dic = settings.DOCUMENTS
        lists = []
        for sets in doc_dic:
            keywords = sets['Keywords']
            if isinstance(keywords, list):
                keywords = "[{0}]".format(", ".join(keywords))
            lists.append("{0}: {1}".format(keywords, sets['DocumentID']))
        return lists

    @classmethod
    def get_keyword_list(cls):
        doc_dic = settings.DOCUMENTS
        lists = []
        for sets in doc_dic:
            keywords = sets['Keywords']
            if isinstance(keywords, list):
                keywords = "[{0}]".format(", ".join(keywords))
            lists.append(keywords)
        return lists

    @classmethod
    def _convert_unicode(cls, text):
        if isinstance(text, unicode):
            return text
        # If text is string, will be decode
        if isinstance(text, str):
            return text.decode('utf-8')
        raise Exception("Target keyword type should be unicode : %r" % (type(text)))

    @classmethod
    def _is_match_keyword(cls, keyword1, keyword2):
        return re.compile('^%s$' % keyword1, settings.RE_FLAGS).match(keyword2)
