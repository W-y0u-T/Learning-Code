''' class_list_pickle1.py
create a list of class instances
The class itself cannot be pickled, but the list of instances can.
To use the pickled data file in another program, you have to
recode the class in that program.
tested with Python273 and Python33  by vegaseat  08jan2013
also works with IronPython273
'''
import operator
import pickle
class Person:
    def __init__(self, name=None, sex=None, slogan=None):
        self.name = name
        self.sex = sex
        self.slogan = slogan
# a csv type data string for testing
data_str = '''\
Porke,Emma,female,Vote for Bush and Dick
Schidd,Jack,male,Never give a schidd!
Negerschwarz,Arnold,often,I know how to spell nukilar!
'''
# make a list of class Person instances using the data_str
person_list = []
for line in data_str.split('\n'):
    if line:
        line = line.split(',')
        pname = "%s %s" % (line[1], line[0])
        person_list.append(Person(pname, line[2], line[3]))
# testing ...
print("Show all persons and what they say:")
for person in person_list:
    print("{} says \"{}\"".format(person.name, person.slogan))
print('-'*50)
print("Show one particular item:")
print(person_list[0].name)
print('-'*50)
print("Sort the person_list by name and show ...")
plist_sorted = sorted(person_list, key=operator.attrgetter('name'))
for person in plist_sorted:
    print(person.name)
print('-'*50)
# pickle the list of instances
fname = "person_instance_list.pkl"
# pickle dump the list object
with open(fname, "wb") as fout:
    # default protocol is zero
    # -1 gives highest prototcol and smallest data file size
    pickle.dump(person_list, fout, protocol=-1)
print("Data has been pickled to file {}".format(fname))
# pickle load the list object back in (senses protocol)
with open(fname, "rb") as fin:
    person_list2 = pickle.load(fin)
print("Pickled data has been reloaded ..")
print('-'*50)
# test loaded list of instances
for person in person_list2:
    print("{} says \"{}\"".format(person.name, person.slogan))
''' result ...
Show all persons and what they say:
Emma Porke says "Vote for Bush and Dick"
Jack Schidd says "Never give a schidd!"
Arnold Negerschwarz says "I know how to spell nukilar!"
--------------------------------------------------
Show one particular item:
Emma Porke
--------------------------------------------------
Sort the person_list by name and show ...
Arnold Negerschwarz
Emma Porke
Jack Schidd
--------------------------------------------------
Data has been pickled to file person_instance_list.pkl
Pickled data has been reloaded ..
--------------------------------------------------
Emma Porke says "Vote for Bush and Dick"
Jack Schidd says "Never give a schidd!"
Arnold Negerschwarz says "I know how to spell nukilar!"
'''
