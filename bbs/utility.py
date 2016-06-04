#_*_coding:utf-8_*_

import models
from s10day12bbs import settings
from models import Article,UserProfile,Category
class Bbs_generater(object):

    def __init__(self,request):
        self.request = request

    def handle_upload_file(request,obj_file):
        upload_dir = '%s/%s' %(settings.BASE_DIR,settings.UPLOAD_DIR)
        print upload_dir
        with open('%s/%s' %(upload_dir,obj_file.name),'wb') as destination:
            for chunk in obj_file.chunks():
                destination.write(chunk)
        return obj_file.name

    def parse_data(self):
        file_name = self.handle_upload_file(self.request.FILES['title_img'])
        cate_id = self.request.POST.get('cate_id')
        article_cate = Category.objects.get(id=cate_id)
        form_data ={
        'title' : self.request.POST.get('title'),
        'brief' : self.request.POST.get('brief'),
        'content' : self.request.POST.get('content'),
        'author' : self.request.user.userprofile,
        'category' : article_cate,
        'head_img':'static/imgs/upload/%s' %(file_name),
        }
        return form_data

    def create(self):
        self.form_list = self.parse_data()
        article = Article(**self.form_list)
        article.save()
        return article


    def update(self):
        pass

def recursive_dic(data_dic,comment):
    for parent,v in data_dic.items():
        if parent == comment.parent_comment:
            data_dic[parent][comment] = {}
        else:
            recursive_dic(data_dic[parent],comment)


def create_comment_tree(request,article_id):
    bbs_obj = models.Article.objects.get(id=article_id)
    tree_dic = {}
    for comment in bbs_obj.comment_set.select_related():
        if not comment.parent_comment:  #have not parent
            tree_dic[comment] = {}
        else:
            recursive_dic(tree_dic,comment)

    return tree_dic

