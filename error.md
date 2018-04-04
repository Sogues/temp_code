## ERROR 1
    HEAD detached at origin/master
    http://blog.csdn.net/sinat_26415011/article/details/54346318

## ERROR2
     Your local changes to the following files would be overwritten by merge
     The following untracked working tree files would be overwritten by merge:
     solution: git clean -d -fx

## ERROR3
    >>>a                       
    {a': 1, 'b': 2, 'c': {'c1': 1, 'c2': 2}}
    >>>cur = a.get('c')        
    >>>cur
    {'c1': 1, 'c2': 2}}
    >>>cur.pop('c1')           
    >>>cur
    {'c2':2}
    >>>a                       
    {a': 1, 'b': 2, 'c': {1, 'c2': 2}}
   
## ERROR4
   mysqlclient failed to install
   fix:
       sudo apt-get install python-dev libmysqlclient-dev
       pip install mysqlclient
