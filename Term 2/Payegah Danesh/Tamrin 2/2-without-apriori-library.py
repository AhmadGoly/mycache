import pandas as pd
import itertools
class Arules:
  def __init__(self):
    ...
  def get_frequent_item_sets(self,transactions,min_support,min_confidence):
      print(f"get_frequent_item_sets Running for Min Support {min_support}")
      totalrows=transactions.shape[0]
      min_support_int=totalrows*min_support
      print(f"Running for K=1")
      #for start, we calculate the C1 and L1:
      final_list=[]
      #C1
      for i in range(0,transactions.shape[1]):
          count=0.0
          col_name=transactions.columns[i]
          for j in range(0,transactions.shape[0]):
              if transactions.loc[j, col_name] != 0:
                  count+=1
          #L1
          if (count)>min_support_int:
              final_list.append([[col_name],count])
      #lets do the K(N)
      last_list=final_list.copy()
      k=2
      while(True):
          print(f"--------------------------------\nRunning for k={k}")
          cachelist=Arules().KN(transactions,last_list,k,min_support_int)
          print(f"\nk({k}) frequent_item_sets size is {len(cachelist)}. passing it to k={(k+1)} (if it's not empty).")
          if cachelist==[]:
              break
          else:
              for i in range(0,len(cachelist)):
                  final_list.append(cachelist[i])
              last_list=cachelist.copy()
              k=k+1
      return final_list

  def get_arules(self,transactions,min_support=0,min_confidence=0,min_lift=0,sort_by='lift',FrequentItemsets=None):
    print(f"get_arules Running for Min_sup={min_support} Min_Conf={min_confidence} and Min_Lift={min_lift}. Sort_by={sort_by}.")
    totalrowsnumber=len(transactions)
    Rules = []
    i=0
    # sort_by: lift , confidence, support
    if sort_by not in ['lift', 'confidence', 'support']:
      raise ValueError("Invalid parameter for sort_by. Allowed Strings for sort_by are 'lift', 'confidence', and 'support'.")
    totalrows=transactions.shape[0]
    min_support_int=totalrows*min_support
    if FrequentItemsets==None:
      load_frequent_item_sets=Arules().get_frequent_item_sets(transactions,min_support,min_confidence)
    else:
      load_frequent_item_sets=FrequentItemsets
    for firstitem in load_frequent_item_sets:
      i=i+1
      print(f"\rProcessing get_arules on frequent_item_sets:{i} out of {len(load_frequent_item_sets)}.", end="")
      #tamoome tarkibate momken ba baghie ro ba sharte min_conf peyda kon.
      #hint: firstitem (ya seconditem) yek list ast ke firstitem[0] liste itemha va firstitem[1] supporte on itemha hast. type(firstitem[0])=list and type(firstitem[1])=int
      for seconditem in load_frequent_item_sets:
        if len(seconditem[0])>1:
          continue
        if seconditem[0][0] in firstitem[0]:
          continue
        #find conf:
        cols=firstitem[0]+seconditem[0]
        #print(type(cols))
        #print(transactions.columns)
        new_df = transactions.loc[:, cols]
        rows_with_firstitemset_df=new_df[(new_df[firstitem[0]] != 0).all(axis=1)]
        rows_with_firstitemset_and_2nditemset_count = rows_with_firstitemset_df[rows_with_firstitemset_df[seconditem[0][0]] != 0].shape[0]
        conf = float(rows_with_firstitemset_and_2nditemset_count/(len(rows_with_firstitemset_df)))
        if conf<min_confidence:
          continue
        #in tarkib khoobe. lift ro hesab kon va in rule ro too Rules[] zakhire kon.
        support=Arules().calculateSupportOfC(cols,transactions)
        if support<min_support_int:
          continue
        #Lift = support/(firstitem[1]*seconditem[1]). vali inja bayad hame support ha taghsim bar tedad kole row ha dar transaction shavand.
        lift = (support/(firstitem[1]*seconditem[1]) )*totalrowsnumber
        if lift<min_lift:
          continue
        Rules.append([firstitem[0],seconditem[0],firstitem[1],seconditem[1],support,conf,lift])
        #each rule has 7 parameters: [list1,list2,support1,support2,supportboth,conf,lift]
    rows = []
    for l1, l2, s1, s2, sb, c, l in Rules:
      row = {"antecedent": l1, "outcome": l2, "support_antecedent": s1, "support_outcome": s2, "support": sb, "confidence": c, "lift": l}
      rows.append(row)
    FinalDF = pd.DataFrame(rows)
    FinalDF_sorted = FinalDF.sort_values(by=sort_by, ascending=False)
    return FinalDF_sorted

  def KN(self,transactions,last_list,k,min_support_int):
      #C(n)
      print(f"Calculating k({k}) from k({(k-1)}). k({(k-1)}) size is {len(last_list)}")
      new_list=[]
      for l1 in range(0,len(last_list)-1):
          print(f"\rProcessing Last_list {(l1+2)} out of {len(last_list)}", end="")
          for l2 in range (l1+1,len(last_list)):
              #comparing this 2 list to merge if possible.
              first_list_cols=last_list[l1][0]
              sec_list_cols=last_list[l2][0]
              these2ListsAreUseless=False
              #compare l1 and l2:
              #Test 1: check all products in 2 list expect the last ones.
              for i in range(0,len(first_list_cols)-1):
                  if first_list_cols[i]!=sec_list_cols[i]:
                      these2ListsAreUseless=True
                      break
              #Test 2: test the last ones: L2's last product should be bigger.
              if not these2ListsAreUseless:
                  if not transactions.columns.get_loc(first_list_cols[len(first_list_cols)-1]) < transactions.columns.get_loc(sec_list_cols[len(sec_list_cols)-1]):
                      #these 2 are not good to merge
                      these2ListsAreUseless=True
              #Test 3:has_infrequent_subsets?
              c = []
              for i in range(0,len(first_list_cols)):
                  c.append(first_list_cols[i])
              c.append(sec_list_cols[len(sec_list_cols)-1])
              #check if c is already in new_list (sometimes there is duplicates in new_list and idk why. ik there is a bug but I didnt find bug. so I had to add this.)
              c_is_already_in_new_list=False
              for lst in new_list:
                if lst[0]==c:
                  c_is_already_in_new_list=True
                  break
              if not c_is_already_in_new_list:
                if not Arules().c_has_infrequent_subnet(c,last_list):
                    #add C to new List.
                    new_list.append([c,Arules().calculateSupportOfC(c,transactions)])
      #LN -> remove the noobs based on min_sup
      totalrows=transactions.shape[0]
      final_list=[]
      for sub in new_list:
          if sub[1]>=min_support_int:
              #print(f"{sub} is good")
              final_list.append(sub)
      return final_list

  def calculateSupportOfC(self,c,transactions):
      #print(c)
      new_df = transactions.loc[:,c]
      #count = len(df[(df == 1).all(axis=1)])
      return len(new_df[(new_df != 0).all(axis=1)])

  def c_has_infrequent_subnet(self,c,last_list):
      #all of the subsets must exist in last_list.
      #print(f"Running c_has_infrequent_subnet for {c}")
      #print(last_list)
      subsets = list(itertools.combinations(c, len(c)-1))
      for i in range(0,len(subsets)):
          cache=list(subsets[i])
          sublist_exists = False
          for lst in last_list:
              #print(f"comparing {lst[0]} and {cache}")
              if lst[0] == cache:
                  sublist_exists = True
                  break
          if not sublist_exists:
              return True
      return False
