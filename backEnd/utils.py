from database import query_article_count

def article_filer(id: int) -> bool:
    '''文章是否存在'''
    if (id is None) or (id < 1) or (id > query_article_count()):
        return False
    else:
        return True