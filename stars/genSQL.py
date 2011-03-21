# -*- coding:utf-8 -*-
def Dict2Str(dictin):
    # make dict to str, with the format key='value'
    #tmpstr=''
    tmplist=[]
    for k,v in dictin.items():
        tmp = str(k)+'='+'\''+str(v)+'\''
        tmplist.append(' '+tmp+' ')
    return ','.join(tmplist)
def gen_update(table,file_id_dict,some_dicts):
    # file_id_dict maybe the Condition, in sql, where key='value'
    # some_dicts are the values to update
    # Here, I assume file_id_dict is a dictionary,
    # so that Can reuse
    sql = ''
    sql += 'update %s '%table
    sql += ' set %s'%Dict2Str(some_dicts)
    sql += ' where %s'%Dict2Str(file_id_dict)
    return sql

def gen_insert(table,known_dict):
    '''
    >>> kdict = {'name':'lin','age':22}
    >>> geninsertsql('persons',kdict)
    insert into person (name,age) values ('lin',22)
    '''
    sql = 'insert into %s '%table
    ksql = []
    vsql = []
    for k,v in known_dict.items():
        ksql.append(str(k))
        vsql.append('\''+str(v)+'\'')
    sql += ' ('+','.join(ksql)+') '
    sql += ' values ('+','.join(vsql)+')'
    return sql

def gen_select(table,keys,conditions):
    sql = 'select %s '%keys
    sql += ' from %s '%table
    sql += ' where %s '%Dict2Str(conditions)
    return sql
def gensql(*args):
    from types import StringType
    if len(args) == 2 :
        return gen_insert(*args)
    elif len(args) == 3 :
        if type(args[1]) == StringType:
            return gen_select(*args)
        else:
            return gen_update(*args)
    else:
        return None
if __name__ == '__main__':
    print gensql('NextIDs','ID',{'TableName':'RealRawReplicas'})      # select
    print gensql('NextIDs',{'TableName':'RealRecFiles','ID':'0'})     # insert
    print gensql('NextIDs',{'TableName':'RealRecFiles'},{'ID':'1'})   # update
