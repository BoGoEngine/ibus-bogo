from nose.tools import eq_
from gui import tablemodel


class TestUnikeyRulesImportExport():

    def test_parseUnikeyRules(self):
        unikeyContent = '''\
DO NOT DELETE THIS LINE*** version=1 ***
kg:không
kgcd:Không Gian Cộng Đồng
vn:Việt Nam
'''
        parsedRules = tablemodel.parseUnikeyRules(unikeyContent)

        expected_rules = {
            'kg': 'không',
            'kgcd': 'Không Gian Cộng Đồng',
            'vn': 'Việt Nam'
        }

        eq_(parsedRules, expected_rules)

    def test_parseUnikeyRules_wrong(self):
        unikeyContent = ""
        parsedRules = tablemodel.parseUnikeyRules(unikeyContent)

        eq_(parsedRules, {})

    def test_toUnikeyRules(self):
        rules = {
            'vn': 'Việt Nam',
            'kg': 'không'
        }

        unikeyRules = '''\
DO NOT DELETE THIS LINE*** version=1 ***
kg:không
vn:Việt Nam
'''
        eq_(tablemodel.toUnikeyRules(rules), unikeyRules)
