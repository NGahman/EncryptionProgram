'''
Asks if you want to encrypt or decrypt a message.
If you encrypt, it shifts each letter by an inputted number (say, 3).
If you decrypt, it does the exact same thing, but the number is negative, so it decrypts the message.
Alternatively, decrypt and encrypt can be reversed, so that decrypt actually encrypts it and encrypt actually decrypts it.
This works for capital letters and numbers as well.
Furthermore, before the above happens, it scrambles all of the letters using a key that can either be pasted in from a previous session or randomly generated,
further encoding the message.
In addition, this project can now mess with the order of the letters,
from playing the message backwards to adding "garbage" letters that don't mean anything to putting the odd letters first,
then the even letters (example: hello world -> hlowrdel orl).
As such, the message can be much more encrypted than before. This program can now save keys to a text file.
If you save the key to a text file, a file called Encryption will appear in your documents folder if it did not exist already, and all of your keys will appear there.
From there, it is up to you to decide how to label the keys so that you know what key to use for each situation.
You can also specify a pathname, and a file will appear with that pathname. Conversionlength is the length of the key.
It can be anything above 1000 length, but the advisable length is between 1000-10000.  The default length is 10000.
NOTE: Any length above 65532 will not work, due the 32 bit integer limit. It now has a backup system, which will recover the key system if conversionlength is too high or low.
It also has the ability to specify the conversionlength on the shell if desired.
Furthermore, it now can grab keys from files, so you can simply paste the key you want in a text file and use it there instead of inputting it.
The program can now not only put garbage letters on the front and back of the key, but in the middle as well.
It takes the amount of letters, divides them by two, and rounds it down, then puts the garbage letters there. Now has a public/private key system.
Three inputs are required, one to activate the system and two more to input prime numbers.
'''
import importlib
secrets = importlib.import_module('secrets')
conversion=""
def RandInt(a,b):
  '''(integer,integer)->integer
  Returns a truly random integer
  (0,5)->3'''
  while True:
    c=secrets.randbelow(b+1)
    if c>=a:
      break
  return c

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m
def lcm(x, y):
   """This function takes two
   integers and returns the L.C.M."""

   # choose the greater number
   if x > y:
       greater = x
   else:
       greater = y

   while(True):
       if((greater % x == 0) and (greater % y == 0)):
           lcm = greater
           break
       greater += 1

   return lcm
def PrimeCheck(num):
  '''(integer)->Boolean
  Checks whether a number is prime or not.
  (24)->False
  '''
  if num > 1:
    for i in range(2,num):
      if (num % i) == 0:
        return False
    return True
  else:
   return False
def RSAKey(prime1,prime2):
  '''(integer,integer)->string
  Uses the RSA cryptosystem to generate a public and private key.
  (61,53)->"The public key is 17, the private key is 413,n is 3233"'''
  n=prime1*prime2
  L=lcm(prime1-1,prime2-1)
  while True:
    e=RandInt(1,L)
    primecheck3=PrimeCheck(e)
    if primecheck3 and L%e!=0:
      break
  d=modinv(e,L)
  return n,e,d
def RSAEncryption(n,EncryptionNumber1,phrase2,alphabet):
  phrase3=""
  padding=""
  for i in phrase2:
    padding+=str(alphabet.index(i))
    padding=(int(padding)**EncryptionNumber1)%n
    phrase3+=str(padding)
    phrase3+="."
    padding=""
  return phrase3
def RSADecryption(n,EncryptionNumber2,phrase2,alphabet,conversionlength):
  phrase=""
  phrase3=""
  for i in phrase2:
    if i!=".":
      phrase+=i
    else:
      phrase=(int(phrase)**EncryptionNumber2)%n
      phrase3+=alphabet[phrase]
      phrase=""
  return phrase3
def KeyCreator(conversionlength):
        alphabet=[]
        for i in range(0,conversionlength+3):
            alphabet.append(chr(i))
        #Deletes enter character, to avoid trouble inputting it during another session.
        del alphabet[10]
        del alphabet[12]
        return alphabet
def caesar(phrase,shift,change):
        '''(string,int,int)->string
        Takes the phrase, and moves the letters forward by shift, and returns the resultinig string.  Change changes the shift by change number each time.
        '''
        newPhrase=""
        for i in phrase:
            if i in alphabet:
                x=alphabet.index(i)
                while True:
                        if x+shift > conversionlength-1:
                          shift-=(conversionlength-1)
                        if x+shift < 0:
                          shift+=(conversionlength-1)
                        newPhrase+=alphabet[x+shift]
                        break
            else:
                newPhrase+=i
            shift+=change
        return newPhrase
