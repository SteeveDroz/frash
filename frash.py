#!/usr/bin/python3

#frash

def frash(string, length = 32, fractal = False, one = '#', zero = ' '):
  '''Frash allows to hash a string using a unique fractal algorithm.
  
  Parameters:
     string - The string to hash.
     length - The length of the returned string (multiply it by 4 to obtain the quantity of bits on which the input string is hashed).
    fractal - When set to "True", displays the fractal that has been used to hash the input string.
        one - The character representing a "1" in the visual fractal, only used if "fractal" is set to True.
       zero - The character representing a "0" in the visual fractal, only used if "fractal" is set to True.
  '''
  initialBinaryChain = '' # Each character of the string coded on 7 bits.
  numberOfBits = 8 * length # The number of bits necessary to code `length` characters. It should be 4 bits for a character (from 0 to f) but the quantity is doubled to avoid the 245a-paradox (see note below).
  for i in range(len(string)):
    character = str(bin(ord(string[i])))[2:]
    while len(character) < 7:
      character = '0' + character
    initialBinaryChain += character
  binaryChain = '' # An intermediate chain of bits that may contain a repeated message ("HelloHelloHello") to be at least the desired length.
  while len(binaryChain) < numberOfBits:
    binaryChain += initialBinaryChain
  sizedBinaryChain = '' # The chain of bits that will be used to develop the fractal.
  for i in range(numberOfBits):
    digit = 0
    j = i
    while j < len(binaryChain):
      digit += int(binaryChain[j]) # The chain is warped after `nuberOfBits` bits. All the bits on the same column are combined with an XOR logic gate to give the value of the givent bit in `sizedBinaryChain`.
      digit = digit % 2
      j += numberOfBits
    sizedBinaryChain += str(digit)
  shift = sizedBinaryChain.count('1') # `shift` will change the place of the row 0 in the fractal based on the number of bits set to 1 on the first row. If this step is ommited, similar input strings (i.e. "Hello" and "Hfllo") will return similar hashes.
  lineList = [] # The list of rows, which means this represents the fractal. It will contain a 2D array.
  lineList.append([])
  for i in range(numberOfBits):
    lineList[0].append(int(sizedBinaryChain[i:i + 1])) # The first row is made of the bits in the calculated binary chain.
  
  for i in range(1, 16): # The 15 next rows are calculated based on the previous row.
    digitList = []
    for j in range(numberOfBits):
      previous = lineList[i - 1][(j - 1) % numberOfBits]
      same = lineList[i - 1][j]
      next = lineList[i - 1][(j + 1) % numberOfBits]
      total = previous + same + next
      newDigit = 1
      if total < 1 or total > 2: # See notes for calculation algorithm.
        newDigit = 0
      digitList.append(newDigit)
    lineList.append(digitList)
  
  stringDigits = [str(lineList[0][n]) for n in range(0, numberOfBits, 2)] # The first row is shortened. Only the bits of even order are taken and changed to strings to allow concatenation. This reduction is to prevent froi the 245a-paradox, see notes.
  hashValue = ''
  for i in range(length):
    origin = '0b' + ''.join(stringDigits[i * 4:(i + 1) * 4]) # Each initial group of 4 bits form a number from 0 to f. This will decide on which row to take the bits that are part of the hash. Remember that the line 0 may be any of the lines due to the `shift` variable.
    stringDigitsSpecificLine = [str(n) for n in lineList[(int(origin,0) + shift) % 16]]
    shortenedDigits = [stringDigitsSpecificLine[n] for n in range(0, numberOfBits, 2)]
    finalValue = '0b' + ''.join(shortenedDigits[i * 4:(i + 1) * 4])
    hashValue += hex(int(finalValue,0))[2:] # The 4 bits from the fractal are transformed to hexadecimal and appent to the hash.
  
  if fractal: # if `fractal` is set to True, the fractal is displayed. 0's being ' ' and 1's being '#'.
    for line in lineList:
      for digit in line:
        if digit == 0:
          print(zero,end='')
        else:
          print(one,end='')
      print() 
  
  return hashValue

