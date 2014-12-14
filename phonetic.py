#super quick stab at the phoenetic string representation builder
#only works on upercase for the minute, can be easily extended to lowercase
#perhaps the query only be run on either first or last name, I have no incoding for space

def phonetify(name = "TWEEZER"):
  out = ''
  t0 = ['A','E','I','O','U','H','W','Y']
  t1 = ['B','F','P','V']
  t2 = ['C','G','K','Q','S','X','Z']
  t3 = ['D','T']
  # 4 = 'L'
  t5 = ['M','N']
  # 6 = 'R'

  #replace all chars with grouping num
  for c in name:
    if c in t0:
      out+='0'
    elif c in t1:
      out+='1'
    elif c in t2:
      out+='2'
    elif c in t3:
      out+='3'
    elif c == 'L':
      out+='4'
    elif c in t5:
      out+='5'
    elif c == 'R':
      out+='6'
    else:
      out+='?'

  #remove all adjacent duplicates
  for i in range(len(out)):
    if i is not len(out)-1 and out[i+1] == out[i]:
      print(i)    
      out = out.replace(out[i], '', 1)


  for i in range(len(out)):
    if out[i] is not '0':  
      out = out[:i] + out[i:].replace('0', '')    #replace all non leading zeros
      break

  out = out[:4]     #reduce to 4 chars

  out = name[0] + out[1:]  #replace leading digit with first letter of name

  return out

if __name__ == '__main__':
  print phonetify('PETER')

