# ----------------------------------------------------------------------
# Table is used to render a multidimensional HTML table
# ----------------------------------------------------------------------
from .dimtable import Indexer, DimIter, Dim, LabelItem
import json

class Table:
    def __init__(self, 
                 coldims,
                 rowdims,
                 data=None,
                 **kwargs):
        self.coldims   = coldims if hasattr(coldims, '__iter__') else [coldims]
        self.rowdims   = rowdims if hasattr(rowdims, '__iter__') else [rowdims]

        self.degenerate = False

        if not self.coldims:
            self.coldims = [Dim(name='', items=[LabelItem('')])]
            self.degenerate = True
        if not self.rowdims:
            self.rowdims = [Dim(name='', items=[LabelItem('')])]
            self.degenerate = True

        self.dims      = sorted(self.coldims + self.rowdims, key=lambda x: x.name)
        self._data     = data

        self.indexer = Indexer(self.coldims, self.rowdims)

        self.col_groups = [self.col_group(cix) for cix in range(len(self.coldims))]
        self.num_cols = len(self.col_groups[-1]['columns'])

        for group in self.col_groups:
            group['num_titles'] = range(self.num_cols//(group['span'] * len(group['col_set'])))

        self.rows = self.__rows()
        self.corner = {'rowspan': len(self.coldims),
                       'colspan': len(self.rowdims)}

        self.dimension_json = json.dumps(sorted([dim.name for dim in self.dims]))
        self.col_dim_json = json.dumps(sorted([dim.name for dim in self.coldims]))
        self.row_dim_json = json.dumps(sorted([dim.name for dim in self.rowdims]))

    def col_group(self, ix):
        dim = self.coldims[ix]
        citer = DimIter(self.coldims[:ix + 1])
        cspan = self.colspan(ix)
        cols = dim.items

        col_list = []
        while not citer.end():
            keyed_dims = self.get_keyed_index(rixes=None, cixes=citer.get())
            if dim.name:
                col_list.append({'val': keyed_dims[dim.name], 'dimensions': keyed_dims})
            citer.next()

        return {'columns': col_list,
                'col_set': cols,
                'span': cspan,
                'name': dim.name,
                'title_span': cspan * len(cols)}

    def __rows(self):
        riter = DimIter(self.rowdims)

        rs = []
        dix = 0

        while True:
            rs.append(self.row(dix, riter.get()))
            dix = riter.next()
            if riter.end(): break
        return rs

    def row(self, dim_ix, riter_index):
        return {'headers': self.row_headers(dim_ix, riter_index), 'cells': self.row_cells(riter_index)}

    def row_headers(self, dim_ix, rixes):
        ret = []

        dim_indices = []
        for index in range(len(self.rowdims)):
            dim = self.rowdims[index]
            vix = rixes[index]
            dim_indices.append(vix)

            if index >= dim_ix:
                item = dim.items[vix]
                tmp = {'item': item, 'span': self.rowspan(index), 'first_header': vix==0,
                            'title_span': self.rowspan(index-1), 'name': dim.name,
                            'dimensions': self.get_keyed_index(rixes=tuple(dim_indices), cixes=None)}
                ret.append(tmp)
        return ret

    def row_cells(self, rixes):
        tds = []
        citer = DimIter(self.coldims)
        while not citer.end():
            tds.append(self.cell(self.get_keyed_index(rixes, citer.get())))
            citer.next()

        return tds

    def rowspan(self, ix):
        if ix + 1 > len(self.rowdims) - 1:
            return 1
        else:
            return len(self.rowdims[ix + 1].values()) * self.rowspan(ix + 1)

    def get_keyed_index(self, rixes, cixes):
        ret = {}
        if rixes is not None:
            ret.update({
                self.rowdims[i].name: self.rowdims[i].items[v].value() for i, v in enumerate(rixes) if self.rowdims[i].name
            })

        if cixes is not None:
            ret.update({
                self.coldims[i].name: self.coldims[i].items[v].value() for i, v in enumerate(cixes) if self.coldims[i].name
            })
        return ret

    # cell-method should be implemented by subclasses
    def cell(self, cellix):
        return {
            'cell': self._data.get(cellix) if self._data else u'',
            'position': cellix,
        }

    def colspan(self, ix):
        if ix + 1 > len(self.coldims) - 1:
            return 1
        else:
            return len(self.coldims[ix + 1].values()) * self.colspan(ix + 1)

    def num_rows(self):
        return len(self.rows)