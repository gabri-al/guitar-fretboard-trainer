# Create custom classes: Note, GuitarString
class Note:
    
    def __init__(self, Value, isAccidental):
        self.value = Value
        self.accidental = isAccidental
        
    def getValue(self):
        return self.value
        
    def isAccidental(self):
        return self.accidental
    
# List with all notes (since C# = Db, they will be the same note)
NOTES_ = [
    Note(["A"], False),
    Note(["A#", "Bb"], True),
    Note(["B"], False),
    Note(["C"], False),
    Note(["C#", "Db"], True),
    Note(["D"], False),
    Note(["D#", "Eb"], True),
    Note(["E"], False),
    Note(["F"], False),
    Note(["F#", "Gb"], True),
    Note(["G"], False),
    Note(["G#", "Ab"], True)]

## Create a class GuitarString. A string has a 0-fret note and it is composed by 24 frets by default
class GuitarString:
    
    def __init__(self, note, numFrets = 24): # note must be a Note class object
        self.OpenNote = note
        self.nFrets = numFrets
        self.StringNotes = self.__setFrets__() # Assign notes to frets
    
    def __setFrets__(self):
        # Init iOpen by looking for the open note in the sequence
        for i in range(0, len(NOTES_)):
            if self.OpenNote.getValue()[0] in NOTES_[i].getValue():
                iOpen = i
                break
        # Assign notes to frets
        StringNotes_ = {} # Dict of Notes class objects
        iNew = iOpen
        for j in range(0, self.nFrets+1):
            StringNotes_[j] = NOTES_[iNew]
            iNew += 1
            if iNew == len(NOTES_):
                iNew = 0
        return StringNotes_
        #print("Notes on the %2s string calculated:\n%s\n" % (self.OpenNote, StringNotes_))
        
    def getOpenNote(self):
        return self.OpenNote.getValue()
    
    def getNumFrets(self):
        return self.nFrets
    
    def getNote(self, fret):
        '''Return the Note class in a fret position'''
        try:
            return self.StringNotes[fret]
        except:
            print("Invalid fret number on String.getNote()")
    
    def guessNote(self, fret, guessedValue):
        '''Return True or False depending if the guessed note is at fret position'''
        # Make sure the guessed note is capital
        if len(guessedValue) > 1:
            guessedValue = guessedValue[:1].upper() + guessedValue[-1]
        elif len(guessedValue) == 1:
            guessedValue = guessedValue.upper()
        try:
            if guessedValue in self.getNote(fret).getValue():
                return True
            else:
                return False
        except:
            print("Invalid input on String.guessNote()")