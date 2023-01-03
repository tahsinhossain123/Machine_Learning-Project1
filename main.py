# -*- coding: utf-8 -*-
"""main.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Sza7xSQ5X3YYaNXyZhv8NQM5qYSQDHio

Filling up the columns of the data frame
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import nltk

from google.colab import files
uploaded = files.upload()
import io
df = pd.read_csv(io.BytesIO(uploaded['Entity_Type_Detector_Data_Set.csv']))

from google.colab import files
uploaded = files.upload()
import io
df = pd.read_csv(io.BytesIO(uploaded['Break_Through_Tech___Entity_Type_Detector_Data_Set.csv']))

"""## Add languages column based on alphabet detect"""

import subprocess
import sys

def ad_col():
  subprocess.check_call([sys.executable, "-m", "pip", "install", "alphabet-detector"])
  from alphabet_detector import AlphabetDetector
  ad = AlphabetDetector()
  df['langs_ad'] = df['Entity Name'].apply(lambda x: [ad.detect_alphabet(x)])
  df['langs_ad'] = df['langs_ad'].str[0]
  df['langs_ad'] = [list(e) for e in df.langs_ad]
  df['langs_ad'] = df['langs_ad'].str[0]

"""## contains number feature
Identifying if an Entity Name Contains a Number

Inputs: Entity Name as type string
Outputs


*   1 if there is a number in the name 
*   0 if there are no numbers in the name 


"""

import unicodedata

def contains_number(x):
  values=[]

  string = [*x]

  for i in range(len(string)):
    if unicodedata.digit(string[i],-1) == -1:
        values.append(False)
    elif unicodedata.digit(string[i],-1) != -1:
        values.append(True)
        
  if True in values:
    return 1
  else:
    return 0

"""## length of entity feature
Creates new column in the dataframe with length (in charichters or words depending on the language) of that row's entity
"""

def char_split(entity):
  import re
  res = re.sub(r'[^\w\s]', '', entity)
  #how to split string into indvidual chars
  return len(res)

def space_split(entity):
  import re
  if entity[-1] == '.':
    entity = entity[:-1]
  e_list = re.split(",|\.|\-|\s",entity)
  if '' in e_list:
    e_list.remove('')
  if '-' in e_list:
    e_list.remove('-')
  return len(e_list)

def entity_length():
  wc = []
  for i in df.index:
    if df['langs_ad'][i] == 'LATIN' or df['langs_ad'][i] == 'ARABIC' or df['langs_ad'][i] == 'CYRILLIC' or df['langs_ad'][i] ==  'GREEK' or df['langs_ad'][i] == 'HEBREW' or df['langs_ad'][i] == 'DEVANAGARI' or df['langs_ad'][i] == 'ARMENIAN' or df['langs_ad'][i] == 'GEORGIAN'or df['langs_ad'][i] == 'LAO' or df['langs_ad'][i] == 'SINHALA' or df['langs_ad'][i] == 'THAI':
      wc.append(space_split(df['Entity Name'][i]))
    else:
      wc.append(char_split(df['Entity Name'][i]))
  return wc

"""

```
# This is formatted as code
```

## contains company suffix and prefix feature

Identifying if an Entity Name Contains a Company Suffix/Prefix

Inputs: Entity Name as type string Outputs

- 1 if there is a company suffix/prefix in the name
- 0 if there are no legal identifers in the name"""

pip install cleanco

import cleanco
from cleanco import basename

def contain_co(x):
  list3 = ["Inc.","Co.","Corp.","Ltd.","Incorporated","Company","Corporation","Limited","Group","Co.,","Ltd","LLC",
        "有限责任公司","股份有限公司","个人独资企业","合伙制企业","無限公司","有限公司","兩合公司","股份有限公司",
         "株式会社","合同会社","有限会社","合名会社","合資会社","任意組合","匿名組合","投資事業有限責任組合","有限責任事業組合",
         "주식회사","유한회사","유한책임회사","합자회사","합명회사","株式會社","有限會社","有限責任會社","合資會社","合名會社",
         "Кооператив","Некоммерческая организация","Индивидуальный предприниматель","предприятие","Общество","Ответственностью","Непубличное","Публичное","Акционерное",
         "PLC","شركة تضامن","شركات توصية بسيطة","LLP","חברה","שותפות","אגודה שיתופית","עמותה","Bhd.","Sdn.","BHD.","SDN.",
         "บริษัทมหาชนจำกัด","บริษัท","จำกัด","บริษัทเอกชนจำกัด","ห้างหุ้นส่วนจำกัด","ห้างหุ้นส่วน","ห้างหุ้นส่วนสามัญนิติบุคคล","Εταιρεία", "Cooperativa", "Society", "Charity", "Pharmaceutical's",
         "Pharmaceutical", "Pública", "Companhia", "Hospital", "Campo", "Warehouse" "Services", "Service", "服务", "Consumer", "Healthcare", "Económico", "Comercial"
         "Health", "Investment", "Development", "Capital", "Management"]

  value = basename(x)
  value1 = any(substring in x for substring in list3)
  if (x != value or value1):
    return 1
  else:
    return 0



