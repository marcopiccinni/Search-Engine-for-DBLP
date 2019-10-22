'''
import xml.etree.ElementTree as ET
tree = ET.parse('dblp.xml')
print(tree)
root=tree.getroot()
'''
import xmltodict as xml


def is_document(line):
    return line.startswith((b'article',
                            b'inproceedings',
                            b'proceedings',
                            b'book',
                            b'incollection',
                            b'phdthesis',
                            b'mastersthesis',
                            b'www'
                            ), 2)


class Parser:
    __t_doc = None
    __document = b''

    def document_start(self, w):
        # if self.__t_doc is not None:
        #   raise Exception("Type document is not None in Class Parser")
        if w.startswith(b'article', 1):
            self.__t_doc = b'article'
            return True
        elif w.startswith(b'inproceedings', 1):
            self.__t_doc = b'inproceedings'
            return True
        elif w.startswith(b'proceedings', 1):
            self.__t_doc = b'proceedings'
            return True
        elif w.startswith(b'book ', 1):
            self.__t_doc = b'book'
            return True
        elif w.startswith(b'incollection', 1):
            self.__t_doc = b'incollection'
            return True
        elif w.startswith(b'phdthesis', 1):
            self.__t_doc = b'phdthesis'
            return True
        elif w.startswith(b'mastersthesis', 1):
            self.__t_doc = b'mastersthesis'
            return True
        elif w.startswith(b'www', 1):
            self.__t_doc = b'www'
            return True
        return False

    def document_end(self, word):
        return word.endswith((b'article>',
                           b'inproceedings>',
                           b'proceedings>',
                           b'book>',
                           b'incollection>',
                           b'phdthesis>',
                           b'mastersthesis>',
                           b'www>'
                           ), 0, len(word))

    def parse(self, word):
        # print('[p]', word)
        is_start = self.document_start(word)
        if is_start:
            pass
            # print('start', word)
        self.__document += word
        is_end = self.document_end(word)
        if is_end:
           # print('end', word)
            pass

        if is_end:
            self.__t_doc = None
            print(self.__document)
            self.__document = b''
            pass  # -> parser
    # r = xml.parse(f)
    # print(r)


if __name__ == "__main__":
    with open('dblp.xml', 'rb') as f:
        P = Parser()

        for line in f:
            words = []
            if is_document(line):
                words = line.split(b'><')
                if len(words) == 2:
                    words[0] += b'>'
                    words[1] = b'<' + words[1]
                elif len(words) > 2:
                    raise Exception('Words Error ', len(words), words, line)
            else:
                words = [line]

            for word in words:
                P.parse(word.replace(b'\n', b'').replace(b'\r',b''))
