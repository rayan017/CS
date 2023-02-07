class CodeBreaker:
    '''
    This is your CodeBreaker class! You will be responsible for filling in the
    logic of this based on the instructions from the handout and TODO comments
    below

    Fields:
    start_word: the word we start with
    end_word: the word we end with
    similarity_array: the intermediate values for comparing each substring of
        start_word and end_word
    '''
    
    def __init__(self, start_word: str, end_word: str):
        '''
        CodeBreaker constructor. Defines variables and initializes the
        similarity array

        You are responsible for initializing self.similarity_array in this
        method
        '''
        # A letter's case does not matter, we use lower() to make input words
        # all lower-case
        self.start_word = start_word.lower()
        self.end_word = end_word.lower()

        # TODO: replace the "None" below with your code to initialize the 2d
        # similarity array
        self.similarity_array = [[0]*(len(self.start_word) + 2) for _ in range(len(self.end_word) + 2)]
        # fill the similarities array
        self.fill_similarities()
        
    def find_score(self) -> int: 
        '''
        TODO: Write your docstring here! 

        Returns: An integer (the smallest difference between self.start_word and
        self.end_word)

        TODO: Fill in this method. This should JUST return the contents of the
        cell that contains your final answer (it should not compute those
        contents)
        '''
        return self.similarity_array[1][1]
        pass

    def fill_similarities(self):
        '''
        Write your docstring here! 

        TODO: Fill in this method to fill in self.similarity array. You should
        expand on your pseudocode from task 1-g in this method. Be sure you're
        looping through the array in the correct order!
        '''
        self.similarity_array[0][len(self.start_word)+1]="-"
        self.similarity_array[len(self.end_word)+1][0]="-"
        for i in range(1,len(self.end_word)+1):
            self.similarity_array[i][0]=self.end_word[i-1]
            self.similarity_array[i][len(self.start_word)+1]=len(self.end_word)+1-i
            for k in range(1,len(self.start_word)+1):
                self.similarity_array[0][k]=self.start_word[k-1]
                self.similarity_array[len(self.end_word)+1][k]=len(self.start_word)+1-k
        for k in range(len(self.start_word),0,-1):
            for i in range(len(self.end_word), 0,-1):
                if self.similarity_array[0][k] == self.similarity_array[i][0]:
                    self.similarity_array[i][k]=self.similarity_array[i+1][k+1]
                else:
                    if i==len(self.end_word):
                        if k==len(self.start_word):
                            self.similarity_array[i][k]=1
                        else:
                            self.similarity_array[i][k]=self.similarity_array[i][k+1]+1
                    else:
                        self.similarity_array[i][k]=min(self.similarity_array[i+1][k], self.similarity_array[i+1][k+1],self.similarity_array[i][k+1])+1
        pass