"""## common names feature"""

list1 = ["Michael", "Ali", "David", "Mohamed", "John", "Mohammed", "Ahmed","Abdul", "Thomas", "Juan", "James","Joseph","Carlos",
         "Abdullah", "Antonio", "Robert", "Richard", "Peter", "王", "李", "张", "刘", "陈",
         "杨", "黄", "赵", "مُ", "Emma", "Maria", "Nushi", "Jose", "Wei", "Yan", "Li" , "Smith", 
         "Ana", "Ying", "Juan", "Anna","Mary" "Jean", "Robert", "Daniel" , "Luis", 
         "Carlos", "James", "Antonio", "Joseph", "Hui", "Elena", "Francisco","Hong"
         "Marie", "Min ", "Lei" ,"Yu","Ibrahim", "Peter", "Fatima", "Aleksandr", 
         "Richard", "Xin", "Ping","Paul", "Lin ", "Olga", "Sri", "Pedro", "William", "Rosa", "Thomas", 
         "Jorge", "Yong", "Elizabeth", "Sergey", "Ram", "Patricia", "Hassan", "Anita","Manuel","Victor", "Sandra",
         "Ming", "沐宸", "浩宇", "沐辰", "茗泽", "奕辰", "宇泽", "浩然", "奕泽","宇轩", "沐阳", 
         "若汐", "一诺", "艺涵","依诺", "梓涵", "苡沫", "雨桐", "欣怡", "语桐", "语汐" ,"Hossain","佐藤", "鈴木","高橋"
         "田中", "渡辺", "伊藤","中村", "小林", "山本", "加藤" , "吉田", "山田", "山口","松本", "	井上", "木村", "清水", "林",
         "斉藤", "斎藤", "山崎", "中島", "森"	, "阿部", "池田", "橋本", "石川", "	山下", "小川", "石井", "後藤", "岡田",
         "Smith", "Johnson", "Williams", "Brown", "Jones", "Miller","Davis", "Garcia" , "Rodriguez"
        "Wilson", "Martinez", "Anderson", "Taylor","Thomas", "Hernandez", "Moore", "Martin", "Jackson", "Thompson", "Lopez", "Lee", "Gonzalez", 
        "Harris", "Lewis", "Robinson", "Perez", "José", "María", "Marry", "Lucía", "Sofía", "Martina"
        "Paula", "Lucas", "Hugo", "Martín", "Daniel", "Pablo", "ария","Маша" , "Анна", "Аня", "Виктория", "Вика", "Ольга" ,"Оля", 
         "Наталья", "Наташа", "Татьяна" "Таня","Иван" "Ваня", "Дмитрий" "Дима", "Пётр","Владимир" ,"Николай", "Коля", "Антон", "Андрей", 
         "Krishna", "Shiva", "Narayan", "Piyush", "Vishwajeet", "Arjuna", "Hariom", "Karan", "Pavan", "Aditya", "Vihaan", "Pranav", "Rithvik", "Aarush",
         "حسن", "مُحَمَّد", "بن", "محمد", "خالد", "عبدالله","أحمد", "فهد","سلمان", "سعود	" ,"Mr", "Jr", "Mrs","Esq","Phd", "先生", 'Ali','Ali','John','David','Li','Abdul','Ana','Ying','Michael',
         'Juan','Anna','Mary','Jean','Robert','Daniel','Luis','Carlos','James','Antonio','Joseph']

from google.colab import files
uploaded = files.upload()
import io
df4 = pd.read_csv(io.BytesIO(uploaded['names.csv']))

df_names=df4["Forename"]
name_list = df_names.tolist()
#conmine the 2 lists 
final_name_list=list1+name_list

def common_names(x):
  1 if any(substring in x for substring in final_name_list) else 0

#test feature 
#df['has_common_person_name'] = df['Entity Name'].apply(lambda x:  common_names(x))

"""## comma presant feature"""

def comma_present(Entity):
  if ',' in Entity:
    return True
  else:
    return False

"""## other puncuation"""

import sys
from unicodedata import category
def create_punc_list(): 
  punctuation_chars =  [
      chr(i) for i in range(sys.maxunicode)
      if category(chr(i)).startswith("P")
      ]
  new_punc_chars = ''.join(punctuation_chars).replace(',', '')
  return new_punc_chars
npc = create_punc_list()
def other_punc_new(Entity):
  for p in npc:
    if p in Entity:
      return True
  return False

"""### **Location Feature**"""

from google.colab import files
uploaded = files.upload()
import io
df5 = pd.read_csv(io.BytesIO(uploaded['main_city.csv']))

df_city2=df5["city_ascii"]
city_list2 = df_city2.tolist()

def location_names(x):
  1 if any(substring in x for substring in city_list2) else 0

#Test feature 
#df['has_city_list2'] = df['Entity Name'].apply(lambda x:  location_names(x))