def VowelsToNumbers(phrase,Vowels,VowelsAsNums):
        '''(string,string,string)->string
        Takes the phrase, and filters it through the key, then prints the result.
        (hello world, helo wrd, ksrnmdqo)->ksrrnmdnqro
        '''
        vowels=list(Vowels)
        vowelsAsNums=list(VowelsAsNums)
        newPhrase=""
        for i in phrase:
            if i in vowels:
                newPhrase+=vowelsAsNums[vowels.index(i)]
            else:
                newPhrase+=i
        return newPhrase
def ScramblingDecode(phrase3):
        '''(string)->string
        Decodes the string by finding where the odd and even letter meet, then putting the min their proper place.
        (hlowrdel ol)->hello world
        '''
        if int(len(phrase3))//2==int(len(phrase3))/2:
            part=int(len(phrase3))//2
        else:
            part=int(len(phrase3))//2+1
        phrasepart1=phrase3[:part]
        phrasepart2=phrase3[part:]
        phrase3=""
        #Adds the two phrases together
        for i in range(0,int(len(phrasepart1))):
            phrase3+=phrasepart1[i]
            #If the phrase has an even number of characters, adds the last character.  Otherwise, it causes an error and stops.
            try:
                phrase3+=phrasepart2[i]
            except IndexError:
                #Do nothing in the event that an error occurs, as nothing needs to be done
              j="j"
        return phrase3
def ScramblingEncode(phrase2):
        '''(string)->string
        Encodes the word by separating the word into odd and even letters, and putting those odd and even portions together.
        (hello world)->hlowrdel ol
        '''
        phrasepart1=phrase2[::2]
        phrasepart2=phrase2[1::2]
        phrase2=phrasepart1+phrasepart2
        return phrase2
def Garbage(garbage1,garbage2,garbage3,phrasePart1,phrasePart2):
        '''(int,int,string)->string
        Takes the phrase and adds random letters to the beginning, end, and middle of it.  The amount of letters is garbage1 letters for the beginning, garbage2 letters for the end, and garbage3 letters for the middle.
        (3,5,hello world)->qerhello worldjskel
        '''
        for i in range(0,garbage3):
            phrasePart1+=secrets.choice(alphabet)
        phrase2=""
        for i in range(0,garbage1):
            phrase2+=secrets.choice(alphabet)
        phrase2+=phrasePart1
        phrase2+=phrasePart2
        for i in range(0,garbage2):
            phrase2+=secrets.choice(alphabet)
        return phrase2
