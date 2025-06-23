import os
import tempfile
import datetime

import dbf
from dbf import *
from dbf.constants import *

from common import *


class TestQuantum(TestCase):
    "Testing Quantum"

    def test_exceptions(self):
        "errors"
        self.assertRaises(ValueError, Quantum, 'wrong')
        self.assertRaises(TypeError, lambda : (0, 1, 2)[On])
        self.assertRaises(TypeError, lambda : (0, 1, 2)[Off])
        self.assertRaises(TypeError, lambda : (0, 1, 2)[Other])

    def test_other(self):
        "Other"
        huh = unknown = Quantum('')
        self.assertEqual(huh is dbf.Other, True)
        self.assertEqual((huh != huh) is unknown, True)
        self.assertEqual((huh != True) is unknown, True)
        self.assertEqual((huh != False) is unknown, True)

        huh = Quantum('?')
        self.assertEqual(huh is dbf.Other, True)
        self.assertEqual((huh != huh) is unknown, True)
        self.assertEqual((huh != True) is unknown, True)
        self.assertEqual((huh != False) is unknown, True)

        huh = Quantum(' ')
        self.assertEqual(huh is dbf.Other, True)
        self.assertEqual((huh != huh) is unknown, True)
        self.assertEqual((huh != True) is unknown, True)
        self.assertEqual((huh != False) is unknown, True)

        huh = Quantum(None)
        self.assertEqual(huh is dbf.Other, True)
        self.assertEqual((huh != huh) is unknown, True)
        self.assertEqual((huh != True) is unknown, True)
        self.assertEqual((huh != False) is unknown, True)

        huh = Quantum(Null())
        self.assertEqual(huh is dbf.Other, True)
        self.assertEqual((huh != huh) is unknown, True)
        self.assertEqual((huh != True) is unknown, True)
        self.assertEqual((huh != False) is unknown, True)

        huh = Quantum(Other)
        self.assertEqual(huh is dbf.Other, True)
        self.assertEqual((huh != huh) is unknown, True)
        self.assertEqual((huh != True) is unknown, True)
        self.assertEqual((huh != False) is unknown, True)

        huh = Quantum(Unknown)
        self.assertEqual(huh is dbf.Other, True)
        self.assertEqual((huh != huh) is unknown, True)
        self.assertEqual((huh != True) is unknown, True)
        self.assertEqual((huh != False) is unknown, True)

    def test_true(self):
        "true"
        huh = Quantum('True')
        unknown = Quantum('?')
        self.assertEqual(huh, True)
        self.assertNotEqual(huh, False)
        self.assertEqual((huh != None) is unknown, True)

        huh = Quantum('yes')
        unknown = Quantum('?')
        self.assertEqual(huh, True)
        self.assertNotEqual(huh, False)
        self.assertEqual((huh != None) is unknown, True)

        huh = Quantum('t')
        unknown = Quantum('?')
        self.assertEqual(huh, True)
        self.assertNotEqual(huh, False)
        self.assertEqual((huh != None) is unknown, True)

        huh = Quantum('Y')
        unknown = Quantum('?')
        self.assertEqual(huh, True)
        self.assertNotEqual(huh, False)
        self.assertEqual((huh != None) is unknown, True)

        huh = Quantum(7)
        unknown = Quantum('?')
        self.assertEqual(huh, True)
        self.assertNotEqual(huh, False)
        self.assertEqual((huh != None) is unknown, True)

        huh = Quantum(['blah'])
        unknown = Quantum('?')
        self.assertEqual(huh, True)
        self.assertNotEqual(huh, False)
        self.assertEqual((huh != None) is unknown, True)

    def test_false(self):
        "false"
        huh = Quantum('false')
        unknown = Quantum('?')
        self.assertEqual(huh, False)
        self.assertNotEqual(huh, True)
        self.assertEqual((huh != None) is unknown, True)

        huh = Quantum('No')
        unknown = Quantum('?')
        self.assertEqual(huh, False)
        self.assertNotEqual(huh, True)
        self.assertEqual((huh != None) is unknown, True)

        huh = Quantum('F')
        unknown = Quantum('?')
        self.assertEqual(huh, False)
        self.assertNotEqual(huh, True)
        self.assertEqual((huh != None) is unknown, True)

        huh = Quantum('n')
        unknown = Quantum('?')
        self.assertEqual(huh, False)
        self.assertNotEqual(huh, True)
        self.assertEqual((huh != None) is unknown, True)

        huh = Quantum(0)
        unknown = Quantum('?')
        self.assertEqual(huh, False)
        self.assertNotEqual(huh, True)
        self.assertEqual((huh != None) is unknown, True)

        huh = Quantum([])
        unknown = Quantum('?')
        self.assertEqual(huh, False)
        self.assertNotEqual(huh, True)
        self.assertEqual((huh != None) is unknown, True)

    def test_singletons(self):
        "singletons"
        heh = Quantum(True)
        hah = Quantum('Yes')
        ick = Quantum(False)
        ack = Quantum([])
        unk = Quantum('?')
        bla = Quantum(None)
        self.assertEqual(heh is hah, True)
        self.assertEqual(ick is ack, True)
        self.assertEqual(unk is bla, True)

    def test_or(self):
        "or"
        true = Quantum(True)
        false = Quantum(False)
        unknown = Quantum(None)
        self.assertEqual(true + true, true)
        self.assertEqual(true + false, true)
        self.assertEqual(false + true, true)
        self.assertEqual(false + false, false)
        self.assertEqual(true + unknown, true)
        self.assertEqual(false + unknown is unknown, True)
        self.assertEqual(unknown + unknown is unknown, True)
        self.assertEqual(true | true, true)
        self.assertEqual(true | false, true)
        self.assertEqual(false | true, true)
        self.assertEqual(false | false, false)
        self.assertEqual(true | unknown, true)
        self.assertEqual(false | unknown is unknown, True)
        self.assertEqual(unknown | unknown is unknown, True)
        self.assertEqual(true + True, true)
        self.assertEqual(true + False, true)
        self.assertEqual(false + True, true)
        self.assertEqual(false + False, false)
        self.assertEqual(true + None, true)
        self.assertEqual(false + None is unknown, True)
        self.assertEqual(unknown + None is unknown, True)
        self.assertEqual(true | True, true)
        self.assertEqual(true | False, true)
        self.assertEqual(false | True, true)
        self.assertEqual(false | False, false)
        self.assertEqual(true | None, true)
        self.assertEqual(false | None is unknown, True)
        self.assertEqual(unknown | None is unknown, True)
        self.assertEqual(True + true, true)
        self.assertEqual(True + false, true)
        self.assertEqual(False + true, true)
        self.assertEqual(False + false, false)
        self.assertEqual(True + unknown, true)
        self.assertEqual(False + unknown is unknown, True)
        self.assertEqual(None + unknown is unknown, True)
        self.assertEqual(True | true, true)
        self.assertEqual(True | false, true)
        self.assertEqual(False | true, true)
        self.assertEqual(False | false, false)
        self.assertEqual(True | unknown, true)
        self.assertEqual(False | unknown is unknown, True)
        self.assertEqual(None | unknown is unknown, True)

    def test_and(self):
        "and"
        true = Quantum(True)
        false = Quantum(False)
        unknown = Quantum(None)
        self.assertEqual(true * true, true)
        self.assertEqual(true * false, false)
        self.assertEqual(false * true, false)
        self.assertEqual(false * false, false)
        self.assertEqual(true * unknown is unknown, True)
        self.assertEqual(false * unknown, false)
        self.assertEqual(unknown * unknown is unknown, True)
        self.assertEqual(true & true, true)
        self.assertEqual(true & false, false)
        self.assertEqual(false & true, false)
        self.assertEqual(false & false, false)
        self.assertEqual(true & unknown is unknown, True)
        self.assertEqual(false & unknown, false)
        self.assertEqual(unknown & unknown is unknown, True)
        self.assertEqual(true * True, true)
        self.assertEqual(true * False, false)
        self.assertEqual(false * True, false)
        self.assertEqual(false * False, false)
        self.assertEqual(true * None is unknown, True)
        self.assertEqual(false * None, false)
        self.assertEqual(unknown * None is unknown, True)
        self.assertEqual(true & True, true)
        self.assertEqual(true & False, false)
        self.assertEqual(false & True, false)
        self.assertEqual(false & False, false)
        self.assertEqual(true & None is unknown, True)
        self.assertEqual(false & None, false)
        self.assertEqual(unknown & None is unknown, True)
        self.assertEqual(True * true, true)
        self.assertEqual(True * false, false)
        self.assertEqual(False * true, false)
        self.assertEqual(False * false, false)
        self.assertEqual(True * unknown is unknown, True)
        self.assertEqual(False * unknown, false)
        self.assertEqual(None * unknown is unknown, True)
        self.assertEqual(True & true, true)
        self.assertEqual(True & false, false)
        self.assertEqual(False & true, false)
        self.assertEqual(False & false, false)
        self.assertEqual(True & unknown is unknown, True)
        self.assertEqual(False & unknown, false)
        self.assertEqual(None & unknown is unknown, True)

    def test_xor(self):
        "xor"
        true = Quantum(True)
        false = Quantum(False)
        unknown = Quantum(None)
        self.assertEqual(true ^ true, false)
        self.assertEqual(true ^ false, true)
        self.assertEqual(false ^ true, true)
        self.assertEqual(false ^ false, false)
        self.assertEqual(true ^ unknown is unknown, True)
        self.assertEqual(false ^ unknown is unknown, True)
        self.assertEqual(unknown ^ unknown is unknown, True)
        self.assertEqual(true ^ True, false)
        self.assertEqual(true ^ False, true)
        self.assertEqual(false ^ True, true)
        self.assertEqual(false ^ False, false)
        self.assertEqual(true ^ None is unknown, True)
        self.assertEqual(false ^ None is unknown, True)
        self.assertEqual(unknown ^ None is unknown, True)
        self.assertEqual(True ^ true, false)
        self.assertEqual(True ^ false, true)
        self.assertEqual(False ^ true, true)
        self.assertEqual(False ^ false, false)
        self.assertEqual(True ^ unknown is unknown, True)
        self.assertEqual(False ^ unknown is unknown, True)
        self.assertEqual(None ^ unknown is unknown, True)

    def test_implication_material(self):
        "implication, material"
        true = Quantum(True)
        false = Quantum(False)
        unknown = Quantum(None)
        self.assertEqual(true >> true, true)
        self.assertEqual(true >> false, false)
        self.assertEqual(false >> true, true)
        self.assertEqual(false >> false, true)
        self.assertEqual(true >> unknown is unknown, True)
        self.assertEqual(false >> unknown, true)
        self.assertEqual(unknown >> unknown is unknown, True)
        self.assertEqual(true >> True, true)
        self.assertEqual(true >> False, false)
        self.assertEqual(false >> True, true)
        self.assertEqual(false >> False, true)
        self.assertEqual(true >> None is unknown, True)
        self.assertEqual(false >> None, true)
        self.assertEqual(unknown >> None is unknown, True)
        self.assertEqual(True >> true, true)
        self.assertEqual(True >> false, false)
        self.assertEqual(False >> true, true)
        self.assertEqual(False >> false, true)
        self.assertEqual(True >> unknown is unknown, True)
        self.assertEqual(False >> unknown, true)
        self.assertEqual(None >> unknown is unknown, True)

    def test_implication_relevant(self):
        "implication, relevant"
        true = Quantum(True)
        false = Quantum(False)
        unknown = Quantum(None)
        Quantum.set_implication('relevant')
        self.assertEqual(true >> true, true)
        self.assertEqual(true >> false, false)
        self.assertEqual(false >> true is unknown, True)
        self.assertEqual(false >> false is unknown, True)
        self.assertEqual(true >> unknown is unknown, True)
        self.assertEqual(false >> unknown is unknown, True)
        self.assertEqual(unknown >> unknown is unknown, True)
        self.assertEqual(true >> True, true)
        self.assertEqual(true >> False, false)
        self.assertEqual(false >> True is unknown, True)
        self.assertEqual(false >> False is unknown, True)
        self.assertEqual(true >> None is unknown, True)
        self.assertEqual(false >> None is unknown, True)
        self.assertEqual(unknown >> None is unknown, True)
        self.assertEqual(True >> true, true)
        self.assertEqual(True >> false, false)
        self.assertEqual(False >> true is unknown, True)
        self.assertEqual(False >> false is unknown, True)
        self.assertEqual(True >> unknown is unknown, True)
        self.assertEqual(False >> unknown is unknown, True)
        self.assertEqual(None >> unknown is unknown, True)

    def test_nand(self):
        "negative and"
        true = Quantum(True)
        false = Quantum(False)
        unknown = Quantum(None)
        self.assertEqual(true.D(true), false)
        self.assertEqual(true.D(false), true)
        self.assertEqual(false.D(true), true)
        self.assertEqual(false.D(false), true)
        self.assertEqual(true.D(unknown) is unknown, True)
        self.assertEqual(false.D(unknown), true)
        self.assertEqual(unknown.D(unknown) is unknown, True)
        self.assertEqual(true.D(True), false)
        self.assertEqual(true.D(False), true)
        self.assertEqual(false.D(True), true)
        self.assertEqual(false.D(False), true)
        self.assertEqual(true.D(None) is unknown, True)
        self.assertEqual(false.D(None), true)
        self.assertEqual(unknown.D(None) is unknown, True)

    def test_negation(self):
        "negation"
        true = Quantum(True)
        false = Quantum(False)
        none = Quantum(None)
        self.assertEqual(-true, false)
        self.assertEqual(-false, true)
        self.assertEqual(-none is none, True)