# Notes:
#
#   The 245a-paradox:
#     It can be mathematically proved that, except for the first one, no row of the fractal can contain a lone 1. 1's always go by 2 or more. As this matter, there can be no 2, 4, 5 or a in the hash, for 2 is coded 0010, 4 is coded 0100, 5 is coded 0101 and a is coded 1010.
#     8, for example, is coded 1000. At first sight, one could think that it's also touched by the same paradox, but there can be an 8 if the precedent number ends with a 1.
#     To avoid the lack of 2, 4, 5 and a's in the hash, the fractal is calculated on a width twice as long as necessary and the bits of the rows are taken on even columns only.
#
#   The algorithm:
#     Based on the three bits right above, one can calculate the value of a given bit. This calculation is based on a modified version of Conway's Game of Life.
#     Detailed mechanics:
#       000 001 010 011 100 101 110 111
#        0   1   1   1   1   1   1   0
#       If all the bits are the same, a 0 is written on the next line. Else, a 1 is written.
#     The fractal is wraped, so that the first bit is adjascent to the last one.
#
#   Complete frash example (simplified):
#     We want the string 'HELLO' to be hashed on 2 characters.
#     First, we translate the string into a chain of bits, which gives '10010001000101100110010011001001111'.
#     To hash 2 characters, we would need 2 * 4 = 8 bits, but to prevent from the 245a-paradox, that number must be doubled. The fractal will then be 16 characters wide.
#     The chain of bits is 35 bits long, which is more than the 16 needed. If it was too small, the chain would be duplicated and concatenated with itself. The chain 'HELLOHELLO' would be used, or even 'HELLOHELLOHELLO', and so on.
#     As the chain is too long, we will warp it each 16 characters and perform an XOR logic gate on each column:
#       1001000100010110
#       0110010011001001
#       111
#
#       0001010111011111
#
#       In other words, an even number of 1's in a column returns a 0, an odd number of 1's return a 1.
#     This is the chain of bits that will be used to generate the fractal with the algorithm described above. We will calculate the 15 next rows. Before we draw it, let's check which line will be considered as the line 0. We can simply count the number of 1's in the row above. There are 10, which means that the 10th line will have the id 0. Let's write ids on the left of the rows.
#       6 0001010111011111
#       7 1011111101110001
#       8 1110000111011011
#       9 0011001101111110
#       a 0111111111000011
#       b 1100000001100111
#       c 0110000011111100
#       d 1111000110000110
#       e 1001101111001111
#       f 1111111001111000
#       0 1000001111001101
#       1 1100011001111111
#       2 0110111111000000
#       3 1111100001100000
#       4 1000110011110000
#       5 1101111110011001
#     We can now reduce the width of the graph, the critical step with the 245a-paradox has been passed. Here is the result with only the even columns and separated groups of 4 bits:
#       6 0000 1011
#       7 1111 0100
#       8 1100 1011
#       9 0101 0111
#       a 0111 1001
#       b 1000 0101
#       c 0100 1110
#       d 1100 1001
#       e 1011 1011
#       f 1111 0110
#       0 1001 1010
#       1 1001 0111
#       2 0111 1000
#       3 1110 0100
#       4 1010 1100
#       5 1011 1010
#
#     To complete the hash, let's see what binary numbers compose the first row: 0000 and 1011, which correspond to 0 and b in hexadecimal. We will then take the first 4 bits from row 0 and the 4 last of row b. These bits are 1001 and 0101, which correspond in hexadecimal numbers to 9 and 5.
#     Conclusion: 'HELLO' is hashed 95.
#
#   Note that this is a tutorial, usual hashes are made on 32 or more characters (which correspond to 128 or more bits) and not on 2. For example, 'HELLO' is hashed 9c16af7827cbf3182ef40977effe7332 on 32 characters.
if __name__ == '__main__':
  string = 'Hello, World!'
  print(string, '=', frash(string))
