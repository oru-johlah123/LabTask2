import operator

#Class Person, general class for a person with it's constraints in form of strings.
class Person:
    name = ""
    status = ""
    smoker = ""
    manyVisitors = ""
    potentialRoomKey = list()

    def __init__(self,name,status,smoker,manyVisitors):
        self.name = name
        self.status = status
        self.smoker = smoker
        self.manyVisitors = manyVisitors

#Class Room, class for a room with a size of how many can be in that room.
class Rooms:
    amount = 0
    currentAmount = 0
    contains = []
    roomKey = ""

    def __init__(self,amount,roomKey):
        self.contains = []
        self.amount = amount
        self.roomKey = roomKey

#Class Office, hold the list of people and officerooms, reads in people and rooms.
class Office:
    persons = list()
    unAssignedPeople = list()
    originalPeopleList = list()
    officeRooms = dict()
    def __init__(self):
        self.officeRooms['T13'] = Rooms(1,'T13')
        self.officeRooms['T14'] = Rooms(1,'T14')
        self.officeRooms['T15'] = Rooms(1,'T15')
        self.officeRooms['T16'] = Rooms(1,'T16')
        self.officeRooms['T11'] = Rooms(2,'T11')
        self.officeRooms['T12'] = Rooms(2,'T12')
        self.officeRooms['T10'] = Rooms(3,'T10')
        self.officeRooms['T17'] = Rooms(3,'T17')
        self.officeRooms['T18'] = Rooms(3,'T18')
        self.setPeople()

    def setPeople(self):
        self.persons.append(Person("E","researcher","smoker","many visitors"))
        self.persons.append(Person("F","researcher","non-smoker","few visitors"))
        self.persons.append(Person("G","researcher","non-smoker","few visitors"))
        self.persons.append(Person("H","PhD Student","non-smoker","many visitors"))
        self.persons.append(Person("I","PhD Student","smoker","few visitors"))
        self.persons.append(Person("J","PhD Student","smoker","few visitors"))
        self.persons.append(Person("K","PhD Student","non-smoker","few visitors"))
        self.persons.append(Person("B","professor","non-smoker","many visitors"))
        self.persons.append(Person("D","professor","smoker","many visitors"))
        self.persons.append(Person("A","head","non-smoker","many visitors"))
        self.persons.append(Person("C","professor","non-smoker","few visitors"))
        self.originalPeopleList = list(self.persons)
        self.unAssignedPeople = list(self.persons)

    def refresh(self):
        self.persons = list(self.originalPeopleList)
        self.unAssignedPeople = list(self.originalPeopleList)

#Class Constraints, has the office object in it and all the constraint functions that must be followed. 
class Constraints:

    office = Office()

    def refresh(self):
        self.office.refresh()

    def checkConstraints(self,one,room):
        if not self.FullRoom(room):
            return False
        if not self.Smoker(one,room):
            return False
        if not self.Visitors(one,room):
            return False
        if not self.CheckStatus(one,room):
           return False
        return True

    def Smoker(self,one,room):
        for another in room.contains:
            if one.smoker != another.smoker:
                return False
        return True
         
    def Visitors(self,one,room):
        for another in room.contains:
            if one.manyVisitors == "many visitors" and another.manyVisitors == "many visitors":
                return False
        return True

    def FullRoom(self,room):
        if room.currentAmount == room.amount:
            return False
        for another in room.contains:
            if another.status == "head" or another.status == "professor":
                return False
        else:
            return True

    def CheckStatus(self,one,room):
        if one.status == "head" or one.status == "professor":
            if room.contains == []:
                if room.amount == 2 or room.amount == 3:
                    return True
                else:
                    return False
        else:
            return True
#The first backtracking search that will call the recursive function that is not using any heuristics, returns either an assignment list or a "None" value
def BackTrackingSearch(csp):
    assignment = dict()
    return ReckursiveBacktracking(assignment,csp)

#Recursive backtracking search, tries to assign all the people in to the rooms following all the constraints from the constraints class
def ReckursiveBacktracking(assignment,csp):
    if csp.office.persons == []:
        return assignment
    person = csp.office.persons.pop()
    for room in roomList(person,assignment,csp):
        assign(person,room,assignment,csp)
        global count
        count = count + 1
        result = ReckursiveBacktracking(assignment,csp)
        if result != None:
            return result
        unAssign(person,room,assignment,csp)
    csp.office.persons.insert(0,person)
    if len(csp.office.persons) < len(csp.office.unAssignedPeople):
        csp.office.unAssignedPeople = list()
        for p in csp.office.persons:
            csp.office.unAssignedPeople.append(p)
    return None