class TestExceptions(TestCase):

    def test_bad_field_specs_on_creation(self):
        self.assertRaises(FieldSpecError, Table, 'blah', 'age N(3,2)', on_disk=False)
        self.assertRaises(FieldSpecError, Table, 'blah', 'name C(300)', on_disk=False)
        self.assertRaises(FieldSpecError, Table, 'blah', 'born L(9)', on_disk=False)
        self.assertRaises(FieldSpecError, Table, 'blah', 'married D(12)', on_disk=False)
        self.assertRaises(FieldSpecError, Table, 'blah', 'desc M(1)', on_disk=False)
        self.assertRaises(FieldSpecError, Table, 'blah', 'desc', on_disk=False)

    def test_too_many_fields_on_creation(self):
        fields = []
        for i in range(255):
            fields.append('a%03d C(10)' % i)
        Table(':test:', ';'.join(fields), on_disk=False)
        fields.append('a255 C(10)')
        self.assertRaises(DbfError, Table, ':test:', ';'.join(fields), on_disk=False)

    def test_adding_too_many_fields(self):
        fields = []
        for i in range(255):
            fields.append('a%03d C(10)' % i)
        table = Table(':test:', ';'.join(fields), on_disk=False)
        table.open(mode=READ_WRITE)
        self.assertRaises(DbfError, table.add_fields, 'a255 C(10)')

    def test_adding_too_many_fields_with_null(self):
        fields = []
        for i in range(254):
            fields.append(u'a%03d C(10) NULL' % i)
        table = Table(':test:', u';'.join(fields), dbf_type='vfp', on_disk=False)
        table.open(mode=READ_WRITE)
        self.assertRaises(DbfError, table.add_fields, u'a255 C(10)')
        fields = []
        for i in range(254):
            fields.append(u'a%03d C(10) NULL' % i)
        table = Table(':test:', u';'.join(fields), dbf_type='vfp', on_disk=False)
        table.open(mode=READ_WRITE)
        self.assertRaises(DbfError, table.add_fields, u'a255 C(10)')

    def test_too_many_records_in_table(self):
        "skipped -- test takes waaaaaaay too long"

    def test_too_many_fields_to_change_to_null(self):
        fields = []
        for i in range(255):
            fields.append('a%03d C(10)' % i)
        table = Table(':test:', ';'.join(fields), on_disk=False)
        table.open(mode=READ_WRITE)
        try:
            self.assertRaises(DbfError, table.allow_nulls, 'a001')
        finally:
            table.close()

    def test_adding_existing_field_to_table(self):
        table = Table(':blah:', 'name C(50)', on_disk=False)
        self.assertRaises(DbfError, table.add_fields, 'name C(10)')

    def test_deleting_non_existing_field_from_table(self):
        table = Table(':bleh:', 'name C(25)', on_disk=False)
        self.assertRaises(DbfError, table.delete_fields, 'age')

    def test_modify_packed_record(self):
        table = Table(':ummm:', 'name C(3); age N(3,0)', on_disk=False)
        table.open(mode=READ_WRITE)
        for person in (('me', 25), ('you', 35), ('her', 29)):
            table.append(person)
        record = table[1]
        dbf.delete(record)
        table.pack()
        self.assertEqual(('you', 35), record)
        self.assertRaises(DbfError, dbf.write, record, **{'age':33})

    def test_read_only(self):
        table = Table(':ahhh:', 'name C(10)', on_disk=False)
        table.open(mode=dbf.READ_ONLY)
        self.assertRaises(DbfError, table.append, dict(name='uh uh!'))

    def test_clipper(self):
        Table(os.path.join(tempdir, 'temptable'), 'name C(377); thesis C(20179)', dbf_type='clp')
        self.assertRaises(BadDataError, Table, os.path.join(tempdir, 'temptable'))

    def test_data_overflow(self):
        table = Table(os.path.join(tempdir, 'temptable'), 'mine C(2); yours C(15)')
        table.open(mode=READ_WRITE)
        table.append(('me',))
        try:
            table.append(('yours',))
        except DataOverflowError:
            pass
        finally:
            table.close()

    def test_change_null_field(self):
        "cannot making an existing field nullable"
        table = Table(
                os.path.join(tempdir, 'vfp_table'),
                'name C(25); paid L; qty N(11,5); orderdate D; desc M; mass B;' +
                ' weight F(18,3); age I; meeting T; misc G; photo P; price Y;' +
                ' dist B',
                dbf_type='vfp',
                default_data_types='enhanced',
                )
        table.open(mode=READ_WRITE)
        namelist = []
        paidlist = []
        qtylist = []
        orderlist = []
        desclist = []
        for i in range(10):
            name = words[i]
            paid = len(words[i]) % 3 == 0
            qty = floats[i]
            orderdate = datetime.date((numbers[i] + 1) * 2, (numbers[i] % 12) +1, (numbers[i] % 27) + 1)
            desc = ' '.join(words[i:i+50])
            namelist.append(name)
            paidlist.append(paid)
            qtylist.append(qty)
            orderlist.append(orderdate)
            desclist.append(desc)
            table.append({u'name':name, u'paid':paid, u'qty':qty, u'orderdate':orderdate, u'desc':desc})
        # plus a blank record
        namelist.append('')
        paidlist.append(None)
        qtylist.append(None)
        orderlist.append(None)
        desclist.append('')
        table.append()
        for field in table.field_names:
            self.assertEqual(table.nullable_field(field), False)
        self.assertRaises(DbfError, table.allow_nulls, (u'name, qty'))
        table.close()