#df['langs_ad'] = df['Entity Name'].apply(lambda x: [ad.detect_alphabet(x)])
ad_col()
df['has_co'] = df['Entity Name'].apply(lambda x:  contain_co(x))
df['has_digit_num'] = df['Entity Name'].apply(lambda x:  contains_number(x))
df['has_common_person_name'] = df['Entity Name'].apply(lambda x:  common_names(x))
df['has_city_list2'] = df['Entity Name'].apply(lambda x:  location_names(x))
df['comma'] = df['Entity Name'].apply(lambda x: comma_present(x))
df['other_punc'] = df['Entity Name'].apply(lambda x : other_punc_new(x))
df['word_count'] = entity_length()
df['conj_pres'] = df['Entity Name'].apply(lambda x: find_conjunction(x))

df.head()

df_final = df

from google.colab import files
df.to_csv('df_final.csv', encoding = 'utf-8-sig') 
files.download('df_final.csv')

from sklearn import preprocessing
le=preprocessing.LabelEncoder()
df['encoded_langs']=le.fit_transform(df['langs_ad']).astype('str')

df.sample()

df.drop('langs_ad',axis = 1, inplace= True)

df.sample(10)

import pickle

with open("df.pkl","wb") as handle:
    pickle.dump(df,handle)
    
with open("df.pkl","rb") as handle:
    dff = pickle.load(handle)

dff.head()

dff.to_csv(r'C:\Users\angel\OneDrive\Desktop\dff.csv', index=False)

# Ange Decision Tree Classifier 

# Import the trees from sklearn
from sklearn import tree

# Helper function to split our data
from sklearn.model_selection import train_test_split

# Helper fuctions to evaluate our model.
from sklearn.metrics import accuracy_score

# Helper function for hyper-parameter turning.
from sklearn.model_selection import GridSearchCV

# Import our Decision Tree
from sklearn.tree import DecisionTreeClassifier 

selected_features = ['has_co', 'has_digit_num',  
                     'has_city_list2', 'comma', 'other_punc',  
                     'word_count']


X = df[selected_features]

y = df['Entity Type']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=45)

print('Length of our Training data:', X_train.shape, '\nLength of our Testing data:', y_test.shape)

model = DecisionTreeClassifier(max_depth=5)

model.fit(X_train,y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_true=y_test, y_pred=y_pred)
print("Accuracy Score: %f" % accuracy)

"""http://hyperopt.github.io/hyperopt/

## conjunction/stopwords feature
"""

import subprocess
import sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "advertools"])
import advertools as adv

def space_split(entity):
  import re
  if entity[-1] == '.':
    entity = entity[:-1]
  e_list = re.split(",|\.|\-|\s",entity)
  if '' in e_list:
    e_list.remove('')
  if '-' in e_list:
    e_list.remove('-')
  return len(e_list)

import subprocess
import sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "advertools"])
import advertools as adv

eng_words = ['and', 'And', 'of', 'for', 'the', 'or', '&', 'with', 'both', 'it', ' y ', 'that', 'by', 'as', 'des', 'de','el', 'et', 'e', 'а также', ]
lang_words = [sorted(adv.stopwords['arabic']), (sorted(adv.stopwords['bengali'])), (sorted(adv.stopwords['catalan'])), (sorted(adv.stopwords['chinese'])), (sorted(adv.stopwords['croatian'])), (sorted(adv.stopwords['danish'])), (sorted(adv.stopwords['dutch'])), (sorted(adv.stopwords['finnish'])), (sorted(adv.stopwords['french'])), (sorted(adv.stopwords['german'])), (sorted(adv.stopwords['greek'])), (sorted(adv.stopwords['hebrew'])), (sorted(adv.stopwords['hindi'])), (sorted(adv.stopwords['hungarian'])), (sorted(adv.stopwords['indonesian'])), (sorted(adv.stopwords['irish'])), (sorted(adv.stopwords['italian'])), (sorted(adv.stopwords['japanese'])), (sorted(adv.stopwords['kazakh'])), (sorted(adv.stopwords['nepali'])), (sorted(adv.stopwords['norwegian'])), (sorted(adv.stopwords['persian'])), (sorted(adv.stopwords['polish'])), (sorted(adv.stopwords['portuguese'])), (sorted(adv.stopwords['romanian'])), (sorted(adv.stopwords['russian'])), (sorted(adv.stopwords['swedish'])), (sorted(adv.stopwords['tagalog'])), (sorted(adv.stopwords['tamil'])), (sorted(adv.stopwords['tatar'])), (sorted(adv.stopwords['telugu'])), (sorted(adv.stopwords['thai'])), (sorted(adv.stopwords['turkish'])), (sorted(adv.stopwords['ukrainian'])), (sorted(adv.stopwords['urdu'])), (sorted(adv.stopwords['vietnamese'])), (sorted(adv.stopwords['spanish']))]
conj_words = eng_words + lang_words

def find_conjunction(Entity):
  for words in Entity.split():
    if words in conj_words:
       return 1
  return 0

#df['conj_pres'] = df['Entity Name'].apply(lambda x: find_conjunction(x))