#Function that returns a list of rooms a given person can be in following the constraints given by the constraints class
def roomList(person,assignment,csp):
    returnKeys = list()
    for room in csp.office.officeRooms.keys():
        if csp.checkConstraints(person,csp.office.officeRooms[room]):
            returnKeys.append(room)
    return returnKeys

#Function assigns a person to the assignment list.
def assign(person,room,assignment,csp):
    personToAppend = csp.office.officeRooms[room]
    personToAppend.contains.append(person)
    personToAppend.currentAmount += 1
    assignment[person] = room 

#Function un assignes a person from the assignment list
def unAssign(person,room,assignment,csp):
    roomToDeletePersonFrom = assignment[person]
    csp.office.officeRooms[roomToDeletePersonFrom].contains.remove(person)
    csp.office.officeRooms[roomToDeletePersonFrom].currentAmount -= 1
    del assignment[person]

#Function that returns the leas constrainging value in form of a room that will be the least constraining for the other un assigned people
def LeastConstrainingVal(person,csp,assignment):
    testAssignment = dict(assignment)
    testCsp = csp
    bestRoom = 0
    if person.potentialRoomKey == []:
        return None
    elif csp.office.persons == []:
        return person.potentialRoomKey.pop()
    for roomKey in person.potentialRoomKey:
        possibleRoomCount = 0
        assign(person,roomKey,testAssignment,testCsp)
        for affectedPerson in testCsp.office.persons:
            tempRoomKeys = roomList(affectedPerson,testAssignment,testCsp)
            possibleRoomCount += len(tempRoomKeys)
        if possibleRoomCount > bestRoom:
            bestRoom = possibleRoomCount
            roomToReturn = roomKey
        unAssign(person,roomKey,testAssignment,testCsp)   
    if bestRoom == 0:
        return None
    person.potentialRoomKey.remove(roomToReturn)
    return roomToReturn

#Function returns the person that is the most constrained of all current people in the people list
def MostConstrainedVariable(csp):
    count = 1000
    findPotential(csp)
    for person in csp.office.persons:
        if len(person.potentialRoomKey) < count:
            count = len(person.potentialRoomKey)
            personToReturn = person
    csp.office.persons.remove(personToReturn)
    return personToReturn

#Function sets what rooms people in the people list can be in, following the constraints
def findPotential(csp):
    for p in csp.office.persons:
        p.potentialRoomKey = list(roomList(p,{},csp))

#Backtracking search with heuristic, calls the recursive function that uses the heuristics, returns an assignment or a "None" value.
def BacktrackingWithH(csp):
    assignment = dict()
    return ReckursiveBacktrackingWithH(assignment,csp)

#Recursive backtracking that uses heuristics.
def ReckursiveBacktrackingWithH(assignment,csp):
    if csp.office.persons == []:
        return assignment
    person = MostConstrainedVariable(csp)
    room = LeastConstrainingVal(person,csp,assignment)
    while room != None:
        assign(person,room,assignment,csp)
        global count
        count = count + 1
        result = ReckursiveBacktrackingWithH(assignment,csp)
        if result != None:
            return result
        unAssign(person,room,assignment,csp)
        room = LeastConstrainingVal(person,csp,assignment)
    csp.office.persons.insert(0,person)
    return None
#Main program
csp = Constraints()
count = 0 
assignments = BackTrackingSearch(csp)

if assignments != None:
    for a in assignments.keys():
        print("Person:",a.name,"constraints:",a.status,a.smoker,a.manyVisitors,"room:",assignments[a])
    del a
    assignments.clear()
else:
    print("Couldn't assign everybody")
    print("People that couldn't be assigned a room:")
    for person in csp.office.unAssignedPeople:
        print(person.name,person.status,person.smoker,person.manyVisitors)
print("It took",count,"recursions in order for the assignment to finish")

dummy = input("Press enter to do the assignment with heuristic search!\n")
count = 0

for room in csp.office.officeRooms.values():
    room.contains.clear()
    room.currentAmount = 0

csp.refresh()
assignments = BacktrackingWithH(csp)
print('Heuristic backtracking:')
if assignments != None:
    for a in assignments.keys():
        print("Person:",a.name,"constraints:",a.status,a.smoker,a.manyVisitors,"room:",assignments[a])
    assignments.clear()
else:
    print("Couldn't assign everybody!")
print("It took",count,"recursions in order for the assignment to finish")

  
