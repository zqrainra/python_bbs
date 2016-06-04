from django import template

register = template.Library()

def create_comment(data_dic,margin_left):
    html = ''
    for k,v in data_dic.items():

        r = """<div style="margin-left:%spx">
        <span>%s</span>
        <span>%s</span>
        <span>%s</span>
        </div>""" % (margin_left,k.user.name, k.comment, k.date)

        if v is not None:
            r += create_comment(v,margin_left+10)

        html += r

    return html



@register.simple_tag
def create_tree(data_dic,margin_left):
    html_ele = ''
    if not data_dic:
        return html_ele
    # print data_dic

    for k, v in data_dic.items():
        r = """<div style="margin-left:%spx">
        <span>%s</span>
        <span>%s</span>
        <span>%s</span>
        </div>""" % (margin_left,k.user.name, k.comment, k.date)

        if v is not None:
            r += create_comment(v,margin_left+10)

        html_ele += r
    return html_ele
    # return data_dic


