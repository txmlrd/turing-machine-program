import string
import sys

class Turing_Machine:
    def __init__(self,state,write_head,tape_list):
        """
        Initialize the Turing machine with its state, write head position, and tape list.

        Parameters:
        - state: Initial state of the Turing machine.
        - write_head: Initial position of the write head on the tape.
        - tape_list: List representing the tape of the Turing machine.

        """
        self.state = state
        self.write_head = write_head
        self.tape_list = tape_list

    def getState(self):
        """
        Get the current state of the Turing machine.

        Returns:
        - Current state of the Turing machine.

        """
        return self.state

    def getHead(self):
        """
        Get the current position of the write head on the tape.

        Returns:
        - Current position of the write head.

        """
        return self.write_head
    
    def getList(self):
        """
        Get the current tape list of the Turing machine.

        Returns:
        - List representing the tape of the Turing machine.

        """
        return self.tape_list

    # Table of rules!
    def updateMachine(self, character_list):
        """
        Update the Turing machine according to its current state and the character list. dan mengikuti table rules

        Parameters:
        - character_list: List of characters that can appear on the tape.

        """
        # Initial State
        if (self.state == 'q1'):
            if (self.tape_list[self.write_head] != 0):
                # Move to state pN where N is the index of the character in character_list
                char_read = self.tape_list[self.write_head]
                char_index = character_list.index(char_read)
                self.state = ''.join(['p',str(char_index)])
                # Write 0 to the current tape position
                self.tape_list[self.write_head] = 0
                 # Move the write head to the right
                self.write_head += 1
            else:
                # Reach acceptance state qy (string is empty or all characters processed)
                self.state = 'qy'
                # Write 0 (unchanged)
                self.tape_list[self.write_head] = 0
                # Move the write head to the right
                self.write_head += 1
    
        elif (self.state.startswith('p')):
            if (self.tape_list[self.write_head]!=0):
                # Stay in the same state and leave the character unchanged
                self.state = self.state
                ### WRITE ### (unchanged)
                self.tape_list[self.write_head] = self.tape_list[self.write_head]
                # Move the write head to the right
                self.write_head += 1
            else:
                # Move to state rN where N is the index from state pN
                self.state = ''.join(['r',self.state[1:]])
                # Write 0 to the current tape position
                self.tape_list[self.write_head] = 0
                 # Move the write head to the left
                self.write_head -= 1
                    
        elif (self.state.startswith('r')):
            char_read = character_list[int(self.state[1:])]
            if (self.tape_list[self.write_head] != char_read and self.tape_list[self.write_head] != 0): # zero is needed for strings of odd length
                # Move to state qn if characters do not match
                self.state = 'qn'
                # Leave the tape unchanged
                self.tape_list[self.write_head] = self.tape_list[self.write_head]
                # Move the write head to the left
                self.write_head -= 1
            else:
                # Move to state q2 if characters match or if 0 is encountered (string of odd length)
                self.state = 'q2'
                # Write 0 to the current tape position
                self.tape_list[self.write_head] = 0
                 # Move the write head to the left
                self.write_head -= 1
                
        elif (self.state == 'q2'):
            if (self.tape_list[self.write_head] != 0):
               # Stay in state q2 and leave the tape unchanged
                self.state = 'q2'
                ### WRITE ### (unchanged)
                self.tape_list[self.write_head] = self.tape_list[self.write_head]
               # Move the write head to the left
                self.write_head -= 1
            else:
                # Move back to state q1 to continue checking the remaining part of the string
                self.state = 'q1'
                # Write 0 to the current tape position
                self.tape_list[self.write_head] = 0
                # Move the write head to the right
                self.write_head += 1


def check_palindrome(initial_string):
    """
    Check if a given string is a palindrome using a Turing machine.

    Parameters:
    - initial_string: The string to be checked for palindrome.

    """
    # Define Character Set (allowed characters for the palindrome)
    character_list = list(string.ascii_lowercase + string.digits)
    character_list.append(' ') # to allow for spaces

    # Initial string
    print('Checking: ' + initial_string)
    print('- - -')
    initial_list = list(initial_string)

    # Quick check that you only used allow characters
    for i in initial_list:
        if i not in character_list:
            print('Error! Initial character >',i,'< not in allowed character list!')
            sys.exit()

    # Append list
    initial_list.append(0)

    # Set up the turing machine
    i_write_head = 0
    i_state = 'q1' # initial state
    i_tape_list = initial_list

    # Initiate the class
    runMachine = Turing_Machine(i_state,i_write_head,i_tape_list)
    # runMachine.getState(),runMachine.getHead(),runMachine.getList()
    print(runMachine.getState(),runMachine.getHead(),runMachine.getList())

    # Run the machine
    ctr=0
    while runMachine.getState() != 'qy' and runMachine.getState() != 'qn' and ctr < 1000:
        runMachine.updateMachine(character_list)
        # runMachine.getState(),runMachine.getHead(),runMachine.getList()
        print(runMachine.getState(),runMachine.getHead(),runMachine.getList())
        ctr += 1
    print('- - -')


    # Printout result
    if (runMachine.getState() == 'qy'):
        print(initial_string, 'is a palindrome!')
    else:
        print(initial_string, 'NOT a palindrome!')


test_cases = ['tenet', 'racecar', 'hello', 'w0rld', 'aa22aa', 'a010a', '1', 'ab0']

for test in test_cases:
    check_palindrome(test)