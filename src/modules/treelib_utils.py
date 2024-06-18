'''
 https://stackoverflow.com/questions/46345677/treelib-prints-garbage-instead-of-pseudographics-in-python3
 - CODE taken from HERE makes our life much easier.
 Not going to lie I didn't read it but it does work. From a glance there's nothing wrong as it's just a recursive functions
 and we will call it at the start of the game running so its not like there's going to be performance problems and no global
 variables to trouble us in the future so we good.

'''

from treelib import Tree

def create_node(tree : Tree, s, counter_byref, verbose, parent_id=None):
    node_id = counter_byref[0]
    if verbose:
        print(f"tree.create_node({s}, {node_id}, parent={parent_id})")

    tree.create_node(s, node_id, parent=parent_id)

    counter_byref[0] += 1
    return node_id

def to_compact_string(o):
    if type(o) == dict:
        if len(o)>1:
            raise Exception()
        k,v =next(iter(o.items()))
        return f'{k}:{to_compact_string(v)}'
    elif type(o) == list:
        if len(o)>1:
            raise Exception()
        return f'[{to_compact_string(next(iter(o)))}]'
    else:
        return str(o)

def to_compact(tree, o, counter_byref, verbose, parent_id):
    try:
        s = to_compact_string(o)
        if verbose:
            print(f"# to_compact({o}) ==> [{s}]")
        create_node(tree, s, counter_byref, verbose, parent_id=parent_id)
        return True
    except:
        return False

def json_2_tree(o , parent_id=None, tree=None, counter_byref=[0], verbose=False, compact_single_dict=False, listsNodeSymbol='+'):
    if tree is None:
        tree = Tree()
        parent_id = create_node(tree, '+', counter_byref, verbose)
    if compact_single_dict and to_compact(tree, o, counter_byref, verbose, parent_id):
        # no need to do more, inserted as a single node
        pass
    elif type(o) == dict:
        for k,v in o.items():
            if compact_single_dict and to_compact(tree, {k:v}, counter_byref, verbose, parent_id):
                # no need to do more, inserted as a single node
                continue
            key_nd_id = create_node(tree, str(k), counter_byref, verbose, parent_id=parent_id)
            if verbose:
                print(f"# json_2_tree({v})")
            json_2_tree(v , parent_id=key_nd_id, tree=tree, counter_byref=counter_byref, verbose=verbose, listsNodeSymbol=listsNodeSymbol, compact_single_dict=compact_single_dict)
    elif type(o) == list:
        if listsNodeSymbol is not None:
            parent_id = create_node(tree, listsNodeSymbol, counter_byref, verbose, parent_id=parent_id)
        for i in o:
            if compact_single_dict and to_compact(tree, i, counter_byref, verbose, parent_id):
                # no need to do more, inserted as a single node
                continue
            if verbose:
                print(f"# json_2_tree({i})")
            json_2_tree(i , parent_id=parent_id, tree=tree, counter_byref=counter_byref, verbose=verbose,listsNodeSymbol=listsNodeSymbol, compact_single_dict=compact_single_dict)
    else: #node
        create_node(tree, str(o), counter_byref, verbose, parent_id=parent_id)
    return tree


