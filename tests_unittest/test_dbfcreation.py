import os
import tempfile
import datetime

import dbf
from dbf import *
from dbf.constants import *

from common import *


class TestDbfCreation(TestCase):
    "Testing table creation..."

    def test_db3_memory_tables(self):
        "dbf tables in memory"
        fields = unicodify(['name C(25)', 'hiredate D', 'male L', 'wisdom M', 'qty N(3,0)', 'weight F(7,3)'])
        for i in range(1, len(fields)+1):
            for fieldlist in combinate(fields, i):
                table = Table(':memory:', fieldlist, dbf_type='db3', on_disk=False)
                actualFields = table.structure()
                self.assertEqual(fieldlist, actualFields)
                self.assertTrue(all([type(x) is unicode for x in table.field_names]))

    def test_db3_disk_tables(self):
        "dbf table on disk"
        fields = unicodify(['name C(25)', 'hiredate D', 'male L', 'wisdom M', 'qty N(3,0)', 'weight F(7,3)'])
        for i in range(1, len(fields)+1):
            for fieldlist in combinate(fields, i):
                table = Table(os.path.join(tempdir, 'temptable'), ';'.join(fieldlist), dbf_type='db3')
                table = Table(os.path.join(tempdir, 'temptable'), dbf_type='db3')
                actualFields = table.structure()
                self.assertEqual(fieldlist, actualFields)
                table = open(table.filename, 'rb')
                try:
                    last_byte = ord(table.read()[-1])
                finally:
                    table.close()
                self.assertEqual(last_byte, EOF)

    def test_clp_memory_tables(self):
        "clp tables in memory"
        fields = unicodify(['name C(10977)', 'hiredate D', 'male L', 'wisdom M', 'qty N(3,0)', 'weight F(7,3)'])
        for i in range(1, len(fields)+1):
            for fieldlist in combinate(fields, i):
                table = Table(':memory:', fieldlist, dbf_type='clp', on_disk=False)
                actualFields = table.structure()
                self.assertEqual(fieldlist, actualFields)
                self.assertTrue(all([type(x) is unicode for x in table.field_names]))

    def test_clp_disk_tables(self):
        "clp table on disk"
        table = Table(os.path.join(tempdir, 'temptable'), u'name C(377); thesis C(20179)', dbf_type='clp')
        self.assertEqual(table.record_length, 20557)
        fields = unicodify(['name C(10977)', 'hiredate D', 'male L', 'wisdom M', 'qty N(3,0)', 'weight F(7,3)'])
        for i in range(1, len(fields)+1):
            for fieldlist in combinate(fields, i):
                table = Table(os.path.join(tempdir, 'temptable'), u';'.join(fieldlist), dbf_type='clp')
                table = Table(os.path.join(tempdir, 'temptable'), dbf_type='clp')
                actualFields = table.structure()
                self.assertEqual(fieldlist, actualFields)
                table = open(table.filename, 'rb')
                try:
                    last_byte = ord(table.read()[-1])
                finally:
                    table.close()
                self.assertEqual(last_byte, EOF)

    def test_fp_memory_tables(self):
        "fp tables in memory"
        fields = unicodify(['name C(25)', 'hiredate D', 'male L', 'wisdom M', 'qty N(3,0)',
                  'litres F(11,5)', 'blob G', 'graphic P', 'weight F(7,3)'])
        for i in range(1, len(fields)+1):
            for fieldlist in combinate(fields, i):
                table = Table(':memory:', u';'.join(fieldlist), dbf_type='fp', on_disk=False)
                actualFields = table.structure()
                self.assertEqual(fieldlist, actualFields)

    def test_fp_disk_tables(self):
        "fp tables on disk"
        fields = unicodify(['name C(25)', 'hiredate D', 'male L', 'wisdom M', 'qty N(3,0)',
                  'litres F(11,5)', 'blob G', 'graphic P', 'weight F(7,3)'])
        for i in range(1, len(fields)+1):
            for fieldlist in combinate(fields, i):
                table = Table(os.path.join(tempdir, 'tempfp'), u';'.join(fieldlist), dbf_type='fp')
                table = Table(os.path.join(tempdir, 'tempfp'), dbf_type='fp')
                actualFields = table.structure()
                self.assertEqual(fieldlist, actualFields)

    def test_vfp_memory_tables(self):
        "vfp tables in memory"
        fields = unicodify(['name C(25)', 'hiredate D', 'male L', 'wisdom M', 'qty N(3,0)',
                  'mass B', 'litres F(11,5)', 'int I', 'birth T', 'blob G', 'graphic P',
                  'menu C(50) BINARY', 'graduated L NULL', 'fired D NULL', 'cipher C(50) NOCPTRANS NULL',
                  'weight F(7,3)'])

        for i in range(1, len(fields)+1):
            for fieldlist in combinate(fields, i):
                table = Table(':memory:', u';'.join(fieldlist), dbf_type='vfp', on_disk=False)
                actualFields = table.structure()
                fieldlist = [f.replace('NOCPTRANS','BINARY') for f in fieldlist]
                self.assertEqual(fieldlist, actualFields)

    def test_vfp_disk_tables(self):
        "vfp tables on disk"
        fields = unicodify(['name C(25)', 'hiredate D', 'male L', 'wisdom M', 'qty N(3,0)',
                  'mass B', 'litres F(11,5)', 'int I', 'birth T', 'blob G', 'graphic P',
                  'menu C(50) binary', 'graduated L null', 'fired D NULL', 'cipher C(50) nocptrans NULL',
                  'weight F(7,3)'])
        for i in range(1, len(fields)+1):
            for fieldlist in combinate(fields, i):
                table = Table(os.path.join(tempdir, 'tempvfp'), u';'.join(fieldlist), dbf_type='vfp')
                table = Table(os.path.join(tempdir, 'tempvfp'), dbf_type='vfp')
                actualFields = table.structure()
                fieldlist = [f.replace('nocptrans','BINARY') for f in fieldlist]
                self.assertEqual(fieldlist, actualFields)

    def test_codepage(self):
        table = Table(os.path.join(tempdir, 'tempvfp'), u'name C(25); male L; fired D NULL', dbf_type='vfp')
        table.close()
        self.assertEqual(dbf.default_codepage, 'ascii')
        self.assertEqual(table.codepage, dbf.CodePage('ascii'))
        table.close()
        table.open(mode=READ_WRITE)
        table.close()
        table = Table(os.path.join(tempdir, 'tempvfp'), u'name C(25); male L; fired D NULL', dbf_type='vfp', codepage='cp850')
        table.close()
        self.assertEqual(table.codepage, dbf.CodePage('cp850'))

        newtable = table.new('tempvfp2', codepage='cp437')
        self.assertEqual(newtable.codepage, dbf.CodePage('cp437'))
        newtable.open(mode=READ_WRITE)
        newtable.create_backup()
        newtable.close()
        bckup = Table(os.path.join(tempdir, newtable.backup))
        self.assertEqual(bckup.codepage, newtable.codepage)

    def test_db3_ignore_memos(self):
        table = Table(os.path.join(tempdir, 'tempdb3'), u'name C(25); wisdom M', dbf_type='db3').open(mode=READ_WRITE)
        table.append(('QC Tester', 'check it twice!  check it thrice!  check it . . . uh . . . again!'))
        table.close()
        table = Table(os.path.join(tempdir, 'tempdb3'), dbf_type='db3', ignore_memos=True)
        table.open(mode=READ_WRITE)
        try:
            self.assertEqual(table[0].wisdom, u'')
        finally:
            table.close()

    def test_fp_ignore_memos(self):
        table = Table(os.path.join(tempdir, 'tempdb3'), u'name C(25); wisdom M', dbf_type='fp').open(mode=READ_WRITE)
        table.append(('QC Tester', 'check it twice!  check it thrice!  check it . . . uh . . . again!'))
        table.close()
        table = Table(os.path.join(tempdir, 'tempdb3'), dbf_type='fp', ignore_memos=True)
        table.open(mode=READ_WRITE)
        try:
            self.assertEqual(table[0].wisdom, u'')
        finally:
            table.close()

    def test_vfp_ignore_memos(self):
        table = Table(os.path.join(tempdir, 'tempdb3'), u'name C(25); wisdom M', dbf_type='vfp').open(mode=READ_WRITE)
        table.append(('QC Tester', 'check it twice!  check it thrice!  check it . . . uh . . . again!'))
        table.close()
        table = Table(os.path.join(tempdir, 'tempdb3'), dbf_type='vfp', ignore_memos=True)
        table.open(mode=READ_WRITE)
        try:
            self.assertEqual(table[0].wisdom, u'')
        finally:
            table.close()

    def test_clp_ignore_memos(self):
        table = Table(os.path.join(tempdir, 'tempdb3'), u'name C(25); wisdom M', dbf_type='clp').open(mode=READ_WRITE)
        table.append(('QC Tester', 'check it twice!  check it thrice!  check it . . . uh . . . again!'))
        table.close()
        table = Table(os.path.join(tempdir, 'tempdb3'), dbf_type='clp', ignore_memos=True)
        table.open(mode=READ_WRITE)
        try:
            self.assertEqual(table[0].wisdom, u'')
        finally:
            table.close()
