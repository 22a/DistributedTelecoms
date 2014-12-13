#super quick stab at the phoenetic string representation builder

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
  for c in range(0, len(name)):
    if name[c] in t0:
      out+='0'
    elif name[c] in t1:
      out+='1'
    elif name[c] in t2:
      out+='2'
    elif name[c] in t3:
      out+='3'
    elif name[c] == 'L':
      out+='4'
    elif name[c] in t5:
      out+='5'
    elif name[c] == 'R':
      out+='6'
    else:
      out+='?'


  print 'out =',out

  #remove all adjacent duplicates
  for i in range(len(out)):         #this will probably go out of bounds
    if i is not len(out)-1 and out[i+1] == out[i]:
      print(i)    
      out = out.replace(out[i], '', 1)


  for i in range(len(out)):
    if out[i] is not '0':
      for c in range(i, len(out)):   
        out = out[:i-1] + out[i:].replace('0', '')    #replace all non leading zeros
        break

  out = out[:4]     #reduce to 4 chars

  out[0] = name[0]    #replace leading digit with first letter of name

  return out

if __name__ == '__main__':
  print phonetify('PETER')