#Soal 3
import csv
Purchases = []
with open('/content/drive/MyDrive/groceries.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        row = [item.strip() for item in row if item.strip()]
        if row:
            Purchases.append(row)
dataset = pd.DataFrame({'Transaction': ['T{}'.format(i) for i in range(1, len(Purchases)+1)],'Items': Purchases})
basket_sets = pd.get_dummies(dataset['Items'].apply(pd.Series).stack()).groupby(level=0).sum()
myFrequentList = Arules().get_frequent_item_sets(basket_sets,0.005,1)
print(f"myFrequentList size is {len(myFrequentList)}")
sorted_list = sorted(myFrequentList, key=lambda x: x[1], reverse=True)
top_10 = sorted_list[:10]
i=1
for item in top_10:
    print(f"{i}:{item[0]} , {item[1]}", )
    i=i+1 #i'm noob in python.

#Soal 4
myRules = Arules().get_arules(basket_sets,0.005,0.2,0,'lift',None)
print(len(myRules))
print(myRules)

#Soal 5a
myRules = Arules().get_arules(basket_sets,0.05,0.3,1,'confidence',None)
print(myRules)

#Soal 5b
myRules = Arules().get_arules(basket_sets,0.03,0.3,1,'confidence',None)
print(myRules)

#Soal 5c
myRules = Arules().get_arules(basket_sets,0.01,0.3,1,'confidence',None)
print(f"Found {len(myRules)} Rules.")
print(myRules)
