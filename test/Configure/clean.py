#!/usr/bin/env python
#
# MIT License
#
# Copyright The SCons Foundation
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE

"""
Verify that we don't perform Configure context actions when the
-c or --clean options have been specified.
"""

import TestSCons

test = TestSCons.TestSCons(match = TestSCons.match_re_dotall)

test.write('SConstruct', """\
DefaultEnvironment(tools=[])
env = Environment()
import os
env.AppendENVPath('PATH', os.environ['PATH'])
conf = Configure(env, clean=int(ARGUMENTS['clean']))
r1 = conf.CheckCHeader( 'math.h' )
r2 = conf.CheckCHeader( 'no_std_c_header.h' ) # leads to compile error
env = conf.Finish()
Export( 'env' )
SConscript( 'SConscript' )
""")

test.write('SConscript', """\
Import( 'env' )
env.Program( 'TestProgram', 'TestProgram.c' )
""")

test.write('TestProgram.c', """\
#include <stdio.h>

int main(void) {
  printf( "Hello\\n" );
}
""")

lines = [
    "Checking for C header file math.h... ",
    "Checking for C header file no_std_c_header.h... "
]

test.run(arguments = '-c clean=0')
test.must_not_contain_any_line(test.stdout(), lines)

test.run(arguments = '-c clean=1')
test.must_contain_all_lines(test.stdout(), lines)

test.run(arguments = '--clean clean=0')
test.must_not_contain_any_line(test.stdout(), lines)

test.run(arguments = '--clean clean=1')
test.must_contain_all_lines(test.stdout(), lines)

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
