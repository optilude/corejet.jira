CoreJet test runner JIRA integration
====================================

This package provides a requirements catalogue source for
`corejet.testrunner`_ that can fetch requirements from JIRA.

To use it, make sure it is installed in the working set of the testrunner.
If using Buildout, you can do this with::

    [test]
    recipe = corejet.testrunner
    eggs = 
        corejet.jira
        <other packages>
    defaults = ['--auto-color', '--auto-progress']

Here is an example command line invocation::

  ./bin/test -s corejet.core --corejet="jira,url=https://acme.jira.com,username=corejet,password=secret,project=Acme Corp,filter=10151,pointsField=10060,epicField=10061,acceptanceCriteriaField=10088"

The ``--corejet`` option must start with ``jira,`` followed by a set of
parameters that indicate how to connect to JIRA. The parameters are:

``url=<url>``
    URL of JIRA instance
``username=<username>``
    username to use to connect
``password=<password>``
    password to use to connect
``project=<name>``
    Name of project
``filter=<id>``
    Numeric id of filter that returns stories
``pointsField=<id>``
    Numeric id of field containing story points
``epicField=<id>``
    Numeric id of field indicating epic for a story
``acceptanceCriteriaField=<id>``
    Numeric id of field containing acceptance criteria (scenarios)

This presumes JIRA is set up with a filter that returns all stories you want
to include (e.g. return all valid issues of type ``Story`` in the project, if
using GreenHopper). The various field ids describe the fields that provide
story points, epic/theme (either a string or a reference to another issue),
and a field with acceptance criteria.

The first two are standard GreenHopper fields. The acceptance criteria field
must be added manually. It should be a plain text field containing scenarios
in simple Gherkin syntax, e.g.::

    Scenario: First scenario
    Given a precondition
      And another precondition
    When something happens
      And something else happens
    Then a result is expected
      And another result is expected
    
    Scenario: Second scenario
    Given another precondition
    When something else happens
    Then a different result is expected

The parser is relatively forgiving, but note:

 * The parser is case-insensitive
 * Zero or more scenarios may be present
 * Scenarios must start with "Scenario: " followed by a name
 * The "Given" clause is optional, but must come first in a scenario
 * The "When" clause is required, and must come before the "Then" clause
 * The "Then"" clause is also required
 * An "And" clause can come after any "Given", "When" or "Then", but not
   first.

.. _corejet.testrunner: http://pypi.python.org/pypi/corejet.testrunner
