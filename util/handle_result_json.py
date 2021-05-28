import json
import os
from deepdiff import DeepDiff

def handle_result_json(dict1,dict2):
    """
    比较2个字典结构是否一致
    """
    if isinstance(dict1,dict) and isinstance(dict2,dict):
        cmp_dict=DeepDiff(dict1,dict2,ignore_order=True).to_dict()
        print(cmp_dict)
        if cmp_dict.get('dictionary_item_added') or cmp_dict.get('dictionary_item_removed'):
            return False
        else:
            return True
    return False

if __name__ == '__main__':

    dict1={"aaa":"AAA","bbb":"BBBB","CC":[{"11":"22"},{"11":"44"}]}
    dict2={"aaa":"123","bbb":"456","CC":[{"11":"111"},{"11":"44"}]}
    dict3="456"
    print(handle_result_json(dict1,dict3))