def Length(phrase,Garbage3Part2):
        '''(string)->int
        Returns the amount of letters that half the phrase has minus a certain number, rounded down.
        (hello world)->5
        '''
        return int((len(phrase)-Garbage3Part2)//2)
def GarbageDecrypt(phrase2,Garbage1Part2,Garbage2Part2,Garbage3Part2,garbage3):
        if Garbage1Part2 != 0 and Garbage2Part2 != 0 and Garbage3Part2 !=0:
                phrase2=phrase2[Garbage1Part2:-Garbage2Part2]
                halfway=Length(phrase2,Garbage3Part2)
                phrase2Part1=phrase2[:halfway]
                phrase2Part2=phrase2[halfway+Garbage3Part2:]
                phrase2=phrase2Part1+phrase2Part2
        elif Garbage1Part2!=0 and Garbage2Part2 !=0:
                phrase2=phrase2[Garbage1Part2:-Garbage2Part2] 
        elif Garbage1Part2 != 0 and Garbage3Part2 !=0:
                phrase2=phrase2[Garbage1Part2:]
                halfway=Length(phrase2,Garbage3Part2)
                phrase2Part1=phrase2[:halfway]
                phrase2Part2=phrase2[halfway+Garbage3Part2:]
                phrase2=phrase2Part1+phrase2Part2
        elif Garbage2Part2 !=0 and Garbage3Part2 !=0:
                phrase2=phrase2[:-Garbage2Part2]
                halfway=Length(phrase2,Garbage3Part2)
                phrase2Part1=phrase2[:halfway]
                phrase2Part2=phrase2[halfway+Garbage3Part2:]
                phrase2=phrase2Part1+phrase2Part2
        elif Garbage1Part2 != 0:
                phrase2=phrase2[Garbage1Part2:]
        elif Garbage2Part2 !=0:
                phrase2=phrase2[:-Garbage2Part2]
        elif Garbage3Part2 !=0:
                halfway=Length(phrase2,Garbage3Part2)
                phrase2Part1=phrase2[:halfway]
                phrase2Part2=phrase2[halfway+Garbage3Part2:]
                phrase2=phrase2Part1+phrase2Part2
        return phrase2
def EncryptionPhase(phrase,phrase2,garbage1,garbage2,garbage3,Garbage1Part1,Garbage2Part1,Garbage1Part2,Garbage2Part2,Garbage3Part1,Garbage3Part2,scramble,backward,shift,change1,change2,alphabet,conversion,SystemKey,n,EncryptionNumber1):
  '''Encrypts the message.'''
  '''phrase2 parameter literally has no purpose idk why it's there'''
  halfway=Length(phrase,0)
  if backward=="y":
      phrase2=phrase[::-1]
  else:
    phrase2=phrase
  phrase2=Garbage(Garbage1Part1,Garbage2Part1,Garbage3Part1,phrase2[:halfway],phrase2[halfway:])
  if scramble.lower()=="y":
      phrase2=ScramblingEncode(phrase2)
  phrase2=VowelsToNumbers(phrase2,alphabet,conversion)
  phrase2=caesar(phrase2,shift,change1)
  phrase2=VowelsToNumbers(phrase2,alphabet,conversion)
  if scramble.lower()=="y":
      phrase2=ScramblingEncode(phrase2)
  halfway=Length(phrase2,0)
  phrase2=Garbage(Garbage1Part2,Garbage2Part2,Garbage3Part2,phrase2[:halfway],phrase2[halfway:])
  if SystemKey.lower()=="y":
      phrase2=RSAEncryption(n,EncryptionNumber1,phrase2,alphabet)
  phrase2=VowelsToNumbers(phrase2,alphabet,conversion)
  phrase2=caesar(phrase2,shift,change2)
  phrase2=VowelsToNumbers(phrase2,alphabet,conversion)
  return phrase2
def DecryptionPhase(phrase,phrase2,garbage1,garbage2,Garbage1Part1,garbage3,Garbage2Part1,Garbage1Part2,Garbage2Part2,Garbage3Part1,Garbage3Part2,scramble,backward,shift,change1,change2,alphabet,conversion,SystemKey,n,EncryptionNumber2,conversionlength):
  '''Decrypts the code'''
  '''phrase parameter literally has no purpose idk why it's there'''
  phrase2=VowelsToNumbers(phrase2,conversion,alphabet)
  phrase2=caesar(phrase2, -shift,-change2)
  phrase2=VowelsToNumbers(phrase2,conversion,alphabet)
  if SystemKey.lower()=="y":
      phrase2=RSADecryption(n,EncryptionNumber2,phrase2,alphabet,conversionlength)
  phrase2=GarbageDecrypt(phrase2,Garbage1Part2,Garbage2Part2,Garbage3Part2,garbage3)
  if scramble.lower()=="y":
      phrase2=ScramblingDecode(phrase2)
  phrase2=VowelsToNumbers(phrase2,conversion,alphabet)
  phrase2=caesar(phrase2, -shift,-change1)
  phrase2=VowelsToNumbers(phrase2,conversion,alphabet)
  if scramble.lower()=="y":
      phrase2=ScramblingDecode(phrase2)
  phrase2=GarbageDecrypt(phrase2,Garbage1Part1,Garbage2Part1,Garbage3Part1,garbage3)
  if backward=="y":
    phrase2=phrase2[::-1]
  return phrase2

while True:
    conversionlength=10000
    while True:
        try:
            conversionlength=int(input("\nHow long do you want the key to be? (1000-65532) "))
            if conversionlength<=999 or conversionlength>=65533:
              print("Please check your input.")
            else:
              break
        except:
            print("\nIt has to be an integer.")
    try:
        keylist=KeyCreator(conversionlength)
        alphabet=KeyCreator(conversionlength)
    except Exception as e:
        print(e)
        #This is the backup system in case conversionlength doesn't work, DO NOT CHANGE.
        print("\nAn error occured.  Please check to see if conversionlength is below 1000 or above 65532.")
        keylist=KeyCreator(10000)
        alphabet=KeyCreator(10000)
        conversionlength=10000
    #Asks if you want to randomly generate a key or use an input.  If you select input, it asks you whether to input a key from scratch or use the previous key. If there is no previous key, asks you to generate a key from scratch. #DO NOT USE A KEY THAT WAS NOT GENERATED BY THIS PROGRAM.  IF YOU CREATE A KEY MANUALLY, THE PROGRAM WILL NOT WORK PROPERLY.
    key=input("\nDo you want to use an inputed key for the encryption?  (WARNING: YOU MUST USE AN INPUTTED KEY THAT HAS BEEN RANDOMLY GENERATED BY THIS PROGRAM) Y/N ")
    if key.lower()=="y":
        if conversion!="":
            key=input("\nUse the previous key? Y/N ")
        else:
            key="n"
        if key.lower()=="n":
            conversion=""
            key=input("\nUse a text file for a key? Y/N ")
            if key.lower()=="y":
                while True:
                    try:
                        #.txt needs to be appended after the filename, even if .txt is in the filename itself. 
                        key2=input("\nInput the path of the file: ")
                        key3=open(key2, encoding="utf8")
                        conversion=key3.read()
                        if int(len(conversion))!=conversionlength:
                            conversionlength=int(len(conversion))
                            alphabet=KeyCreator(conversionlength)
                        print("\nThe alphabet is: \n"+ "".join(alphabet))
                        print("\nThe key is: \n"+ conversion)
                        break
                    except Exception as e:
                        print(e)
                        print("That file does not exist, or there was an error with opening the file.  Be sure to only type the file name and not any file extensions, and check the error message printed.")
            else:    
                while len(conversion)!=conversionlength:
                    conversion=input("\nInput your key here: ")
                    print(len(conversion))
    else:
        conversion=""
        for i in range(0,conversionlength+1):
            variable=secrets.choice(keylist)
            keylist.remove(variable)
            conversion+=variable
        print("\nThe alphabet is: \n"+ "".join(alphabet))
        print("\nThe key is: \n"+ conversion)
    while True:
        purpose=input("\nDo you want to encrypt or decrypt? E/D ")
        if purpose.lower()=="e":
            purpose="encrypt"
        if purpose.lower()=="d":
            purpose="decrypt"
        if purpose.lower()=="encrypt" or purpose.lower()=="decrypt":
            break
        else:
            print("\nYou must specify to either encrypt or decrypt.")
    phrase=input("\nGive a phrase: ")
    while True:
        try:
            shift=int(input("\nHow many places to shift? "))
            change=int(input("\nHow many places to shift after each letter? "))
            break
        except ValueError:
            print("\nYou must specify a number.")
    while True:
          SystemKey=input("\nUse the public/private key system? Y/N ")
          if SystemKey.lower()=="y":
            RSACreator=input("\nGenerate a new public/private key, or use an old one? N/O ")
            if RSACreator.lower()!="o":
              while True:
                try:
                  prime1=int(input("\nWhat number is the first prime? "))
                  prime2=int(input("\nWhat number is the second prime? "))
                  primecheck1=PrimeCheck(prime1)
                  primecheck2=PrimeCheck(prime2)
                  if primecheck1 and primecheck2:
                    n,e,d=RSAKey(prime1,prime2)
                    print("\nThe public key is",e, "the private key is", d, " and n is",n)
                    if n>=conversionlength:
                      EncryptionNumber1=e
                      EncryptionNumber2=d
                      break
                    else:
                      print("\nn must be greater than or equal to conversionlength.")
                  else:
                    print("\nOne of the numbers inputted is not prime. Please check your input.")
                except ValueError:
                  print("\nYou must specify a number.")
            else:
              while True:
                try:
                  n=int(input("Input integer n. "))
                  if purpose.lower()=="encrypt":
                      EncryptionNumber1=int(input("\nPlease input the public key to encrypt the program. "))
                  else:
                      EncryptionNumber2=int(input("Please input the private key to decrypt the program. "))
                  break
                except:
                  print("Please check your input.")
          else:
            n=0
            EncryptionNumber1=0
            EncryptionNumber2=0
          break
    while True:
        #Asks the user to scramble letters, play the message backwards and add garbage letters to the beginning and end of the phrase.
        scramble=input("\nScramble letters? Y/N ")
        backward=input("\nRepeat message backwards? Y/N ")
        try:
            garbage1=int(input("\nHow many garbage letters to put at the beginning of the word? (0-infinity) "))
            garbage2=int(input("\nHow many garbage letters to put at the end of the word? (0-infinity) "))
            garbage3=int(input("\nHow many garbage letters to put in the middle of the word? (0-infinity) "))
            if garbage1>=0 and garbage2>=0 and garbage3 >=0:
                if scramble.lower()=="y" or scramble.lower()=="n":
                    if backward.lower()=="y" or backward.lower()=="n":
                        break
                    else:
                        print("\nBackwards needs to be either Y or N.")
                else:
                    print("\nScramble needs to be either Y or N.")
            else:
                print("\nGarbage1 and Garbage2 and Garbage3 need to be greater than or equal to zero.")
        except:
            print("\nPlease check your input.")
    #Checks to see if the process can be encrypted correctly. If it works, it encrypts the phrase.  If it is decrypted, the process is reversed.
    #If it doesn't encrypt & decrypt correctly, it sends a message that the message cannot be encrypted correctly.
    phrase2=phrase
    Garbage1Part2=garbage1//2
    Garbage1Part1=garbage1-Garbage1Part2
    Garbage2Part2=garbage2//2
    Garbage2Part1=garbage2-Garbage2Part2
    Garbage3Part2=garbage3//2
    Garbage3Part1=garbage3-Garbage3Part2
    change2=change//2
    change1=change-change2
    if purpose.lower() == "encrypt":
      Check=input("\nCheck to see if the encryption works correctly? Y/N ")
    else:
      Check = "n"
    #NOTE: You need to have knowledge of both the public and private keys in order to check the encryption if the RSA encryption is enabled.  Otherwise it doesn't work.
    if Check.lower()!="n" and SystemKey.lower()=="y"and EncryptionNumber1==0 and EncryptionNumber2==0:
      EncryptionNumber1=int(input("\nPlease input the public key to encrypt the program. "))
      EncryptionNumber2=int(input("\nPlease input the private key to decrypt the program. "))
    #This is where the encoding and decoding begins.
    if Check.lower()=="y":
        phrase2=EncryptionPhase(phrase,phrase2,garbage1,garbage2,garbage3,Garbage1Part1,Garbage2Part1,Garbage1Part2,Garbage2Part2,Garbage3Part1,Garbage3Part2,scramble,backward,shift,change1,change2,alphabet,conversion,SystemKey,n,EncryptionNumber1)
        phrase2=DecryptionPhase(phrase,phrase2,garbage1,garbage2,Garbage1Part1,garbage3,Garbage2Part1,Garbage1Part2,Garbage2Part2,Garbage3Part1,Garbage3Part2,scramble,backward,shift,change1,change2,alphabet,conversion,SystemKey,n,EncryptionNumber2,conversionlength)
    if phrase2==phrase:
        #phrase2=""
        #If decrypt is selected, decrypt code
        if purpose.lower()=="decrypt":
            phrase2=DecryptionPhase(phrase,phrase2,garbage1,garbage2,Garbage1Part1,garbage3,Garbage2Part1,Garbage1Part2,Garbage2Part2,Garbage3Part1,Garbage3Part2,scramble,backward,shift,change1,change2,alphabet,conversion,SystemKey,n,EncryptionNumber2,conversionlength)
            print("\n"+phrase2)
        else:
            #Otherwise, encrypt code
            phrase2=EncryptionPhase(phrase,phrase2,garbage1,garbage2,garbage3,Garbage1Part1,Garbage2Part1,Garbage1Part2,Garbage2Part2,Garbage3Part1,Garbage3Part2,scramble,backward,shift,change1,change2,alphabet,conversion,SystemKey,n,EncryptionNumber1)
            print("\n"+phrase2)
    else:
        print("\n"+phrase2)
        print("\nThe message does not encrypt properly.")
    #Asks if you want to make another message.  If you answer yes, repeats the whole script over again.
    save=input("\nDo you want to save the key to a text file? Y/N ")
    if save.lower()=="y":
        try:
            ask2=input("Input a pathname? Y/N ")
            if ask2.lower()=="y":
                ask=input("Please input a pathname for a text file. ")
                #The pathname for the file doesn't have to exist, it just needs to be in the right syntax.
                #An example of good syntax is: C:/Users/Pa Cyber/Documents/Encryption.txt
            else:
                ask='C:/Users/Pa Cyber/Documents/Encryption.txt'  
            test=open(ask,"ab")
            test.write(conversion.encode('utf-8'))
            test.close()
            print("\nKey saved.")
        except Exception as e:
            print(e)
            print("\nKey save failed.")
    x=input("\nDo you want to make another message?  Y/N ")
    if x.lower()=="n":
        break
