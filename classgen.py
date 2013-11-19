'''

A .clg file should contain a list of classes, with the following way.

The program file p5.clg serves as an example of what may be an input

class [class name]
includes /
members
[members]
memberline1
memberline2
methods
[methods]
methodblock1
'''

def translate(s):
  name = ''
  hpp = ''
  cpp = ''
  
  name, s = s.split('includes', 1)
  includes, s = s.split('members', 1)
  members, s = s.split('methods', 1)
  methods = s
  s = ''
  
  '''process name'''
  name = name.strip()
  
  '''process includes'''
  hppi, cppi = includes.split('/')
  cppi = name+'.hpp ' + cppi
  for x in hppi.split():
    if x.endswith('.hpp'): x = '\n#include"%s"'%x
    else: x = '\n#include<%s>'%x
    hpp += x
  for x in cppi.split():
    if x.endswith('.hpp'): x = '\n#include"%s"'%x
    else: x = '\n#include<%s>'%x
    cpp += x
    
  hpp += '\n\nclass '+name+'{\nprivate:'
  cpp += '\n'
  
  '''process members'''
  for line in members.splitlines():
    if line.strip() == '': continue
    typename, names = line.split('/')
    hpp += '\n  %s %s;'%(typename.strip(),','.join(names.split()))
    
  '''process methods'''
  def qual(proto):
    i = proto.find('(') - 1
    while proto[i].isalnum() or proto[i] in ['_','~']: i -= 1
    i += 1
    return '\n'+proto[:i]+name+'::'+proto[i:]
  hpp += '\npublic:'
  First = True
  for line in methods.splitlines():
    if line.strip() == '': continue
    if line.startswith('  '): cpp += '\n'+line
    else:
      if not First: cpp+='\n}'
      else: First = False
      line = line.replace('$$',name)
      cpp += qual('\n'+line.replace('%%',name+'::')+'{')
      hpp += '\n  '+line.replace('%%','')+';'
  hpp += '\n};'
  if not First: cpp+='\n}'
  return name, hpp.strip()+'\n', cpp.strip()+'\n'
  
def process_single_class(s):
  name, hpp, cpp = translate(s)
  with open(name+'.hpp','w') as f: f.write(hpp)
  with open(name+'.cpp','w') as f: f.write(cpp)

def process(s):
  for x in list(s.split('class'))[1:]:
    process_single_class(x)
  with open('start.cpp','w') as f:
    f.write(
'''#include "Main.hpp"
int main(int argc, char** argv) {
  return Main().run(argc, argv);
}
''')
  
if __name__ == '__main__':
  from sys import argv
  process(open(argv[1],'r').read())
