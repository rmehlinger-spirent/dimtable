__author__ = 'rmehlinger'

from django import template

register = template.Library()

# col_head_template, row_head_template, cell_template

def multi_table(
        data,
        cell_template       ='../templates/default-cell.html',
        row_header_template ='../templates/default-row-header.html',
        col_header_template ='../templates/default-col-header.html',
        corner_template     ='../templates/default-corner-template.html',
        row_title_template  ='../templates/default-row-title-template.html',
        col_title_template  ='../templates/default-col-title-template.html',
    ):

    return {
        'cell_template'         : cell_template,
        'row_header_template'   : row_header_template,
        'col_header_template'   : col_header_template,
        'corner_template'       : corner_template,
        'data'                  : data,
        'row_title_template'    : row_title_template,
        'col_title_template'    : col_title_template,
    }

register.inclusion_tag('../templates/multi-table.html', takes_context=False)(multi_table)