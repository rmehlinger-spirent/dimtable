from setuptools.compat import unicode
from .dimtable import Table, DimIter

__author__ = 'rmehlinger'


class KeyedTable(Table):
    def get_keyed_index(self, rixes, cixes):
        ret = {
            self.rowdims[i].name: self.rowdims[i].items[rixes[i]].value() for i in range(len(rixes))
        }

        ret.update({
            self.coldims[i].name: self.coldims[i].items[cixes[i]].value() for i in range(len(cixes))
        })

        return ret

    def cell(self, cellix):
        cellid = "table_cell_" + str(cellix).replace(' ', '_')
        celldata = unicode(self._data.get(cellix)) if self._data else u'n/a'
        return u''.join(['<td id="', cellid, '">', celldata, '</td>'])

    def row_cells(self, rixes):
        tds = []
        citer = DimIter(self.coldims)
        while not citer.end():
            tds.append(self.cell(self.get_keyed_index(rixes, citer.get())))
            citer.next()

        return tds