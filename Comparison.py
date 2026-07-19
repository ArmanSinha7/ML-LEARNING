import pandas as pd
import time
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
transactions=[
["Milk","Bread","Butter"],
["Milk","Bread"],
["Bread","Butter"],
["Milk","Butter"],
["Milk","Bread","Butter"],
["Bread","Eggs"],
["Milk","Eggs"],
["Bread","Butter","Eggs"],
["Milk","Bread","Eggs"],
["Milk","Bread","Butter","Eggs"]]
encoder=TransactionEncoder()
encoded=encoder.fit(transactions).transform(transactions)
df=pd.DataFrame(encoded,columns=encoder.columns_)
start=time.perf_counter()
apriori_result=apriori(df,min_support=0.3,use_colnames=True)
apriori_time=time.perf_counter()-start

def eclat(data,min_support):
    item_dict={}
    for index,transaction in enumerate(data):
        for item in transaction:
            if item not in item_dict:
                item_dict[item]=set()
            item_dict[item].add(index)
    total=len(data)
    result=[]
    def build(prefix,items):
        for i in range(len(items)):
            itemset,tids=items[i]
            support=len(tids)/total
            if support>=min_support:
                current=prefix|itemset
                result.append([set(current),round(support,2)])
                next_items=[]
                for j in range(i+1,len(items)):
                    new_itemset,new_tids=items[j]
                    common=tids&new_tids
                    if len(common)/total>=min_support:
                        next_items.append((itemset|new_itemset,common))
                build(current,next_items)
    initial=[(frozenset([item]),tids) for item,tids in item_dict.items()]
    build(frozenset(),initial)
    return result
start=time.perf_counter()
eclat_result=eclat(transactions,0.3)
eclat_time=time.perf_counter()-start
print("\nApriori Frequent Itemsets\n")
print(apriori_result)
print("\nECLAT Frequent Itemsets\n")
for itemset,support in eclat_result:
    print(itemset,"Support:",support)
comparison=pd.DataFrame({
    "Algorithm":["Apriori","ECLAT"],
    "Execution Time (s)":[round(apriori_time,6),round(eclat_time,6)],
    "Frequent Itemsets":[len(apriori_result),len(eclat_result)]
})
print("\nComparison\n")
print(comparison)