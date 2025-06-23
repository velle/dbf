
class TestChar(TestCase):

    def test_exceptions(self):
        "exceptions"
        self.assertRaises(ValueError, Char, 7)
        self.assertRaises(ValueError, Char, [u'nope'])
        self.assertRaises(ValueError, Char, True)
        self.assertRaises(ValueError, Char, False)
        self.assertRaises(ValueError, Char, type)
        self.assertRaises(ValueError, Char, str)
        self.assertRaises(ValueError, Char, None)

    def test_bools_and_none(self):
        "booleans and None"
        empty = Char()
        self.assertFalse(bool(empty))
        one = Char(u' ')
        self.assertFalse(bool(one))
        actual = Char(u'1')
        self.assertTrue(bool(actual))

    def test_equality(self):
        "equality"
        a1 = Char(u'a')
        a2 = u'a '
        self.assertEqual(a1, a2)
        self.assertEqual(a2, a1)
        a3 = u'a '
        a4 = Char(u'a ')
        self.assertEqual(a3, a4)
        self.assertEqual(a4, a3)

    def test_inequality(self):
        "inequality"
        a1 = Char(u'ab ')
        a2 = u'a b'
        self.assertNotEqual(a1, a2)
        self.assertNotEqual(a2, a1)
        a3 = u'ab '
        a4 = Char(u'a b')
        self.assertNotEqual(a3, a4)
        self.assertNotEqual(a4, a3)

    def test_less_than(self):
        "less-than"
        a1 = Char(u'a')
        a2 = u'a '
        self.assertFalse(a1 < a2)
        self.assertFalse(a2 < a1)
        a3 = u'a '
        a4 = Char(u'a ')
        self.assertFalse(a3 < a4)
        self.assertFalse(a4 < a3)
        a5 = u'abcd'
        a6 = u'abce'
        self.assertTrue(a5 < a6)
        self.assertFalse(a6 < a5)

    def test_less_than_equal(self):
        "less-than or equal"
        a1 = Char(u'a')
        a2 = u'a '
        self.assertTrue(a1 <= a2)
        self.assertTrue(a2 <= a1)
        a3 = u'a '
        a4 = Char(u'a ')
        self.assertTrue(a3 <= a4)
        self.assertTrue(a4 <= a3)
        a5 = u'abcd'
        a6 = u'abce'
        self.assertTrue(a5 <= a6)
        self.assertFalse(a6 <= a5)

    def test_greater_than(self):
        "greater-than or equal"
        a1 = Char(u'a')
        a2 = u'a '
        self.assertTrue(a1 >= a2)
        self.assertTrue(a2 >= a1)
        a3 = u'a '
        a4 = Char(u'a ')
        self.assertTrue(a3 >= a4)
        self.assertTrue(a4 >= a3)
        a5 = u'abcd'
        a6 = u'abce'
        self.assertFalse(a5 >= a6)
        self.assertTrue(a6 >= a5)

    def test_greater_than_equal(self):
        "greater-than"
        a1 = Char(u'a')
        a2 = u'a '
        self.assertFalse(a1 > a2)
        self.assertFalse(a2 > a1)
        a3 = u'a '
        a4 = Char(u'a ')
        self.assertFalse(a3 > a4)
        self.assertFalse(a4 > a3)
        a5 = u'abcd'
        a6 = u'abce'
        self.assertFalse(a5 > a6)
        self.assertTrue(a6 > a5)


class TestDateTime(TestCase):
    "Testing Date"

    def test_date_creation(self):
        "Date creation"
        self.assertEqual(Date(), NullDate)
        self.assertEqual(Date.fromymd('        '), NullDate)
        self.assertEqual(Date.fromymd('00000000'), NullDate)
        self.assertEqual(Date.fromordinal(0), NullDate)
        self.assertEqual(Date.today(), datetime.date.today())
        self.assertEqual(Date.max, datetime.date.max)
        self.assertEqual(Date.min, datetime.date.min)
        self.assertEqual(Date(2018, 5, 21), datetime.date(2018, 5, 21))
        self.assertEqual(Date.strptime('2018-01-01'), datetime.date(2018, 1, 1))
        self.assertRaises(ValueError, Date.fromymd, '00000')
        self.assertRaises(ValueError, Date, 0, 0, 0)

    def test_date_compare(self):
        "Date comparisons"
        nodate1 = Date()
        nodate2 = Date()
        date1 = Date.fromordinal(1000)
        date2 = Date.fromordinal(2000)
        date3 = Date.fromordinal(3000)
        self.compareTimes(nodate1, nodate2, date1, date2, date3)

    def test_datetime_creation(self):
        "DateTime creation"
        self.assertEqual(DateTime(), NullDateTime)
        self.assertEqual(DateTime.fromordinal(0), NullDateTime)
        self.assertTrue(DateTime.today())
        self.assertEqual(DateTime.max, datetime.datetime.max)
        self.assertEqual(DateTime.min, datetime.datetime.min)
        self.assertEqual(DateTime(2018, 5, 21, 19, 17, 16), datetime.datetime(2018, 5, 21, 19, 17 ,16))
        self.assertEqual(DateTime.strptime('2018-01-01 19:17:16'), datetime.datetime(2018, 1, 1, 19, 17, 16))

    def test_datetime_compare(self):
        "DateTime comparisons"
        nodatetime1 = DateTime()
        nodatetime2 = DateTime()
        datetime1 = DateTime.fromordinal(1000)
        datetime2 = DateTime.fromordinal(20000)
        datetime3 = DateTime.fromordinal(300000)
        self.compareTimes(nodatetime1, nodatetime2, datetime1, datetime2, datetime3)

    def test_datetime_replace(self):
        "DateTime replacements"
        datetime_target = DateTime(2001, 5, 31, 23, 59, 59, 999000)
        datetime1 = datetime.datetime(2001, 5, 31, 23, 59, 59, 999230)
        datetime2 = datetime.datetime(2001, 5, 31, 23, 59, 59, 999500)
        datetime3 = datetime.datetime(2001, 5, 31, 23, 59, 59, 999728)
        original_datetime = datetime.datetime
        for dt in (datetime1, datetime2, datetime3):
            class DateTimeNow(datetime.datetime):
                @classmethod
                def now(self):
                    datetime.datetime = original_datetime
                    return dt
            datetime.datetime = DateTimeNow
            result = DateTime.now()
            self.assertEqual(result, datetime_target, 'in: %r  out: %r  desired: %r' % (dt, result, datetime_target))

    def test_time_creation(self):
        "Time creation"
        self.assertEqual(Time(), NullTime)
        self.assertEqual(Time.max, datetime.time.max)
        self.assertEqual(Time.min, datetime.time.min)
        self.assertEqual(Time(19, 17, 16), datetime.time(19, 17 ,16))
        self.assertEqual(Time.strptime('19:17:16'), datetime.time(19, 17, 16))

    def test_time_compare(self):
        "Time comparisons"
        notime1 = Time()
        notime2 = Time()
        time1 = Time.fromfloat(7.75)
        time2 = Time.fromfloat(9.5)
        time3 = Time.fromfloat(16.25)
        self.compareTimes(notime1, notime2, time1, time2, time3)

    @unittest.skipIf(pytz is None, 'pytz not installed')
    def test_datetime_tz(self):
        "DateTime with Time Zones"
        pst = pytz.timezone('America/Los_Angeles')
        mst = pytz.timezone('America/Boise')
        cst = pytz.timezone('America/Chicago')
        est = pytz.timezone('America/New_York')
        utc = pytz.timezone('UTC')
        #
        pdt = DateTime(2018, 5, 20, 5, 41, 33, tzinfo=pst)
        mdt = DateTime(2018, 5, 20, 6, 41, 33, tzinfo=mst)
        cdt = DateTime(2018, 5, 20, 7, 41, 33, tzinfo=cst)
        edt = DateTime(2018, 5, 20, 8, 41, 33, tzinfo=est)
        udt = DateTime(2018, 5, 20, 12, 41, 33, tzinfo=utc)
        self.assertTrue(pdt == mdt == cdt == edt == udt)
        #
        dup1 = DateTime.combine(pdt.date(), mdt.timetz())
        dup2 = DateTime.combine(cdt.date(), Time(5, 41, 33, tzinfo=pst))
        self.assertTrue(dup1 == dup2 == udt)
        #
        udt2 = DateTime(2018, 5, 20, 13, 41, 33, tzinfo=utc)
        mdt2 = mdt.replace(tzinfo=pst)
        self.assertTrue(mdt2 == udt2)
        #
        with self.assertRaisesRegex(ValueError, 'not naive datetime'):
            DateTime(pdt, tzinfo=mst)
        with self.assertRaisesRegex(ValueError, 'not naive datetime'):
            DateTime(datetime.datetime(2018, 5, 27, 15, 57, 11, tzinfo=pst), tzinfo=pst)
        with self.assertRaisesRegex(ValueError, 'not naive time'):
            Time(pdt.timetz(), tzinfo=mst)
        with self.assertRaisesRegex(ValueError, 'not naive time'):
            Time(datetime.time(15, 58, 59, tzinfo=mst), tzinfo=mst)
        #
        if py_ver < (3, 0):
            from xmlrpclib import Marshaller, loads
        else:
            from xmlrpc.client import Marshaller, loads
        self.assertEqual(
                udt.utctimetuple(),
                loads(Marshaller().dumps([pdt]), use_datetime=True)[0][0].utctimetuple(),
                )
        #
        self.assertEqual(
                pdt,
                DateTime.combine(Date(2018, 5, 20), Time(5, 41, 33), tzinfo=pst),
                )

    def test_arithmetic(self):
        "Date, DateTime, & Time Arithmetic"
        one_day = datetime.timedelta(1)
        a_day = Date(1970, 5, 20)
        self.assertEqual(a_day + one_day, Date(1970, 5, 21))
        self.assertEqual(a_day - one_day, Date(1970, 5, 19))
        self.assertEqual(datetime.date(1970, 5, 21) - a_day, one_day)
        a_time = Time(12)
        one_second = datetime.timedelta(0, 1, 0)
        self.assertEqual(a_time + one_second, Time(12, 0, 1))
        self.assertEqual(a_time - one_second, Time(11, 59, 59))
        self.assertEqual(datetime.time(12, 0, 1) - a_time, one_second)
        an_appt = DateTime(2012, 4, 15, 12, 30, 00)
        displacement = datetime.timedelta(1, 60*60*2+60*15)
        self.assertEqual(an_appt + displacement, DateTime(2012, 4, 16, 14, 45, 0))
        self.assertEqual(an_appt - displacement, DateTime(2012, 4, 14, 10, 15, 0))
        self.assertEqual(datetime.datetime(2012, 4, 16, 14, 45, 0) - an_appt, displacement)

    def test_none_compare(self):
        "comparisons to None"
        empty_date = Date()
        empty_time = Time()
        empty_datetime = DateTime()
        self.assertEqual(empty_date, None)
        self.assertEqual(empty_time, None)
        self.assertEqual(empty_datetime, None)

    def test_singletons(self):
        "singletons"
        empty_date = Date()
        empty_time = Time()
        empty_datetime = DateTime()
        self.assertTrue(empty_date is NullDate)
        self.assertTrue(empty_time is NullTime)
        self.assertTrue(empty_datetime is NullDateTime)

    def test_boolean_value(self):
        "boolean evaluation"
        empty_date = Date()
        empty_time = Time()
        empty_datetime = DateTime()
        self.assertEqual(bool(empty_date), False)
        self.assertEqual(bool(empty_time), False)
        self.assertEqual(bool(empty_datetime), False)
        actual_date = Date.today()
        actual_time = Time.now()
        actual_datetime = DateTime.now()
        self.assertEqual(bool(actual_date), True)
        self.assertEqual(bool(actual_time), True)
        self.assertEqual(bool(actual_datetime), True)

    def compareTimes(self, empty1, empty2, uno, dos, tres):
        self.assertTrue(empty1 is empty2)
        self.assertTrue(empty1 < uno, '%r is not less than %r' % (empty1, uno))
        self.assertFalse(empty1 > uno, '%r is less than %r' % (empty1, uno))
        self.assertTrue(uno > empty1, '%r is not greater than %r' % (empty1, uno))
        self.assertFalse(uno < empty1, '%r is greater than %r' % (empty1, uno))
        self.assertEqual(uno < dos, True)
        self.assertEqual(uno <= dos, True)
        self.assertEqual(dos <= dos, True)
        self.assertEqual(dos <= tres, True)
        self.assertEqual(dos < tres, True)
        self.assertEqual(tres <= tres, True)
        self.assertEqual(uno == uno, True)
        self.assertEqual(dos == dos, True)
        self.assertEqual(tres == tres, True)
        self.assertEqual(uno != dos, True)
        self.assertEqual(dos != tres, True)
        self.assertEqual(tres != uno, True)
        self.assertEqual(tres >= tres, True)
        self.assertEqual(tres > dos, True)
        self.assertEqual(dos >= dos, True)
        self.assertEqual(dos >= uno, True)
        self.assertEqual(dos > uno, True)
        self.assertEqual(uno >= uno, True)
        self.assertEqual(uno >= dos, False)
        self.assertEqual(uno >= tres, False)
        self.assertEqual(dos >= tres, False)
        self.assertEqual(tres <= dos, False)
        self.assertEqual(tres <= uno, False)
        self.assertEqual(tres < tres, False)
        self.assertEqual(tres < dos, False)
        self.assertEqual(tres < uno, False)
        self.assertEqual(dos < dos, False)
        self.assertEqual(dos < uno, False)
        self.assertEqual(uno < uno, False)
        self.assertEqual(uno == dos, False)
        self.assertEqual(uno == tres, False)
        self.assertEqual(dos == uno, False)
        self.assertEqual(dos == tres, False)
        self.assertEqual(tres == uno, False)
        self.assertEqual(tres == dos, False)
        self.assertEqual(uno != uno, False)
        self.assertEqual(dos != dos, False)
        self.assertEqual(tres != tres, False)


class TestNull(TestCase):

    def test_all(self):
        NULL = Null = dbf.Null()
        self.assertTrue(NULL is dbf.Null())

        self.assertTrue(NULL + 1 is Null)
        self.assertTrue(1 + NULL is Null)
        NULL += 4
        self.assertTrue(NULL is Null)
        value = 5
        value += NULL
        self.assertTrue(value is Null)

        self.assertTrue(NULL - 2 is Null)
        self.assertTrue(2 - NULL is Null)
        NULL -= 5
        self.assertTrue(NULL is Null)
        value = 6
        value -= NULL
        self.assertTrue(value is Null)

        self.assertTrue(NULL / 0 is Null)
        self.assertTrue(3 / NULL is Null)
        NULL /= 6
        self.assertTrue(NULL is Null)
        value = 7
        value /= NULL
        self.assertTrue(value is Null)

        self.assertTrue(NULL * -3 is Null)
        self.assertTrue(4 * NULL is Null)
        NULL *= 7
        self.assertTrue(NULL is Null)
        value = 8
        value *= NULL
        self.assertTrue(value is Null)

        self.assertTrue(NULL % 1 is Null)
        self.assertTrue(7 % NULL is Null)
        NULL %= 1
        self.assertTrue(NULL is Null)
        value = 9
        value %= NULL
        self.assertTrue(value is Null)

        self.assertTrue(NULL ** 2 is Null)
        self.assertTrue(4 ** NULL is Null)
        NULL **= 3
        self.assertTrue(NULL is Null)
        value = 9
        value **= NULL
        self.assertTrue(value is Null)

        self.assertTrue(NULL & 1 is Null)
        self.assertTrue(1 & NULL is Null)
        NULL &= 1
        self.assertTrue(NULL is Null)
        value = 1
        value &= NULL
        self.assertTrue(value is Null)

        self.assertTrue(NULL ^ 1 is Null)
        self.assertTrue(1 ^ NULL is Null)
        NULL ^= 1
        self.assertTrue(NULL is Null)
        value = 1
        value ^= NULL
        self.assertTrue(value is Null)

        self.assertTrue(NULL | 1 is Null)
        self.assertTrue(1 | NULL is Null)
        NULL |= 1
        self.assertTrue(NULL is Null)
        value = 1
        value |= NULL
        self.assertTrue(value is Null)

        self.assertTrue(str(divmod(NULL, 1)) == '(<null>, <null>)')
        self.assertTrue(str(divmod(1, NULL)) == '(<null>, <null>)')

        self.assertTrue(NULL << 1 is Null)
        self.assertTrue(2 << NULL is Null)
        NULL <<=3
        self.assertTrue(NULL is Null)
        value = 9
        value <<= NULL
        self.assertTrue(value is Null)

        self.assertTrue(NULL >> 1 is Null)
        self.assertTrue(2 >> NULL is Null)
        NULL >>= 3
        self.assertTrue(NULL is Null)
        value = 9
        value >>= NULL
        self.assertTrue(value is Null)

        self.assertTrue(-NULL is Null)
        self.assertTrue(+NULL is Null)
        self.assertTrue(abs(NULL) is Null)
        self.assertTrue(~NULL is Null)

        self.assertTrue(NULL.attr is Null)
        self.assertTrue(NULL() is Null)
        self.assertTrue(getattr(NULL, 'fake') is Null)

        self.assertRaises(TypeError, hash, NULL)

class TestLogical(TestCase):
    "Testing Logical"

    def test_unknown(self):
        "Unknown"
        for unk in '', '?', ' ', None, Null, Unknown, Other:
            huh = Logical(unk)
            self.assertEqual(huh == None, True, "huh is %r from %r, which is not None" % (huh, unk))
            self.assertEqual(huh != None, False, "huh is %r from %r, which is not None" % (huh, unk))
            self.assertEqual(huh != True, True, "huh is %r from %r, which is not None" % (huh, unk))
            self.assertEqual(huh == True, False, "huh is %r from %r, which is not None" % (huh, unk))
            self.assertEqual(huh != False, True, "huh is %r from %r, which is not None" % (huh, unk))
            self.assertEqual(huh == False, False, "huh is %r from %r, which is not None" % (huh, unk))
            self.assertRaises(ValueError, lambda : (0, 1, 2)[huh])

    def test_true(self):
        "true"
        for true in 'True', 'yes', 't', 'Y', 7, ['blah']:
            huh = Logical(true)
            self.assertEqual(huh == True, True)
            self.assertEqual(huh != True, False)
            self.assertEqual(huh == False, False, "%r is not True" % true)
            self.assertEqual(huh != False, True)
            self.assertEqual(huh == None, False)
            self.assertEqual(huh != None, True)
            self.assertEqual((0, 1, 2)[huh], 1)

    def test_false(self):
        "false"
        for false in 'false', 'No', 'F', 'n', 0, []:
            huh = Logical(false)
            self.assertEqual(huh != False, False)
            self.assertEqual(huh == False, True)
            self.assertEqual(huh != True, True)
            self.assertEqual(huh == True, False)
            self.assertEqual(huh != None, True)
            self.assertEqual(huh == None, False)
            self.assertEqual((0, 1, 2)[huh], 0)

    def test_singletons(self):
        "singletons"
        heh = Logical(True)
        hah = Logical('Yes')
        ick = Logical(False)
        ack = Logical([])
        unk = Logical('?')
        bla = Logical(None)
        self.assertEqual(heh is hah, True)
        self.assertEqual(ick is ack, True)
        self.assertEqual(unk is bla, True)

    def test_error(self):
        "errors"
        self.assertRaises(ValueError, Logical, 'wrong')

    def test_and(self):
        "and"
        true = Logical(True)
        false = Logical(False)
        unknown = Logical(None)
        self.assertEqual((true & true) is true, True)
        self.assertEqual((true & false) is false, True)
        self.assertEqual((false & true) is false, True)
        self.assertEqual((false & false) is false, True)
        self.assertEqual((true & unknown) is unknown, True)
        self.assertEqual((false & unknown) is false, True)
        self.assertEqual((unknown & true) is unknown, True)
        self.assertEqual((unknown & false) is false, True)
        self.assertEqual((unknown & unknown) is unknown, True)
        self.assertEqual((true & True) is true, True)
        self.assertEqual((true & False) is false, True)
        self.assertEqual((false & True) is false, True)
        self.assertEqual((false & False) is false, True)
        self.assertEqual((true & None) is unknown, True)
        self.assertEqual((false & None) is false, True)
        self.assertEqual((unknown & True) is unknown, True)
        self.assertEqual((unknown & False) is false, True)
        self.assertEqual((unknown & None) is unknown, True)
        self.assertEqual((True & true) is true, True)
        self.assertEqual((True & false) is false, True)
        self.assertEqual((False & true) is false, True)
        self.assertEqual((False & false) is false, True)
        self.assertEqual((True & unknown) is unknown, True)
        self.assertEqual((False & unknown) is false, True)
        self.assertEqual((None & true) is unknown, True)
        self.assertEqual((None & false) is false, True)
        self.assertEqual((None & unknown) is unknown, True)
        self.assertEqual(type(true & 0), int)
        self.assertEqual(true & 0, 0)
        self.assertEqual(type(true & 3), int)
        self.assertEqual(true & 3, 1)
        self.assertEqual(type(false & 0), int)
        self.assertEqual(false & 0, 0)
        self.assertEqual(type(false & 2), int)
        self.assertEqual(false & 2, 0)
        self.assertEqual(type(unknown & 0), int)
        self.assertEqual(unknown & 0, 0)
        self.assertEqual(unknown & 2, unknown)

        t = true
        t &= true
        self.assertEqual(t is true, True)
        t = true
        t &= false
        self.assertEqual(t is false, True)
        f = false
        f &= true
        self.assertEqual(f is false, True)
        f = false
        f &= false
        self.assertEqual(f is false, True)
        t = true
        t &= unknown
        self.assertEqual(t is unknown, True)
        f = false
        f &= unknown
        self.assertEqual(f is false, True)
        u = unknown
        u &= true
        self.assertEqual(u is unknown, True)
        u = unknown
        u &= false
        self.assertEqual(u is false, True)
        u = unknown
        u &= unknown
        self.assertEqual(u is unknown, True)
        t = true
        t &= True
        self.assertEqual(t is true, True)
        t = true
        t &= False
        self.assertEqual(t is false, True)
        f = false
        f &= True
        self.assertEqual(f is false, True)
        f = false
        f &= False
        self.assertEqual(f is false, True)
        t = true
        t &= None
        self.assertEqual(t is unknown, True)
        f = false
        f &= None
        self.assertEqual(f is false, True)
        u = unknown
        u &= True
        self.assertEqual(u is unknown, True)
        u = unknown
        u &= False
        self.assertEqual(u is false, True)
        u = unknown
        u &= None
        self.assertEqual(u is unknown, True)
        t = True
        t &= true
        self.assertEqual(t is true, True)
        t = True
        t &= false
        self.assertEqual(t is false, True)
        f = False
        f &= true
        self.assertEqual(f is false, True)
        f = False
        f &= false
        self.assertEqual(f is false, True)
        t = True
        t &= unknown
        self.assertEqual(t is unknown, True)
        f = False
        f &= unknown
        self.assertEqual(f is false, True)
        u = None
        u &= true
        self.assertEqual(u is unknown, True)
        u = None
        u &= false
        self.assertEqual(u is false, True)
        u = None
        u &= unknown
        self.assertEqual(u is unknown, True)
        t = true
        t &= 0
        self.assertEqual(type(true & 0), int)
        t = true
        t &= 0
        self.assertEqual(true & 0, 0)
        t = true
        t &= 3
        self.assertEqual(type(true & 3), int)
        t = true
        t &= 3
        self.assertEqual(true & 3, 1)
        f = false
        f &= 0
        self.assertEqual(type(false & 0), int)
        f = false
        f &= 0
        self.assertEqual(false & 0, 0)
        f = false
        f &= 2
        self.assertEqual(type(false & 2), int)
        f = false
        f &= 2
        self.assertEqual(false & 2, 0)
        u = unknown
        u &= 0
        self.assertEqual(type(unknown & 0), int)
        u = unknown
        u &= 0
        self.assertEqual(unknown & 0, 0)
        u = unknown
        u &= 2
        self.assertEqual(unknown & 2, unknown)

    def test_or(self):
        "or"
        true = Logical(True)
        false = Logical(False)
        unknown = Logical(None)
        self.assertEqual((true | true) is true, True)
        self.assertEqual((true | false) is true, True)
        self.assertEqual((false | true) is true, True)
        self.assertEqual((false | false) is false, True)
        self.assertEqual((true | unknown) is true, True)
        self.assertEqual((false | unknown) is unknown, True)
        self.assertEqual((unknown | true) is true, True)
        self.assertEqual((unknown | false) is unknown, True)
        self.assertEqual((unknown | unknown) is unknown, True)
        self.assertEqual((true | True) is true, True)
        self.assertEqual((true | False) is true, True)
        self.assertEqual((false | True) is true, True)
        self.assertEqual((false | False) is false, True)
        self.assertEqual((true | None) is true, True)
        self.assertEqual((false | None) is unknown, True)
        self.assertEqual((unknown | True) is true, True)
        self.assertEqual((unknown | False) is unknown, True)
        self.assertEqual((unknown | None) is unknown, True)
        self.assertEqual((True | true) is true, True)
        self.assertEqual((True | false) is true, True)
        self.assertEqual((False | true) is true, True)
        self.assertEqual((False | false) is false, True)
        self.assertEqual((True | unknown) is true, True)
        self.assertEqual((False | unknown) is unknown, True)
        self.assertEqual((None | true) is true, True)
        self.assertEqual((None | false) is unknown, True)
        self.assertEqual((None | unknown) is unknown, True)
        self.assertEqual(type(true | 0), int)
        self.assertEqual(true | 0, 1)
        self.assertEqual(type(true | 2), int)
        self.assertEqual(true | 2, 3)
        self.assertEqual(type(false | 0), int)
        self.assertEqual(false | 0, 0)
        self.assertEqual(type(false | 2), int)
        self.assertEqual(false | 2, 2)
        self.assertEqual(unknown | 0, unknown)
        self.assertEqual(unknown | 2, unknown)

        t = true
        t |= true
        self.assertEqual(t is true, True)
        t = true
        t |= false
        self.assertEqual(t is true, True)
        f = false
        f |= true
        self.assertEqual(f is true, True)
        f = false
        f |= false
        self.assertEqual(f is false, True)
        t = true
        t |= unknown
        self.assertEqual(t is true, True)
        f = false
        f |= unknown
        self.assertEqual(f is unknown, True)
        u = unknown
        u |= true
        self.assertEqual(u is true, True)
        u = unknown
        u |= false
        self.assertEqual(u is unknown, True)
        u = unknown
        u |= unknown
        self.assertEqual(u is unknown, True)
        t = true
        t |= True
        self.assertEqual(t is true, True)
        t = true
        t |= False
        self.assertEqual(t is true, True)
        f = false
        f |= True
        self.assertEqual(f is true, True)
        f = false
        f |= False
        self.assertEqual(f is false, True)
        t = true
        t |= None
        self.assertEqual(t is true, True)
        f = false
        f |= None
        self.assertEqual(f is unknown, True)
        u = unknown
        u |= True
        self.assertEqual(u is true, True)
        u = unknown
        u |= False
        self.assertEqual(u is unknown, True)
        u = unknown
        u |= None
        self.assertEqual(u is unknown, True)
        t = True
        t |= true
        self.assertEqual(t is true, True)
        t = True
        t |= false
        self.assertEqual(t is true, True)
        f = False
        f |= true
        self.assertEqual(f is true, True)
        f = False
        f |= false
        self.assertEqual(f is false, True)
        t = True
        t |= unknown
        self.assertEqual(t is true, True)
        f = False
        f |= unknown
        self.assertEqual(f is unknown, True)
        u = None
        u |= true
        self.assertEqual(u is true, True)
        u = None
        u |= false
        self.assertEqual(u is unknown, True)
        u = None
        u |= unknown
        self.assertEqual(u is unknown, True)
        t = true
        t |= 0
        self.assertEqual(type(t), int)
        t = true
        t |= 0
        self.assertEqual(t, 1)
        t = true
        t |= 2
        self.assertEqual(type(t), int)
        t = true
        t |= 2
        self.assertEqual(t, 3)
        f = false
        f |= 0
        self.assertEqual(type(f), int)
        f = false
        f |= 0
        self.assertEqual(f, 0)
        f = false
        f |= 2
        self.assertEqual(type(f), int)
        f = false
        f |= 2
        self.assertEqual(f, 2)
        u = unknown
        u |= 0
        self.assertEqual(u, unknown)

    def test_xor(self):
        "xor"
        true = Logical(True)
        false = Logical(False)
        unknown = Logical(None)
        self.assertEqual((true ^ true) is false, True)
        self.assertEqual((true ^ false) is true, True)
        self.assertEqual((false ^ true) is true, True)
        self.assertEqual((false ^ false) is false, True)
        self.assertEqual((true ^ unknown) is unknown, True)
        self.assertEqual((false ^ unknown) is unknown, True)
        self.assertEqual((unknown ^ true) is unknown, True)
        self.assertEqual((unknown ^ false) is unknown, True)
        self.assertEqual((unknown ^ unknown) is unknown, True)
        self.assertEqual((true ^ True) is false, True)
        self.assertEqual((true ^ False) is true, True)
        self.assertEqual((false ^ True) is true, True)
        self.assertEqual((false ^ False) is false, True)
        self.assertEqual((true ^ None) is unknown, True)
        self.assertEqual((false ^ None) is unknown, True)
        self.assertEqual((unknown ^ True) is unknown, True)
        self.assertEqual((unknown ^ False) is unknown, True)
        self.assertEqual((unknown ^ None) is unknown, True)
        self.assertEqual((True ^ true) is false, True)
        self.assertEqual((True ^ false) is true, True)
        self.assertEqual((False ^ true) is true, True)
        self.assertEqual((False ^ false) is false, True)
        self.assertEqual((True ^ unknown) is unknown, True)
        self.assertEqual((False ^ unknown) is unknown, True)
        self.assertEqual((None ^ true) is unknown, True)
        self.assertEqual((None ^ false) is unknown, True)
        self.assertEqual((None ^ unknown) is unknown, True)
        self.assertEqual(type(true ^ 2), int)
        self.assertEqual(true ^ 2, 3)
        self.assertEqual(type(true ^ 0), int)
        self.assertEqual(true ^ 0, 1)
        self.assertEqual(type(false ^ 0), int)
        self.assertEqual(false ^ 0, 0)
        self.assertEqual(type(false ^ 2), int)
        self.assertEqual(false ^ 2, 2)
        self.assertEqual(unknown ^ 0, unknown)
        self.assertEqual(unknown ^ 2, unknown)

        t = true
        t ^= true
        self.assertEqual(t is false, True)
        t = true
        t ^= false
        self.assertEqual(t is true, True)
        f = false
        f ^= true
        self.assertEqual(f is true, True)
        f = false
        f ^= false
        self.assertEqual(f is false, True)
        t = true
        t ^= unknown
        self.assertEqual(t is unknown, True)
        f = false
        f ^= unknown
        self.assertEqual(f is unknown, True)
        u = unknown
        u ^= true
        self.assertEqual(u is unknown, True)
        u = unknown
        u ^= false
        self.assertEqual(u is unknown, True)
        u = unknown
        u ^= unknown
        self.assertEqual(u is unknown, True)
        t = true
        t ^= True
        self.assertEqual(t is false, True)
        t = true
        t ^= False
        self.assertEqual(t is true, True)
        f = false
        f ^= True
        self.assertEqual(f is true, True)
        f = false
        f ^= False
        self.assertEqual(f is false, True)
        t = true
        t ^= None
        self.assertEqual(t is unknown, True)
        f = false
        f ^= None
        self.assertEqual(f is unknown, True)
        u = unknown
        u ^= True
        self.assertEqual(u is unknown, True)
        u = unknown
        u ^= False
        self.assertEqual(u is unknown, True)
        u = unknown
        u ^= None
        self.assertEqual(u is unknown, True)
        t = True
        t ^= true
        self.assertEqual(t is false, True)
        t = True
        t ^= false
        self.assertEqual(t is true, True)
        f = False
        f ^= true
        self.assertEqual(f is true, True)
        f = False
        f ^= false
        self.assertEqual(f is false, True)
        t = True
        t ^= unknown
        self.assertEqual(t is unknown, True)
        f = False
        f ^= unknown
        self.assertEqual(f is unknown, True)
        u = None
        u ^= true
        self.assertEqual(u is unknown, True)
        u = None
        u ^= false
        self.assertEqual(u is unknown, True)
        u = None
        u ^= unknown
        self.assertEqual(u is unknown, True)
        t = true
        t ^= 0
        self.assertEqual(type(true ^ 0), int)
        t = true
        t ^= 0
        self.assertEqual(true ^ 0, 1)
        t = true
        t ^= 2
        self.assertEqual(type(true ^ 2), int)
        t = true
        t ^= 2
        self.assertEqual(true ^ 2, 3)
        f = false
        f ^= 0
        self.assertEqual(type(false ^ 0), int)
        f = false
        f ^= 0
        self.assertEqual(false ^ 0, 0)
        f = false
        f ^= 2
        self.assertEqual(type(false ^ 2), int)
        f = false
        f ^= 2
        self.assertEqual(false ^ 2, 2)
        u = unknown
        u ^= 0
        self.assertEqual(unknown ^ 0, unknown)
        u = unknown
        u ^= 2
        self.assertEqual(unknown ^ 2, unknown)

    def test_negation(self):
        "negation"
        true = Logical(True)
        false = Logical(False)
        none = Logical(None)
        self.assertEqual(-true, -1)
        self.assertEqual(-false, 0)
        self.assertEqual(-none, none)

    def test_posation(self):
        "posation"
        true = Logical(True)
        false = Logical(False)
        none = Logical(None)
        self.assertEqual(+true, 1)
        self.assertEqual(+false, 0)
        self.assertEqual(+none, none)

    def test_abs(self):
        "abs()"
        true = Logical(True)
        false = Logical(False)
        none = Logical(None)
        self.assertEqual(abs(true), 1)
        self.assertEqual(abs(false), 0)
        self.assertEqual(abs(none), none)

    def test_invert(self):
        "~ operator"
        true = Logical(True)
        false = Logical(False)
        none = Logical(None)
        self.assertEqual(~true, false)
        self.assertEqual(~false, true)
        self.assertEqual(~none, none)

    def test_complex(self):
        "complex"
        true = Logical(True)
        false = Logical(False)
        none = Logical(None)
        self.assertEqual(complex(true), complex(1))
        self.assertEqual(complex(false), complex(0))
        self.assertRaises(ValueError, complex, none)

    def test_int(self):
        "int"
        true = Logical(True)
        false = Logical(False)
        none = Logical(None)
        self.assertEqual(int(true), 1)
        self.assertEqual(int(false), 0)
        self.assertRaises(ValueError, int, none)

    if py_ver < (3, 0):
        def test_long(self):
            "long"
            true = Logical(True)
            false = Logical(False)
            none = Logical(None)
            self.assertEqual(long(true), long(1))
            self.assertEqual(long(false), long(0))
            self.assertRaises(ValueError, long, none)

    def test_float(self):
        "float"
        true = Logical(True)
        false = Logical(False)
        none = Logical(None)
        self.assertEqual(float(true), 1.0)
        self.assertEqual(float(false), 0.0)
        self.assertRaises(ValueError, float, none)

    def test_oct(self):
        "oct"
        true = Logical(True)
        false = Logical(False)
        none = Logical(None)
        self.assertEqual(oct(true), oct(1))
        self.assertEqual(oct(false), oct(0))
        self.assertRaises(ValueError, oct, none)

    def test_hex(self):
        "hex"
        true = Logical(True)
        false = Logical(False)
        none = Logical(None)
        self.assertEqual(hex(true), hex(1))
        self.assertEqual(hex(false), hex(0))
        self.assertRaises(ValueError, hex, none)

    def test_addition(self):
        "addition"
        true = Logical(True)
        false = Logical(False)
        unknown = Logical(None)
        self.assertEqual(true + true, 2)
        self.assertEqual(true + false, 1)
        self.assertEqual(false + true, 1)
        self.assertEqual(false + false, 0)
        self.assertEqual(true + unknown, unknown)
        self.assertEqual(false + unknown, unknown)
        self.assertEqual(unknown + true, unknown)
        self.assertEqual(unknown + false, unknown)
        self.assertEqual(unknown + unknown, unknown)
        self.assertEqual(true + True, 2)
        self.assertEqual(true + False, 1)
        self.assertEqual(false + True, 1)
        self.assertEqual(false + False, 0)
        self.assertEqual(true + None, unknown)
        self.assertEqual(false + None, unknown)
        self.assertEqual(unknown + True, unknown)
        self.assertEqual(unknown + False, unknown)
        self.assertEqual(unknown + None, unknown)
        self.assertEqual(True + true, 2)
        self.assertEqual(True + false, 1)
        self.assertEqual(False + true, 1)
        self.assertEqual(False + false, 0)
        self.assertEqual(True + unknown, unknown)
        self.assertEqual(False + unknown, unknown)
        self.assertEqual(None + true, unknown)
        self.assertEqual(None + false, unknown)
        self.assertEqual(None + unknown, unknown)

        t = true
        t += true
        self.assertEqual(t, 2)
        t = true
        t += false
        self.assertEqual(t, 1)
        f = false
        f += true
        self.assertEqual(f, 1)
        f = false
        f += false
        self.assertEqual(f, 0)
        t = true
        t += unknown
        self.assertEqual(t, unknown)
        f = false
        f += unknown
        self.assertEqual(f, unknown)
        u = unknown
        u += true
        self.assertEqual(u, unknown)
        u = unknown
        u += false
        self.assertEqual(u, unknown)
        u = unknown
        u += unknown
        self.assertEqual(u, unknown)
        t = true
        t += True
        self.assertEqual(t, 2)
        t = true
        t += False
        self.assertEqual(t, 1)
        f = false
        f += True
        self.assertEqual(f, 1)
        f = false
        f += False
        self.assertEqual(f, 0)
        t = true
        t += None
        self.assertEqual(t, unknown)
        f = false
        f += None
        self.assertEqual(f, unknown)
        u = unknown
        u += True
        self.assertEqual(u, unknown)
        u = unknown
        u += False
        self.assertEqual(u, unknown)
        u = unknown
        u += None
        self.assertEqual(u, unknown)
        t = True
        t += true
        self.assertEqual(t, 2)
        t = True
        t += false
        self.assertEqual(t, 1)
        f = False
        f += true
        self.assertEqual(f, 1)
        f = False
        f += false
        self.assertEqual(f, 0)
        t = True
        t += unknown
        self.assertEqual(t, unknown)
        f = False
        f += unknown
        self.assertEqual(f, unknown)
        u = None
        u += true
        self.assertEqual(u, unknown)
        u = None
        u += false
        self.assertEqual(u, unknown)
        u = None
        u += unknown
        self.assertEqual(u, unknown)

    def test_multiplication(self):
        "multiplication"
        true = Logical(True)
        false = Logical(False)
        unknown = Logical(None)
        self.assertEqual(true * true, 1)
        self.assertEqual(true * false, 0)
        self.assertEqual(false * true, 0)
        self.assertEqual(false * false, 0)
        self.assertEqual(true * unknown, unknown)
        self.assertEqual(false * unknown, 0)
        self.assertEqual(unknown * true, unknown)
        self.assertEqual(unknown * false, 0)
        self.assertEqual(unknown * unknown, unknown)
        self.assertEqual(true * True, 1)
        self.assertEqual(true * False, 0)
        self.assertEqual(false * True, 0)
        self.assertEqual(false * False, 0)
        self.assertEqual(true * None, unknown)
        self.assertEqual(false * None, 0)
        self.assertEqual(unknown * True, unknown)
        self.assertEqual(unknown * False, 0)
        self.assertEqual(unknown * None, unknown)
        self.assertEqual(True * true, 1)
        self.assertEqual(True * false, 0)
        self.assertEqual(False * true, 0)
        self.assertEqual(False * false, 0)
        self.assertEqual(True * unknown, unknown)
        self.assertEqual(False * unknown, 0)
        self.assertEqual(None * true, unknown)
        self.assertEqual(None * false, 0)
        self.assertEqual(None * unknown, unknown)

        t = true
        t *= true
        self.assertEqual(t, 1)
        t = true
        t *= false
        self.assertEqual(t, 0)
        f = false
        f *= true
        self.assertEqual(f, 0)
        f = false
        f *= false
        self.assertEqual(f, 0)
        t = true
        t *= unknown
        self.assertEqual(t, unknown)
        f = false
        f *= unknown
        self.assertEqual(f, 0)
        u = unknown
        u *= true
        self.assertEqual(u, unknown)
        u = unknown
        u *= false
        self.assertEqual(u, 0)
        u = unknown
        u *= unknown
        self.assertEqual(u, unknown)
        t = true
        t *= True
        self.assertEqual(t, 1)
        t = true
        t *= False
        self.assertEqual(t, 0)
        f = false
        f *= True
        self.assertEqual(f, 0)
        f = false
        f *= False
        self.assertEqual(f, 0)
        t = true
        t *= None
        self.assertEqual(t, unknown)
        f = false
        f *= None
        self.assertEqual(f, 0)
        u = unknown
        u *= True
        self.assertEqual(u, unknown)
        u = unknown
        u *= False
        self.assertEqual(u, 0)
        u = unknown
        u *= None
        self.assertEqual(u, unknown)
        t = True
        t *= true
        self.assertEqual(t, 1)
        t = True
        t *= false
        self.assertEqual(t, 0)
        f = False
        f *= true
        self.assertEqual(f, 0)
        f = False
        f *= false
        self.assertEqual(f, 0)
        t = True
        t *= unknown
        self.assertEqual(t, unknown)
        f = False
        f *= unknown
        self.assertEqual(f, 0)
        u = None
        u *= true
        self.assertEqual(u, unknown)
        u = None
        u *= false
        self.assertEqual(u, 0)
        u = None
        u *= unknown
        self.assertEqual(u, unknown)

    def test_subtraction(self):
        "subtraction"
        true = Logical(True)
        false = Logical(False)
        unknown = Logical(None)
        self.assertEqual(true - true, 0)
        self.assertEqual(true - false, 1)
        self.assertEqual(false - true, -1)
        self.assertEqual(false - false, 0)
        self.assertEqual(true - unknown, unknown)
        self.assertEqual(false - unknown, unknown)
        self.assertEqual(unknown - true, unknown)
        self.assertEqual(unknown - false, unknown)
        self.assertEqual(unknown - unknown, unknown)
        self.assertEqual(true - True, 0)
        self.assertEqual(true - False, 1)
        self.assertEqual(false - True, -1)
        self.assertEqual(false - False, 0)
        self.assertEqual(true - None, unknown)
        self.assertEqual(false - None, unknown)
        self.assertEqual(unknown - True, unknown)
        self.assertEqual(unknown - False, unknown)
        self.assertEqual(unknown - None, unknown)
        self.assertEqual(True - true, 0)
        self.assertEqual(True - false, 1)
        self.assertEqual(False - true, -1)
        self.assertEqual(False - false, 0)
        self.assertEqual(True - unknown, unknown)
        self.assertEqual(False - unknown, unknown)
        self.assertEqual(None - true, unknown)
        self.assertEqual(None - false, unknown)
        self.assertEqual(None - unknown, unknown)

        t = true
        t -= true
        self.assertEqual(t, 0)
        t = true
        t -= false
        self.assertEqual(t, 1)
        f = false
        f -= true
        self.assertEqual(f, -1)
        f = false
        f -= false
        self.assertEqual(f, 0)
        t = true
        t -= unknown
        self.assertEqual(t, unknown)
        f = false
        f -= unknown
        self.assertEqual(f, unknown)
        u = unknown
        u -= true
        self.assertEqual(u, unknown)
        u = unknown
        u -= false
        self.assertEqual(u, unknown)
        u = unknown
        u -= unknown
        self.assertEqual(u, unknown)
        t = true
        t -= True
        self.assertEqual(t, 0)
        t = true
        t -= False
        self.assertEqual(t, 1)
        f = false
        f -= True
        self.assertEqual(f, -1)
        f = false
        f -= False
        self.assertEqual(f, 0)
        t = true
        t -= None
        self.assertEqual(t, unknown)
        f = false
        f -= None
        self.assertEqual(f, unknown)
        u = unknown
        u -= True
        self.assertEqual(u, unknown)
        u = unknown
        u -= False
        self.assertEqual(u, unknown)
        u = unknown
        u -= None
        self.assertEqual(u, unknown)
        t = True
        t -= true
        self.assertEqual(t, 0)
        t = True
        t -= false
        self.assertEqual(t, 1)
        f = False
        f -= true
        self.assertEqual(f, -1)
        f = False
        f -= false
        self.assertEqual(f, 0)
        t = True
        t -= unknown
        self.assertEqual(t, unknown)
        f = False
        f -= unknown
        self.assertEqual(f, unknown)
        u = None
        u -= true
        self.assertEqual(u, unknown)
        u = None
        u -= false
        self.assertEqual(u, unknown)
        u = None
        u -= unknown
        self.assertEqual(u, unknown)

    def test_division(self):
        "division"
        true = Logical(True)
        false = Logical(False)
        unknown = Logical(None)
        self.assertEqual(true / true, 1)
        self.assertEqual(true / false, unknown)
        self.assertEqual(false / true, 0)
        self.assertEqual(false / false, unknown)
        self.assertEqual(true / unknown, unknown)
        self.assertEqual(false / unknown, unknown)
        self.assertEqual(unknown / true, unknown)
        self.assertEqual(unknown / false, unknown)
        self.assertEqual(unknown / unknown, unknown)
        self.assertEqual(true / True, 1)
        self.assertEqual(true / False, unknown)
        self.assertEqual(false / True, 0)
        self.assertEqual(false / False, unknown)
        self.assertEqual(true / None, unknown)
        self.assertEqual(false / None, unknown)
        self.assertEqual(unknown / True, unknown)
        self.assertEqual(unknown / False, unknown)
        self.assertEqual(unknown / None, unknown)
        self.assertEqual(True / true, 1)
        self.assertEqual(True / false, unknown)
        self.assertEqual(False / true, 0)
        self.assertEqual(False / false, unknown)
        self.assertEqual(True / unknown, unknown)
        self.assertEqual(False / unknown, unknown)
        self.assertEqual(None / true, unknown)
        self.assertEqual(None / false, unknown)
        self.assertEqual(None / unknown, unknown)

        t = true
        t /= true
        self.assertEqual(t, 1)
        t = true
        t /= false
        self.assertEqual(t, unknown)
        f = false
        f /= true
        self.assertEqual(f, 0)
        f = false
        f /= false
        self.assertEqual(f, unknown)
        t = true
        t /= unknown
        self.assertEqual(t, unknown)
        f = false
        f /= unknown
        self.assertEqual(f, unknown)
        u = unknown
        u /= true
        self.assertEqual(u, unknown)
        u = unknown
        u /= false
        self.assertEqual(u, unknown)
        u = unknown
        u /= unknown
        self.assertEqual(u, unknown)
        t = true
        t /= True
        self.assertEqual(t, 1)
        t = true
        t /= False
        self.assertEqual(t, unknown)
        f = false
        f /= True
        self.assertEqual(f, 0)
        f = false
        f /= False
        self.assertEqual(f, unknown)
        t = true
        t /= None
        self.assertEqual(t, unknown)
        f = false
        f /= None
        self.assertEqual(f, unknown)
        u = unknown
        u /= True
        self.assertEqual(u, unknown)
        u = unknown
        u /= False
        self.assertEqual(u, unknown)
        u = unknown
        u /= None
        self.assertEqual(u, unknown)
        t = True
        t /= true
        self.assertEqual(t, 1)
        t = True
        t /= false
        self.assertEqual(t, unknown)
        f = False
        f /= true
        self.assertEqual(f, 0)
        f = False
        f /= false
        self.assertEqual(f, unknown)
        t = True
        t /= unknown
        self.assertEqual(t, unknown)
        f = False
        f /= unknown
        self.assertEqual(f, unknown)
        u = None
        u /= true
        self.assertEqual(u, unknown)
        u = None
        u /= false
        self.assertEqual(u, unknown)
        u = None
        u /= unknown
        self.assertEqual(u, unknown)


        self.assertEqual(true // true, 1)
        self.assertEqual(true // false, unknown)
        self.assertEqual(false // true, 0)
        self.assertEqual(false // false, unknown)
        self.assertEqual(true // unknown, unknown)
        self.assertEqual(false // unknown, unknown)
        self.assertEqual(unknown // true, unknown)
        self.assertEqual(unknown // false, unknown)
        self.assertEqual(unknown // unknown, unknown)
        self.assertEqual(true // True, 1)
        self.assertEqual(true // False, unknown)
        self.assertEqual(false // True, 0)
        self.assertEqual(false // False, unknown)
        self.assertEqual(true // None, unknown)
        self.assertEqual(false // None, unknown)
        self.assertEqual(unknown // True, unknown)
        self.assertEqual(unknown // False, unknown)
        self.assertEqual(unknown // None, unknown)
        self.assertEqual(True // true, 1)
        self.assertEqual(True // false, unknown)
        self.assertEqual(False // true, 0)
        self.assertEqual(False // false, unknown)
        self.assertEqual(True // unknown, unknown)
        self.assertEqual(False // unknown, unknown)
        self.assertEqual(None // true, unknown)
        self.assertEqual(None // false, unknown)
        self.assertEqual(None // unknown, unknown)

        t = true
        t //= true
        self.assertEqual(t, 1)
        t = true
        t //= false
        self.assertEqual(t, unknown)
        f = false
        f //= true
        self.assertEqual(f, 0)
        f = false
        f //= false
        self.assertEqual(f, unknown)
        t = true
        t //= unknown
        self.assertEqual(t, unknown)
        f = false
        f //= unknown
        self.assertEqual(f, unknown)
        u = unknown
        u //= true
        self.assertEqual(u, unknown)
        u = unknown
        u //= false
        self.assertEqual(u, unknown)
        u = unknown
        u //= unknown
        self.assertEqual(u, unknown)
        t = true
        t //= True
        self.assertEqual(t, 1)
        t = true
        t //= False
        self.assertEqual(t, unknown)
        f = false
        f //= True
        self.assertEqual(f, 0)
        f = false
        f //= False
        self.assertEqual(f, unknown)
        t = true
        t //= None
        self.assertEqual(t, unknown)
        f = false
        f //= None
        self.assertEqual(f, unknown)
        u = unknown
        u //= True
        self.assertEqual(u, unknown)
        u = unknown
        u //= False
        self.assertEqual(u, unknown)
        u = unknown
        u //= None
        self.assertEqual(u, unknown)
        t = True
        t //= true
        self.assertEqual(t, 1)
        t = True
        t //= false
        self.assertEqual(t, unknown)
        f = False
        f //= true
        self.assertEqual(f, 0)
        f = False
        f //= false
        self.assertEqual(f, unknown)
        t = True
        t //= unknown
        self.assertEqual(t, unknown)
        f = False
        f //= unknown
        self.assertEqual(f, unknown)
        u = None
        u //= true
        self.assertEqual(u, unknown)
        u = None
        u //= false
        self.assertEqual(u, unknown)
        u = None
        u //= unknown
        self.assertEqual(u, unknown)

    def test_shift(self):
        "<< and >>"
        true = Logical(True)
        false = Logical(False)
        unknown = Logical(None)

        self.assertEqual(true >> true, 0)
        self.assertEqual(true >> false, 1)
        self.assertEqual(false >> true, 0)
        self.assertEqual(false >> false, 0)
        self.assertEqual(true >> unknown, unknown)
        self.assertEqual(false >> unknown, unknown)
        self.assertEqual(unknown >> true, unknown)
        self.assertEqual(unknown >> false, unknown)
        self.assertEqual(unknown >> unknown, unknown)
        self.assertEqual(true >> True, 0)
        self.assertEqual(true >> False, 1)
        self.assertEqual(false >> True, 0)
        self.assertEqual(false >> False, 0)
        self.assertEqual(true >> None, unknown)
        self.assertEqual(false >> None, unknown)
        self.assertEqual(unknown >> True, unknown)
        self.assertEqual(unknown >> False, unknown)
        self.assertEqual(unknown >> None, unknown)
        self.assertEqual(True >> true, 0)
        self.assertEqual(True >> false, 1)
        self.assertEqual(False >> true, 0)
        self.assertEqual(False >> false, 0)
        self.assertEqual(True >> unknown, unknown)
        self.assertEqual(False >> unknown, unknown)
        self.assertEqual(None >> true, unknown)
        self.assertEqual(None >> false, unknown)
        self.assertEqual(None >> unknown, unknown)

        self.assertEqual(true << true, 2)
        self.assertEqual(true << false, 1)
        self.assertEqual(false << true, 0)
        self.assertEqual(false << false, 0)
        self.assertEqual(true << unknown, unknown)
        self.assertEqual(false << unknown, unknown)
        self.assertEqual(unknown << true, unknown)
        self.assertEqual(unknown << false, unknown)
        self.assertEqual(unknown << unknown, unknown)
        self.assertEqual(true << True, 2)
        self.assertEqual(true << False, 1)
        self.assertEqual(false << True, 0)
        self.assertEqual(false << False, 0)
        self.assertEqual(true << None, unknown)
        self.assertEqual(false << None, unknown)
        self.assertEqual(unknown << True, unknown)
        self.assertEqual(unknown << False, unknown)
        self.assertEqual(unknown << None, unknown)
        self.assertEqual(True << true, 2)
        self.assertEqual(True << false, 1)
        self.assertEqual(False << true, 0)
        self.assertEqual(False << false, 0)
        self.assertEqual(True << unknown, unknown)
        self.assertEqual(False << unknown, unknown)
        self.assertEqual(None << true, unknown)
        self.assertEqual(None << false, unknown)
        self.assertEqual(None << unknown, unknown)

        t = true
        t >>= true
        self.assertEqual(t, 0)
        t = true
        t >>= false
        self.assertEqual(t, 1)
        f = false
        f >>= true
        self.assertEqual(f, 0)
        f = false
        f >>= false
        self.assertEqual(f, 0)
        t = true
        t >>= unknown
        self.assertEqual(t, unknown)
        f = false
        f >>= unknown
        self.assertEqual(f, unknown)
        u = unknown
        u >>= true
        self.assertEqual(u, unknown)
        u = unknown
        u >>= false
        self.assertEqual(u, unknown)
        u = unknown
        u >>= unknown
        self.assertEqual(u, unknown)
        t = true
        t >>= True
        self.assertEqual(t, 0)
        t = true
        t >>= False
        self.assertEqual(t, 1)
        f = false
        f >>= True
        self.assertEqual(f, 0)
        f = false
        f >>= False
        self.assertEqual(f, 0)
        t = true
        t >>= None
        self.assertEqual(t, unknown)
        f = false
        f >>= None
        self.assertEqual(f, unknown)
        u = unknown
        u >>= True
        self.assertEqual(u, unknown)
        u = unknown
        u >>= False
        self.assertEqual(u, unknown)
        u = unknown
        u >>= None
        self.assertEqual(u, unknown)
        t = True
        t >>= true
        self.assertEqual(t, 0)
        t = True
        t >>= false
        self.assertEqual(t, 1)
        f = False
        f >>= true
        self.assertEqual(f, 0)
        f = False
        f >>= false
        self.assertEqual(f, 0)
        t = True
        t >>= unknown
        self.assertEqual(t, unknown)
        f = False
        f >>= unknown
        self.assertEqual(f, unknown)
        u = None
        u >>= true
        self.assertEqual(u, unknown)
        u = None
        u >>= false
        self.assertEqual(u, unknown)
        u = None
        u >>= unknown
        self.assertEqual(u, unknown)

        t = true
        t <<= true
        self.assertEqual(t, 2)
        t = true
        t <<= false
        self.assertEqual(t, 1)
        f = false
        f <<= true
        self.assertEqual(f, 0)
        f = false
        f <<= false
        self.assertEqual(f, 0)
        t = true
        t <<= unknown
        self.assertEqual(t, unknown)
        f = false
        f <<= unknown
        self.assertEqual(f, unknown)
        u = unknown
        u <<= true
        self.assertEqual(u, unknown)
        u = unknown
        u <<= false
        self.assertEqual(u, unknown)
        u = unknown
        u <<= unknown
        self.assertEqual(u, unknown)
        t = true
        t <<= True
        self.assertEqual(t, 2)
        t = true
        t <<= False
        self.assertEqual(t, 1)
        f = false
        f <<= True
        self.assertEqual(f, 0)
        f = false
        f <<= False
        self.assertEqual(f, 0)
        t = true
        t <<= None
        self.assertEqual(t, unknown)
        f = false
        f <<= None
        self.assertEqual(f, unknown)
        u = unknown
        u <<= True
        self.assertEqual(u, unknown)
        u = unknown
        u <<= False
        self.assertEqual(u, unknown)
        u = unknown
        u <<= None
        self.assertEqual(u, unknown)
        t = True
        t <<= true
        self.assertEqual(t, 2)
        t = True
        t <<= false
        self.assertEqual(t, 1)
        f = False
        f <<= true
        self.assertEqual(f, 0)
        f = False
        f <<= false
        self.assertEqual(f, 0)
        t = True
        t <<= unknown
        self.assertEqual(t, unknown)
        f = False
        f <<= unknown
        self.assertEqual(f, unknown)
        u = None
        u <<= true
        self.assertEqual(u, unknown)
        u = None
        u <<= false
        self.assertEqual(u, unknown)
        u = None
        u <<= unknown
        self.assertEqual(u, unknown)

    def test_pow(self):
        "**"
        true = Logical(True)
        false = Logical(False)
        unknown = Logical(None)

        self.assertEqual(true ** true, 1)
        self.assertEqual(true ** false, 1)
        self.assertEqual(false ** true, 0)
        self.assertEqual(false ** false, 1)
        self.assertEqual(true ** unknown, unknown)
        self.assertEqual(false ** unknown, unknown)
        self.assertEqual(unknown ** true, unknown)
        self.assertEqual(unknown ** false, 1)
        self.assertEqual(unknown ** unknown, unknown)
        self.assertEqual(true ** True, 1)
        self.assertEqual(true ** False, 1)
        self.assertEqual(false ** True, 0)
        self.assertEqual(false ** False, 1)
        self.assertEqual(true ** None, unknown)
        self.assertEqual(false ** None, unknown)
        self.assertEqual(unknown ** True, unknown)
        self.assertEqual(unknown ** False, 1)
        self.assertEqual(unknown ** None, unknown)
        self.assertEqual(True ** true, 1)
        self.assertEqual(True ** false, 1)
        self.assertEqual(False ** true, 0)
        self.assertEqual(False ** false, 1)
        self.assertEqual(True ** unknown, unknown)
        self.assertEqual(False ** unknown, unknown)
        self.assertEqual(None ** true, unknown)
        self.assertEqual(None ** false, 1)
        self.assertEqual(None ** unknown, unknown)

        t = true
        t **= true
        self.assertEqual(t, 1)
        t = true
        t **= false
        self.assertEqual(t, 1)
        f = false
        f **= true
        self.assertEqual(f, 0)
        f = false
        f **= false
        self.assertEqual(f, 1)
        t = true
        t **= unknown
        self.assertEqual(t, unknown)
        f = false
        f **= unknown
        self.assertEqual(f, unknown)
        u = unknown
        u **= true
        self.assertEqual(u, unknown)
        u = unknown
        u **= false
        self.assertEqual(u, 1)
        u = unknown
        u **= unknown
        self.assertEqual(u, unknown)
        t = true
        t **= True
        self.assertEqual(t, 1)
        t = true
        t **= False
        self.assertEqual(t, 1)
        f = false
        f **= True
        self.assertEqual(f, 0)
        f = false
        f **= False
        self.assertEqual(f, 1)
        t = true
        t **= None
        self.assertEqual(t, unknown)
        f = false
        f **= None
        self.assertEqual(f, unknown)
        u = unknown
        u **= True
        self.assertEqual(u, unknown)
        u = unknown
        u **= False
        self.assertEqual(u, 1)
        u = unknown
        u **= None
        self.assertEqual(u, unknown)
        t = True
        t **= true
        self.assertEqual(t, 1)
        t = True
        t **= false
        self.assertEqual(t, 1)
        f = False
        f **= true
        self.assertEqual(f, 0)
        f = False
        f **= false
        self.assertEqual(f, 1)
        t = True
        t **= unknown
        self.assertEqual(t, unknown)
        f = False
        f **= unknown
        self.assertEqual(f, unknown)
        u = None
        u **= true
        self.assertEqual(u, unknown)
        u = None
        u **= false
        self.assertEqual(u, 1)
        u = None
        u **= unknown
        self.assertEqual(u, unknown)

    def test_mod(self):
        "%"
        true = Logical(True)
        false = Logical(False)
        unknown = Logical(None)

        self.assertEqual(true % true, 0)
        self.assertEqual(true % false, unknown)
        self.assertEqual(false % true, 0)
        self.assertEqual(false % false, unknown)
        self.assertEqual(true % unknown, unknown)
        self.assertEqual(false % unknown, unknown)
        self.assertEqual(unknown % true, unknown)
        self.assertEqual(unknown % false, unknown)
        self.assertEqual(unknown % unknown, unknown)
        self.assertEqual(true % True, 0)
        self.assertEqual(true % False, unknown)
        self.assertEqual(false % True, 0)
        self.assertEqual(false % False, unknown)
        self.assertEqual(true % None, unknown)
        self.assertEqual(false % None, unknown)
        self.assertEqual(unknown % True, unknown)
        self.assertEqual(unknown % False, unknown)
        self.assertEqual(unknown % None, unknown)
        self.assertEqual(True % true, 0)
        self.assertEqual(True % false, unknown)
        self.assertEqual(False % true, 0)
        self.assertEqual(False % false, unknown)
        self.assertEqual(True % unknown, unknown)
        self.assertEqual(False % unknown, unknown)
        self.assertEqual(None % true, unknown)
        self.assertEqual(None % false, unknown)
        self.assertEqual(None % unknown, unknown)

        t = true
        t %= true
        self.assertEqual(t, 0)
        t = true
        t %= false
        self.assertEqual(t, unknown)
        f = false
        f %= true
        self.assertEqual(f, 0)
        f = false
        f %= false
        self.assertEqual(f, unknown)
        t = true
        t %= unknown
        self.assertEqual(t, unknown)
        f = false
        f %= unknown
        self.assertEqual(f, unknown)
        u = unknown
        u %= true
        self.assertEqual(u, unknown)
        u = unknown
        u %= false
        self.assertEqual(u, unknown)
        u = unknown
        u %= unknown
        self.assertEqual(u, unknown)
        t = true
        t %= True
        self.assertEqual(t, 0)
        t = true
        t %= False
        self.assertEqual(t, unknown)
        f = false
        f %= True
        self.assertEqual(f, 0)
        f = false
        f %= False
        self.assertEqual(f, unknown)
        t = true
        t %= None
        self.assertEqual(t, unknown)
        f = false
        f %= None
        self.assertEqual(f, unknown)
        u = unknown
        u %= True
        self.assertEqual(u, unknown)
        u = unknown
        u %= False
        self.assertEqual(u, unknown)
        u = unknown
        u %= None
        self.assertEqual(u, unknown)
        t = True
        t %= true
        self.assertEqual(t, 0)
        t = True
        t %= false
        self.assertEqual(t, unknown)
        f = False
        f %= true
        self.assertEqual(f, 0)
        f = False
        f %= false
        self.assertEqual(f, unknown)
        t = True
        t %= unknown
        self.assertEqual(t, unknown)
        f = False
        f %= unknown
        self.assertEqual(f, unknown)
        u = None
        u %= true
        self.assertEqual(u, unknown)
        u = None
        u %= false
        self.assertEqual(u, unknown)
        u = None
        u %= unknown
        self.assertEqual(u, unknown)

    def test_divmod(self):
        "divmod()"
        true = Logical(True)
        false = Logical(False)
        unknown = Logical(None)

        self.assertEqual(divmod(true, true), (1, 0))
        self.assertEqual(divmod(true, false), (unknown, unknown))
        self.assertEqual(divmod(false, true), (0, 0))
        self.assertEqual(divmod(false, false), (unknown, unknown))
        self.assertEqual(divmod(true, unknown), (unknown, unknown))
        self.assertEqual(divmod(false, unknown), (unknown, unknown))
        self.assertEqual(divmod(unknown, true), (unknown, unknown))
        self.assertEqual(divmod(unknown, false), (unknown, unknown))
        self.assertEqual(divmod(unknown, unknown), (unknown, unknown))
        self.assertEqual(divmod(true, True), (1, 0))
        self.assertEqual(divmod(true, False), (unknown, unknown))
        self.assertEqual(divmod(false, True), (0, 0))
        self.assertEqual(divmod(false, False), (unknown, unknown))
        self.assertEqual(divmod(true, None), (unknown, unknown))
        self.assertEqual(divmod(false, None), (unknown, unknown))
        self.assertEqual(divmod(unknown, True), (unknown, unknown))
        self.assertEqual(divmod(unknown, False), (unknown, unknown))
        self.assertEqual(divmod(unknown, None), (unknown, unknown))
        self.assertEqual(divmod(True, true), (1, 0))
        self.assertEqual(divmod(True, false), (unknown, unknown))
        self.assertEqual(divmod(False, true), (0, 0))
        self.assertEqual(divmod(False, false), (unknown, unknown))
        self.assertEqual(divmod(True, unknown), (unknown, unknown))
        self.assertEqual(divmod(False, unknown), (unknown, unknown))
        self.assertEqual(divmod(None, true), (unknown, unknown))
        self.assertEqual(divmod(None, false), (unknown, unknown))
        self.assertEqual(divmod(None, unknown), (unknown, unknown))


class TestWarnings(TestCase):

    def test_field_name_warning(self):
        with warnings.catch_warnings(record=True) as w:
            huh = dbf.Table('cloud', 'p^type C(25)', on_disk=False).open(dbf.READ_WRITE)
            self.assertEqual(len(w), 1, str(w))
            warning = w[-1]
            self.assertTrue(issubclass(warning.category, dbf.FieldNameWarning))
            huh.resize_field('p^type', 30)
            self.assertEqual(len(w), 1, 'warning objects\n'+'\n'.join([str(warning) for warning in w]))
            huh.add_fields('c^word C(50)')
            self.assertEqual(len(w), 2, str(w))
            warning = w[-1]
            self.assertTrue(issubclass(warning.category, dbf.FieldNameWarning))


class TestIndexLocation(TestCase):

    def test_false(self):
        self.assertFalse(IndexLocation(0, False))
        self.assertFalse(IndexLocation(42, False))

    def test_true(self):
        self.assertTrue(IndexLocation(0, True))
        self.assertTrue(IndexLocation(42, True))


class TestDbfRecords(TestCase):
    "Testing records"

    def setUp(self):
        self.dbf_table = Table(
                os.path.join(tempdir, 'dbf_table'),
                u'name C(25); paid L; qty N(11,5); orderdate D; desc M',
                dbf_type='db3',
                )
        self.vfp_table = Table(
                os.path.join(tempdir, 'vfp_table'),
                u'name C(25); paid L; qty N(11,5); orderdate D; desc M; mass B;' +
                u' weight F(18,3); age I; meeting T; misc G; photo P; price Y;' +
                u' dist B',
                dbf_type='vfp',
                default_data_types='enhanced',
                )
        self.null_vfp_table = null_table = Table(
                os.path.join(tempdir, 'null_vfp_table'),
                'first C(25) null; last C(25); height N(3,1) null; age N(3,0); life_story M null; plans M',
                dbf_type='vfp',
                )
        null_table.open(dbf.READ_WRITE)
        null_table.append()
        null_table.close()

    def tearDown(self):
        self.dbf_table.close()
        self.vfp_table.close()
        self.null_vfp_table.close()

    def test_slicing(self):
        table = self.dbf_table
        table.open(mode=READ_WRITE)
        table.append(('myself', True, 5.97, dbf.Date(2012, 5, 21), 'really cool'))
        self.assertEqual(table.first_record[u'name':u'qty'], table[0][:3])

    def test_dbf_adding_records(self):
        "dbf table:  adding records"
        table = self.dbf_table
        table.open(mode=READ_WRITE)
        namelist = []
        paidlist = []
        qtylist = []
        orderlist = []
        desclist = []
        for i in range(len(floats)):
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
            table.append(unicodify({'name':name, 'paid':paid, 'qty':qty, 'orderdate':orderdate, 'desc':desc}))
            record = table[-1]

            t = open(table.filename, 'rb')
            last_byte = ord(t.read()[-1])
            t.close()
            self.assertEqual(last_byte, EOF)
            self.assertEqual(record.name.strip(), name)
            self.assertEqual(record.paid, paid)
            self.assertEqual(record.qty, round(qty, 5))
            self.assertEqual(record.orderdate, orderdate)
            self.assertEqual(record.desc.strip(), desc)
        # plus a blank record
        namelist.append('')
        paidlist.append(None)
        qtylist.append(None)
        orderlist.append(None)
        desclist.append('')
        blank_record = table.append()
        self.assertEqual(len(table), len(floats)+1)
        for field in table.field_names:
            self.assertEqual(1, table.field_names.count(field))
        table.close()
        t = open(table.filename, 'rb')
        last_byte = ord(t.read()[-1])
        t.close()
        self.assertEqual(last_byte, EOF)
        table = Table(table.filename, dbf_type='db3')
        table.open(mode=READ_WRITE)
        self.assertEqual(len(table), len(floats)+1)
        for field in table.field_names:
            self.assertEqual(1, table.field_names.count(field))
        i = 0
        for record in table[:-1]:
            i += 1
            continue
            self.assertEqual(dbf.recno(record), i)
            self.assertEqual(table[i].name.strip(), namelist[i])
            self.assertEqual(record.name.strip(), namelist[i])
            self.assertEqual(table[i].paid, paidlist[i])
            self.assertEqual(record.paid, paidlist[i])
            self.assertEqual(abs(table[i].qty - qtylist[i]) < .00001, True)
            self.assertEqual(abs(record.qty - qtylist[i]) < .00001, True)
            self.assertEqual(table[i].orderdate, orderlist[i])
            self.assertEqual(record.orderdate, orderlist[i])
            self.assertEqual(table[i].desc.strip(), desclist[i])
            self.assertEqual(record.desc.strip(), desclist[i])
            i += 1
        record = table[-1]
        self.assertEqual(dbf.recno(record), i)
        self.assertEqual(table[i].name.strip(), namelist[i])
        self.assertEqual(record.name.strip(), namelist[i])
        self.assertEqual(table[i].paid, paidlist[i])
        self.assertEqual(record.paid, paidlist[i])
        self.assertEqual(table[i].qty, qtylist[i])
        self.assertEqual(record.qty, qtylist[i])
        self.assertEqual(table[i].orderdate, orderlist[i])
        self.assertEqual(record.orderdate, orderlist[i])
        self.assertEqual(table[i].desc, desclist[i])
        self.assertEqual(record.desc, desclist[i])
        i += 1
        self.assertEqual(i, len(table))
        table.close()

    def test_vfp_adding_records(self):
        "vfp table:  adding records"
        table = self.vfp_table
        table.open(mode=READ_WRITE)
        namelist = []
        paidlist = []
        qtylist = []
        orderlist = []
        desclist = []
        masslist = []
        weightlist = []
        agelist = []
        meetlist = []
        misclist = []
        photolist = []
        pricelist = []
        distlist = []
        for i in range(len(floats)):
            name = words[i]
            paid = len(words[i]) % 3 == 0
            qty = floats[i]
            orderdate = datetime.date((numbers[i] + 1) * 2, (numbers[i] % 12) +1, (numbers[i] % 27) + 1)
            desc = ' '.join(words[i:i+50])
            mass = floats[i] * floats[i] / 2.0
            weight = floats[i] * 3
            dist = floats[i] * 2
            age = numbers[i]
            meeting = datetime.datetime((numbers[i] + 2000), (numbers[i] % 12)+1, (numbers[i] % 28)+1,
                      (numbers[i] % 24), numbers[i] % 60, (numbers[i] * 3) % 60)
            misc = (' '.join(words[i:i+50:3])).encode('ascii')
            photo = (' '.join(words[i:i+50:7])).encode('ascii')
            price = Decimal(round(floats[i] * 2.182737, 4))
            namelist.append(name)
            paidlist.append(paid)
            qtylist.append(qty)
            orderlist.append(orderdate)
            desclist.append(desc)
            masslist.append(mass)
            distlist.append(dist)
            weightlist.append(weight)
            agelist.append(age)
            meetlist.append(meeting)
            misclist.append(misc)
            photolist.append(photo)
            pricelist.append(price)
            table.append(unicodify({'name':name, 'paid':paid, 'qty':qty, 'orderdate':orderdate, 'desc':desc,
                    'mass':mass, 'weight':weight, 'age':age, 'meeting':meeting, 'misc':misc, 'photo':photo,
                    'dist': dist, 'price':price}))
            record = table[-1]
            self.assertEqual(record.name.strip(), name)
            self.assertEqual(record.paid, paid)
            self.assertEqual(round(record.qty, 5), round(qty, 5))
            self.assertEqual(record.orderdate, orderdate)
            self.assertEqual(record.desc.strip(), desc)
            self.assertEqual(record.mass, mass)
            self.assertEqual(record.dist, dist)
            self.assertEqual(round(record.weight, 3), round(weight, 3))
            self.assertEqual(record.age, age)
            self.assertEqual(record.meeting, meeting)
            self.assertEqual(record.misc, misc)
            self.assertEqual(record.photo, photo)
            self.assertEqual(round(record.price, 4), round(price, 4))
        # plus a blank record
        namelist.append('')
        paidlist.append(Unknown)
        qtylist.append(None)
        orderlist.append(NullDate)
        desclist.append('')
        masslist.append(0.0)
        distlist.append(0.0)
        weightlist.append(None)
        agelist.append(0)
        meetlist.append(NullDateTime)
        misclist.append(''.encode('ascii'))
        photolist.append(''.encode('ascii'))
        pricelist.append(Decimal('0.0'))
        table.append()
        table.close()
        table = Table(table.filename, dbf_type='vfp')
        table.open(mode=READ_WRITE)
        self.assertEqual(len(table), len(floats)+1)
        i = 0
        for record in table[:-1]:
            self.assertEqual(dbf.recno(record), i)
            self.assertEqual(table[i].name.strip(), namelist[i])
            self.assertEqual(record.name.strip(), namelist[i])
            self.assertEqual(table[i].paid, paidlist[i])
            self.assertEqual(record.paid, paidlist[i])
            self.assertEqual(abs(table[i].qty - qtylist[i]) < .00001, True)
            self.assertEqual(abs(record.qty - qtylist[i]) < .00001, True)
            self.assertEqual(table[i].orderdate, orderlist[i])
            self.assertEqual(record.orderdate, orderlist[i])
            self.assertEqual(table[i].desc.strip(), desclist[i])
            self.assertEqual(record.desc.strip(), desclist[i])
            self.assertEqual(record.mass, masslist[i])
            self.assertEqual(record.dist, distlist[i])
            self.assertEqual(table[i].mass, masslist[i])
            self.assertEqual(record.weight, round(weightlist[i], 3))
            self.assertEqual(table[i].weight, round(weightlist[i], 3))
            self.assertEqual(record.age, agelist[i])
            self.assertEqual(table[i].age, agelist[i])
            self.assertEqual(record.meeting, meetlist[i])
            self.assertEqual(table[i].meeting, meetlist[i])
            self.assertEqual(record.misc, misclist[i])
            self.assertEqual(table[i].misc, misclist[i])
            self.assertEqual(record.photo, photolist[i])
            self.assertEqual(table[i].photo, photolist[i])
            self.assertEqual(round(record.price, 4), round(pricelist[i], 4))
            self.assertEqual(round(table[i].price, 4), round(pricelist[i], 4))
            i += 1
        record = table[-1]
        self.assertEqual(dbf.recno(record), i)
        self.assertEqual(table[i].name.strip(), namelist[i])
        self.assertEqual(record.name.strip(), namelist[i])
        self.assertEqual(table[i].paid is None, True)
        self.assertEqual(record.paid is None, True)
        self.assertEqual(table[i].qty, None)
        self.assertEqual(record.qty, None)
        self.assertEqual(table[i].orderdate, orderlist[i])
        self.assertEqual(record.orderdate, orderlist[i])
        self.assertEqual(table[i].desc, desclist[i])
        self.assertEqual(record.desc, desclist[i])
        self.assertEqual(record.mass, masslist[i])
        self.assertEqual(table[i].mass, masslist[i])
        self.assertEqual(record.dist, distlist[i])
        self.assertEqual(table[i].dist, distlist[i])
        self.assertEqual(record.weight, weightlist[i])
        self.assertEqual(table[i].weight, weightlist[i])
        self.assertEqual(record.age, agelist[i])
        self.assertEqual(table[i].age, agelist[i])
        self.assertEqual(record.meeting, meetlist[i])
        self.assertEqual(table[i].meeting, meetlist[i])
        self.assertEqual(record.misc, misclist[i])
        self.assertEqual(table[i].misc, misclist[i])
        self.assertEqual(record.photo, photolist[i])
        self.assertEqual(table[i].photo, photolist[i])
        self.assertEqual(record.price, 0)
        self.assertEqual(table[i].price, 0)
        i += 1
        table.close()

    def test_char_memo_return_type(self):
        "check character fields return type"
        table = Table(':memory:', 'text C(50); memo M', codepage='cp1252', dbf_type='vfp', on_disk=False)
        table.open(mode=READ_WRITE)
        table.append(('another one bites the dust', "and another one's gone, and another one's gone..."))
        table.append()
        for record in table:
            self.assertTrue(type(record.text) is unicode)
            self.assertTrue(type(record.memo) is unicode)

        table = Table(':memory:', 'text C(50); memo M', codepage='cp1252', dbf_type='vfp',
            default_data_types=dict(C=Char, M=Char), on_disk=False)
        table.open(mode=READ_WRITE)
        table.append(('another one bites the dust', "and another one's gone, and another one's gone..."))
        table.append()
        for record in table:
            self.assertTrue(type(record.text) is Char)
            self.assertTrue(type(record.memo) is Char)

        table = Table(':memory:', 'text C(50); memo M', codepage='cp1252', dbf_type='vfp',
            default_data_types=dict(C=(Char, NoneType), M=(Char, NoneType)), on_disk=False)
        table.open(mode=READ_WRITE)
        table.append(('another one bites the dust', "and another one's gone, and another one's gone..."))
        table.append()
        record = table[0]
        self.assertTrue(type(record.text) is Char)
        self.assertTrue(type(record.memo) is Char)
        record = table[1]
        self.assertTrue(type(record.text) is NoneType)
        self.assertTrue(type(record.memo) is NoneType)

    def test_empty_is_none(self):
        "empty and None values"
        table = Table(':memory:', 'name C(20); born L; married D; appt T; wisdom M', dbf_type='vfp', on_disk=False)
        table.open(mode=READ_WRITE)
        table.append()
        record = table[-1]
        self.assertTrue(record.born is None)
        self.assertTrue(record.married is None)
        self.assertTrue(record.appt is None)
        self.assertEqual(record.wisdom, '')
        appt = DateTime.now()
        dbf.write(
                record,
                born = True,
                married = Date(1992, 6, 27),
                appt = appt,
                wisdom = 'Choose Python',
                )
        self.assertTrue(record.born)
        self.assertEqual(record.married, Date(1992, 6, 27))
        self.assertEqual(record.appt, appt)
        self.assertEqual(record.wisdom, 'Choose Python')
        dbf.write(
                record,
                born = Unknown,
                married = NullDate,
                appt = NullDateTime,
                wisdom = '',
                )
        self.assertTrue(record.born is None)
        self.assertTrue(record.married is None)
        self.assertTrue(record.appt is None)
        self.assertEqual(record.wisdom, '')

    def test_custom_data_type(self):
        "custom data types"
        table = Table(
            filename=':memory:',
            field_specs='name C(20); born L; married D; appt T; wisdom M',
            field_data_types=dict(name=Char, born=Logical, married=Date, appt=DateTime, wisdom=Char,),
            dbf_type='vfp',
            on_disk=False,
            )
        table.open(mode=READ_WRITE)
        table.append()
        record = table[-1]
        self.assertTrue(type(record.name) is Char, "record.name is %r, not Char" % type(record.name))
        self.assertTrue(type(record.born) is Logical, "record.born is %r, not Logical" % type(record.born))
        self.assertTrue(type(record.married) is Date, "record.married is %r, not Date" % type(record.married))
        self.assertTrue(type(record.appt) is DateTime, "record.appt is %r, not DateTime" % type(record.appt))
        self.assertTrue(type(record.wisdom) is Char, "record.wisdom is %r, not Char" % type(record.wisdom))
        self.assertEqual(record.name, ' ' * 20)
        self.assertTrue(record.born is Unknown, "record.born is %r, not Unknown" % record.born)
        self.assertTrue(record.married is NullDate, "record.married is %r, not NullDate" % record.married)
        self.assertEqual(record.married, None)
        self.assertTrue(record.appt is NullDateTime, "record.appt is %r, not NullDateTime" % record.appt)
        self.assertEqual(record.appt, None)
        appt = DateTime.now()
        dbf.write(
                record,
                name = 'Ethan               ',
                born = True,
                married = Date(1992, 6, 27),
                appt = appt,
                wisdom = 'Choose Python',
                )
        self.assertEqual(type(record.name), Char, "record.wisdom is %r, but should be Char" % record.wisdom)
        self.assertTrue(record.born is Truth)
        self.assertEqual(record.married, Date(1992, 6, 27))
        self.assertEqual(record.appt, appt)
        self.assertEqual(type(record.wisdom), Char, "record.wisdom is %r, but should be Char" % record.wisdom)
        self.assertEqual(record.wisdom, 'Choose Python')
        dbf.write(record, born=Falsth)
        self.assertEqual(record.born, False)
        dbf.write(record, born=None, married=None, appt=None, wisdom=None)
        self.assertTrue(record.born is Unknown)
        self.assertTrue(record.married is NullDate)
        self.assertTrue(record.appt is NullDateTime)
        self.assertTrue(type(record.wisdom) is Char, "record.wisdom is %r, but should be Char" % type(record.wisdom))

    def test_datatypes_param(self):
        "field_types with normal data type but None on empty"
        table = Table(
            filename=':memory:',
            field_specs='name C(20); born L; married D; wisdom M',
            field_data_types=dict(name=(str, NoneType), born=(bool, bool)),
            dbf_type='db3',
            on_disk=False,
            )
        table.open(mode=READ_WRITE)
        table.append()
        record = table[-1]
        self.assertTrue(type(record.name) is type(None), "record.name is %r, not None" % type(record.name))
        self.assertTrue(type(record.born) is bool, "record.born is %r, not bool" % type(record.born))
        self.assertTrue(record.name is None)
        self.assertTrue(record.born is False, "record.born is %r, not False" % record.born)
        dbf.write(record, name='Ethan               ', born=True)
        self.assertEqual(type(record.name), str, "record.name is %r, but should be Char" % record.wisdom)
        self.assertTrue(record.born is True)
        dbf.write(record, born=False)
        self.assertEqual(record.born, False)
        dbf.write(
            record,
            name = None,
            born = None,
            )
        self.assertTrue(record.name is None)
        self.assertTrue(record.born is False)

    def test_null_type(self):
        "NullType"
        table = Table(
            filename=':memory:',
            field_specs='name C(20) NULL; born L NULL; married D NULL; appt T NULL; wisdom M NULL',
            default_data_types=dict(
                    C=(Char, NoneType, NullType),
                    L=(Logical, NoneType, NullType),
                    D=(Date, NoneType, NullType),
                    T=(DateTime, NoneType, NullType),
                    M=(Char, NoneType, NullType),
                    ),
            dbf_type='vfp',
            on_disk=False,
            )
        table.open(mode=READ_WRITE)
        table.append()
        record = table[-1]
        self.assertIs(record.name, Null)
        self.assertIs(record.born, Null)
        self.assertIs(record.married, Null)
        self.assertIs(record.appt, Null)
        self.assertIs(record.wisdom, Null)
        appt = datetime.datetime(2012, 12, 15, 9, 37, 11)
        dbf.write(
                record,
                name = 'Ethan               ',
                born = True,
                married = datetime.date(2001, 6, 27),
                appt = appt,
                wisdom = 'timing is everything',
                )
        record = table[-1]
        self.assertEqual(record.name, u'Ethan')
        self.assertEqual(type(record.name), Char)
        self.assertTrue(record.born)
        self.assertTrue(record.born is Truth)
        self.assertEqual(record.married, datetime.date(2001, 6, 27))
        self.assertEqual(type(record.married), Date)
        self.assertEqual(record.appt, datetime.datetime(2012, 12, 15, 9, 37, 11))
        self.assertEqual(type(record.appt), DateTime)
        self.assertEqual(record.wisdom, u'timing is everything')
        self.assertEqual(type(record.wisdom), Char)
        dbf.write(record, name=Null, born=Null, married=Null, appt=Null, wisdom=Null)
        self.assertTrue(record.name is Null)
        self.assertTrue(record.born is Null)
        self.assertTrue(record.married is Null)
        self.assertTrue(record.appt is Null)
        self.assertTrue(record.wisdom is Null)
        dbf.write(
                record,
                name = None,
                born = None,
                married = None,
                appt = None,
                wisdom = None,
                )
        record = table[-1]
        self.assertTrue(record.name is None)
        self.assertTrue(record.born is None)
        self.assertTrue(record.married is None)
        self.assertTrue(record.appt is None)
        self.assertTrue(record.wisdom is None)
        table = Table(
            filename=':memory:',
            field_specs='name C(20); born L; married D NULL; appt T; wisdom M; pets L; cars N(3,0) NULL; story M; died D NULL;',
            default_data_types=dict(
                    C=(Char, NoneType, NullType),
                    L=(Logical, NoneType, NullType),
                    D=(Date, NoneType, NullType),
                    T=(DateTime, NoneType, NullType),
                    M=(Char, NoneType, NullType),
                    N=(int, NoneType, NullType),
                    ),
            dbf_type='vfp',
            on_disk=False,
            )
        table.open(mode=READ_WRITE)
        table.append()
        record = table[-1]
        self.assertTrue(record.name is None)
        self.assertTrue(record.born is None)
        self.assertTrue(record.married is Null)
        self.assertTrue(record.appt is None)
        self.assertTrue(record.wisdom is None)
        self.assertTrue(record.pets is None)
        self.assertTrue(record.cars is Null)
        self.assertTrue(record.story is None)
        self.assertTrue(record.died is Null)
        dbf.write(
                record,
                name = 'Ethan               ',
                born = True,
                married = datetime.date(2001, 6, 27),
                appt = appt,
                wisdom = 'timing is everything',
                pets = True,
                cars = 10,
                story = 'a poor farm boy who made  good',
                died = datetime.date(2018, 5, 30),
                )
        record = table[-1]
        self.assertEqual(record.name, 'Ethan')
        self.assertTrue(record.born)
        self.assertTrue(record.born is Truth)
        self.assertEqual(record.married, datetime.date(2001, 6, 27))
        self.assertEqual(record.appt, datetime.datetime(2012, 12, 15, 9, 37, 11))
        self.assertEqual(record.wisdom, 'timing is everything')
        self.assertTrue(record.pets)
        self.assertEqual(record.cars, 10)
        self.assertEqual(record.story, 'a poor farm boy who made  good',)
        self.assertEqual(record.died, datetime.date(2018, 5, 30))
        dbf.write(record, married=Null, died=Null)
        record = table[-1]
        self.assertTrue(record.married is Null)
        self.assertTrue(record.died is Null)

    def test_nonascii_text_cptrans(self):
        "check non-ascii text to unicode"
        table = Table(':memory:', 'data C(50); memo M', codepage='cp437', dbf_type='vfp', on_disk=False)
        table.open(mode=READ_WRITE)
        decoder = codecs.getdecoder('cp437')
        if py_ver < (3, 0):
            high_ascii = decoder(''.join(chr(c) for c in range(128, 128+50)))[0]
        else:
            high_ascii = bytes(range(128, 128+50)).decode('cp437')
        table.append(dict(data=high_ascii, memo=high_ascii))
        self.assertEqual(table[0].data, high_ascii)
        self.assertEqual(table[0].memo, high_ascii)
        table.close()

    def test_nonascii_text_no_cptrans(self):
        "check non-ascii text to bytes"
        table = Table(':memory:', 'bindata C(50) BINARY; binmemo M BINARY', codepage='cp1252', dbf_type='vfp', on_disk=False)
        table.open(mode=READ_WRITE)
        if py_ver < (3, 0):
            high_ascii = ''.join(chr(c) for c in range(128, 128+50))
        else:
            high_ascii = bytes(range(128, 128+50))
        table.append(dict(bindata=high_ascii, binmemo=high_ascii))
        bindata = table[0].bindata
        binmemo = table[0].binmemo
        self.assertTrue(isinstance(bindata, bytes))
        self.assertTrue(isinstance(binmemo, bytes))
        self.assertEqual(table[0].bindata, high_ascii)
        self.assertEqual(table[0].binmemo, high_ascii)
        table.close()

    def test_add_null_field(self):
        "adding a NULL field to an existing table"
        table = Table(
            self.vfp_table.filename,
            'name C(50); age N(3,0)',
            dbf_type='vfp',
            )
        table.open(mode=READ_WRITE)
        def _50(text):
            return text + ' ' * (50 - len(text))
        data = ( (_50('Ethan'), 29), (_50('Joseph'), 33), (_50('Michael'), 54), )
        for datum in data:
            table.append(datum)
        for datum, recordnum in zip(data, table):
            self.assertEqual(datum, tuple(recordnum))
        table.add_fields('fired D NULL')
        for datum, recordnum in zip(data, table):
            self.assertEqual(datum, tuple(recordnum)[:2])
        data += ((_50('Daniel'), 44, Null), )
        table.append(('Daniel', 44, Null))
        for datum, recordnum in zip(data, table):
            self.assertEqual(datum[:2], tuple(recordnum)[:2])
        self.assertTrue(datum[2] is recordnum[2])
        table.close()
        table = Table(table.filename)
        table.open(mode=READ_WRITE)
        for datum, recordnum in zip(data, table):
            self.assertEqual(datum[0:2], tuple(recordnum)[:2])
        self.assertTrue(datum[2] is recordnum[2])
        table.close()

    def test_remove_null_field(self):
        "removing NULL fields from an existing table"
        table = Table(
            self.vfp_table.filename,
            'name C(50); age N(3,0); fired D NULL',
            dbf_type='vfp',
            )
        table.open(mode=READ_WRITE)
        def _50(text):
            return text + ' ' * (50 - len(text))
        data = ( (_50('Ethan'), 29, Null), (_50('Joseph'), 33, Null), (_50('Michael'), 54, Date(2010, 5, 3)))
        for datum in data:
            table.append(datum)
        for datum, recordnum in zip(data, table):
            self.assertEqual(datum[:2], tuple(recordnum)[:2])
            self.assertTrue(datum[2] is recordnum[2] or datum[2] == recordnum[2])
        table.delete_fields('fired')
        for datum, recordnum in zip(data, table):
            self.assertEqual(datum[:2], tuple(recordnum))
        data += ((_50('Daniel'), 44), )
        table.append(('Daniel', 44))
        for datum, recordnum in zip(data, table):
            self.assertEqual(datum[:2], tuple(recordnum))
        table.close()
        table = Table(table.filename)
        table.open(mode=READ_WRITE)
        for datum, recordnum in zip(data, table):
            self.assertEqual(datum[:2], tuple(recordnum))
        table.close()

    def test_add_field_to_null(self):
        "adding a normal field to a table with NULL fields"
        table = Table(
            self.vfp_table.filename,
            'name C(50); age N(3,0); fired D NULL',
            dbf_type='vfp',
            )
        table.open(mode=READ_WRITE)
        def _50(text):
            return text + ' ' * (50 - len(text))
        data = ( (_50('Ethan'), 29, Null), (_50('Joseph'), 33, Null), (_50('Michael'), 54, Date(2010, 7, 4)), )
        for datum in data:
            table.append(datum)
        for datum, recordnum in zip(data, table):
            self.assertEqual(datum[:2], tuple(recordnum)[:2])
            self.assertTrue(datum[2] is recordnum[2] or datum[2] == recordnum[2])
        table.add_fields('tenure N(3,0)')
        for datum, recordnum in zip(data, table):
            self.assertEqual(datum[:2], tuple(recordnum)[:2])
            self.assertTrue(datum[2] is recordnum[2] or datum[2] == recordnum[2])
        data += ((_50('Daniel'), 44, Date(2005, 1, 31), 15 ), )
        table.append(('Daniel', 44, Date(2005, 1, 31), 15))
        for datum, recordnum in zip(data, table):
            self.assertEqual(datum[:2], tuple(recordnum)[:2])
            self.assertTrue(datum[2] is recordnum[2] or datum[2] == recordnum[2])
        self.assertEqual(datum[3], recordnum[3])
        table.close()
        table = Table(table.filename)
        table.open(mode=READ_WRITE)
        for datum, recordnum in zip(data, table):
            self.assertEqual(datum[:2], tuple(recordnum)[:2])
            self.assertTrue(datum[2] is recordnum[2] or datum[2] == recordnum[2])
        self.assertEqual(datum[3], recordnum[3])
        table.close()

    def test_remove_field_from_null(self):
        "removing a normal field from a table with NULL fields"
        table = Table(
            self.vfp_table.filename,
            'name C(50); age N(3,0); fired D NULL',
            dbf_type='vfp',
            )
        table.open(mode=READ_WRITE)
        def _50(text):
            return text + ' ' * (50 - len(text))
        data = ( (_50('Ethan'), 29, Null), (_50('Joseph'), 33, Null), (_50('Michael'), 54, Date(2010, 7, 4)), )
        for datum in data:
            table.append(datum)
        for datum, recordnum in zip(data, table):
            self.assertEqual(datum[:2], tuple(recordnum)[:2])
            self.assertTrue(datum[2] is recordnum[2] or datum[2] == recordnum[2])
        table.delete_fields('age')
        for datum, recordnum in zip(data, table):
            self.assertEqual(datum[0], recordnum[0])
            self.assertTrue(datum[-1] is recordnum[1] or datum[-1] == recordnum[1])
        data += ((_50('Daniel'), Date(2001, 11, 13)), )
        table.append(('Daniel', Date(2001, 11, 13)))
        for datum, recordnum in zip(data, table):
            self.assertEqual(datum[0], recordnum[0])
            self.assertTrue(datum[-1] is recordnum[1] or datum[-1] == recordnum[1])
        table.close()
        table = Table(table.filename)
        table.open(mode=READ_WRITE)
        for datum, recordnum in zip(data, table):
            self.assertEqual(datum[0], recordnum[0])
            self.assertTrue(datum[-1] is recordnum[-1] or datum[-1] == recordnum[-1], "name = %s; datum[-1] = %r;  recordnum[-1] = %r" % (datum[0], datum[-1], recordnum[-1]))
        table.close()

    def test_blank_record_template_uses_null(self):
        nullable = self.null_vfp_table
        with nullable:
            rec = nullable[-1]
            self.assertTrue(rec.first is Null, "rec.first is %r" % (rec.first, ))
            self.assertTrue(rec.last == ' '*25, "rec.last is %r" % (rec.last, ))
            self.assertTrue(rec.height is Null, "rec.height is %r" % (rec.height, ))
            self.assertTrue(rec.age is None, "rec.age is %r" % (rec.age, ))
            self.assertTrue(rec.life_story is Null, "rec.life_story is %r" % (rec.life_story, ))
            self.assertTrue(rec.plans == '', "rec.plans is %r" % (rec.plans, ))
        nullable.close()
        nullable = Table(
                self.null_vfp_table.filename,
                default_data_types='enhanced',
                )
        with nullable:
            rec = nullable[-1]
            self.assertTrue(rec.first is Null, "rec.first is %r" % (rec.first, ))
            self.assertTrue(rec.last == '', "rec.last is %r" % (rec.last, ))
            self.assertTrue(rec.height is Null, "rec.height is %r" % (rec.height, ))
            self.assertTrue(rec.age is None, "rec.age is %r" % (rec.age, ))
            self.assertTrue(rec.life_story is Null, "rec.life_story is %r" % (rec.life_story, ))
            self.assertTrue(rec.plans == '', "rec.plans is %r" % (rec.plans, ))
        nullable.close()
        nullable = Table(
                self.null_vfp_table.filename,
                default_data_types=dict(
                        C=(Char, NoneType, NullType),
                        L=(Logical, NoneType, NullType),
                        D=(Date, NoneType, NullType),
                        T=(DateTime, NoneType, NullType),
                        M=(Char, NoneType, NullType),
                        ),
                )
        with nullable:
            rec = nullable[-1]
            self.assertTrue(rec.first is Null, "rec.first is %r" % (rec.first, ))
            self.assertTrue(rec.last is None, "rec.last is %r" % (rec.last, ))
            self.assertTrue(rec.height is Null, "rec.height is %r" % (rec.height, ))
            self.assertTrue(rec.age is None, "rec.age is %r" % (rec.age, ))
            self.assertTrue(rec.life_story is Null, "rec.life_story is %r" % (rec.life_story, ))
            self.assertTrue(rec.plans is None, "rec.plans is %r" % (rec.plans, ))

    def test_new_record_with_partial_fields_respects_null(self):
        nullable = self.null_vfp_table
        nullable.close()
        nullable = Table(
                self.null_vfp_table.filename,
                default_data_types=dict(
                        C=(Char, NoneType, NullType),
                        L=(Logical, NoneType, NullType),
                        D=(Date, NoneType, NullType),
                        T=(DateTime, NoneType, NullType),
                        M=(Char, NoneType, NullType),
                        ),
                )
        with nullable:
            nullable.append({'first': 'ethan', 'last':'doe'})
            rec = nullable[-1]
            self.assertTrue(rec.first == 'ethan', "rec.first is %r" % (rec.first, ))
            self.assertTrue(rec.last == 'doe', "rec.last is %r" % (rec.last, ))
            self.assertTrue(rec.height is Null, "rec.height is %r" % (rec.height, ))
            self.assertTrue(rec.age is None, "rec.age is %r" % (rec.age, ))
            self.assertTrue(rec.life_story is Null, "rec.life_story is %r" % (rec.life_story, ))
            self.assertTrue(rec.plans is None, "rec.plans is %r" % (rec.plans, ))
        nullable.close()

    def test_flux_internal(self):
        "commit and rollback of flux record (implementation detail)"
        table = self.dbf_table
        table.open(mode=READ_WRITE)
        table.append(('dbf master', True, 77, Date(2012, 5, 20), "guru of some things dbf-y"))
        record = table[-1]
        old_data = dbf.scatter(record)
        record._start_flux()
        record.name = 'novice'
        record.paid = False
        record.qty = 69
        record.orderdate = Date(2011, 1, 1)
        record.desc = 'master of all he surveys'
        try:
            self.assertEqual(
                dbf.scatter(record),
                dict(
                    name=unicode('novice                   '),
                    paid=False,
                    qty=69,
                    orderdate=datetime.date(2011, 1, 1),
                    desc='master of all he surveys',
                    ))
        finally:
            record._rollback_flux()
        self.assertEqual(old_data, dbf.scatter(record))
        record._start_flux()
        record.name = 'novice'
        record.paid = False
        record.qty = 69
        record.orderdate = Date(2011, 1, 1)
        record._commit_flux()
        self.assertEqual(
                dbf.scatter(record),
                dict(
                    name=unicode('novice                   '),
                    paid=False,
                    qty=69,
                    orderdate=datetime.date(2011, 1, 1),
                    desc='guru of some things dbf-y',
                    ))
        self.assertNotEqual(old_data, dbf.scatter(record))

    def test_field_capitalization(self):
        "ensure mixed- and upper-case field names work"
        table = dbf.Table('mixed', 'NAME C(30); Age N(5,2)', on_disk=False)
        self.assertEqual(['NAME', 'AGE'], field_names(table))
        table.open(dbf.READ_WRITE)
        table.append({'Name':'Ethan', 'AGE': 99})
        rec = table[0]
        self.assertEqual(rec.NaMe.strip(), 'Ethan')
        table.rename_field('NaMe', 'My_NAME')
        self.assertEqual(rec.My_NaMe.strip(), 'Ethan')
        self.assertEqual(['MY_NAME', 'AGE'], field_names(table))
        table.append({'MY_Name':'Allen', 'AGE': 7})
        rec = table[1]
        self.assertEqual(rec.my_NaMe.strip(), 'Allen')

class TestDbfRecordTemplates(TestCase):
    "Testing records"

    def setUp(self):
        self.dbf_table = Table(
                os.path.join(tempdir, 'dbf_table'),
                'name C(25); paid L; qty N(11,5); orderdate D; desc M',
                dbf_type='db3',
                )
        self.vfp_table = Table(
                os.path.join(tempdir, 'vfp_table'),
                'name C(25); paid L; qty N(11,5); orderdate D; desc M; mass B;' +
                ' weight F(18,3); age I; meeting T; misc G; photo P; price Y',
                dbf_type='vfp',
                )

    def tearDown(self):
        self.dbf_table.close()
        self.vfp_table.close()

    def test_dbf_storage(self):
        table = self.dbf_table
        table.open(mode=READ_WRITE)
        record = table.create_template()
        record.name = 'Stoneleaf'
        record.paid = True
        record.qty = 1
        record.orderdate = Date.today()
        record.desc = 'some Python dude'
        table.append(record)

    def test_vfp_storage(self):
        table = self.vfp_table
        table.open(mode=READ_WRITE)
        record = table.create_template()
        record.name = 'Stoneleaf'
        record.paid = True
        record.qty = 1
        record.orderdate = Date.today()
        record.desc = 'some Python dude'
        record.mass = 251.9287
        record.weight = 971204.39
        record.age = 29
        record.meeting = DateTime.now()
        record.misc = MISC
        record.photo = PHOTO
        record.price = 19.99
        table.append(record)


class TestDbfNavigation(TestCase):

    def setUp(self):
        "create a dbf and vfp table"
        self.dbf_table = table = Table(
            os.path.join(tempdir, 'temptable'),
            'name C(25); paid L; qty N(11,5); orderdate D; desc M', dbf_type='db3'
            )
        table.open(mode=READ_WRITE)
        namelist = self.dbf_namelist = []
        paidlist = self.dbf_paidlist = []
        qtylist = self.dbf_qtylist = []
        orderlist = self.dbf_orderlist = []
        desclist = self.dbf_desclist = []
        for i in range(len(floats)):
            name = '%-25s' % words[i]
            paid = len(words[i]) % 3 == 0
            qty = floats[i]
            orderdate = datetime.date((numbers[i] + 1) * 2, (numbers[i] % 12) +1, (numbers[i] % 27) + 1)
            desc = ' '.join(words[i:i+50])
            namelist.append(name)
            paidlist.append(paid)
            qtylist.append(qty)
            orderlist.append(orderdate)
            desclist.append(desc)
            table.append({'name':name, 'paid':paid, 'qty':qty, 'orderdate':orderdate, 'desc':desc})
        table.close()

        self.vfp_table = table = Table(
                os.path.join(tempdir, 'tempvfp'),
                'name C(25); paid L; qty N(11,5); orderdate D; desc M; mass B;'
                ' weight F(18,3); age I; meeting T; misc G; photo P',
                dbf_type='vfp',
                )
        table.open(mode=READ_WRITE)
        namelist = self.vfp_namelist = []
        paidlist = self.vfp_paidlist = []
        qtylist = self.vfp_qtylist = []
        orderlist = self.vfp_orderlist = []
        desclist = self.vfp_desclist = []
        masslist = self.vfp_masslist = []
        weightlist = self.vfp_weightlist = []
        agelist = self.vfp_agelist = []
        meetlist = self.vfp_meetlist = []
        misclist = self.vfp_misclist = []
        photolist = self.vfp_photolist = []
        for i in range(len(floats)):
            name = words[i]
            paid = len(words[i]) % 3 == 0
            qty = floats[i]
            orderdate = datetime.date((numbers[i] + 1) * 2, (numbers[i] % 12) +1, (numbers[i] % 27) + 1)
            desc = ' '.join(words[i:i+50])
            mass = floats[i] * floats[i] / 2.0
            weight = floats[i] * 3
            age = numbers[i]
            meeting = datetime.datetime((numbers[i] + 2000), (numbers[i] % 12)+1, (numbers[i] % 28)+1, \
                      (numbers[i] % 24), numbers[i] % 60, (numbers[i] * 3) % 60)
            misc = ' '.join(words[i:i+50:3]).encode('ascii')
            photo = ' '.join(words[i:i+50:7]).encode('ascii')
            namelist.append('%-25s' % name)
            paidlist.append(paid)
            qtylist.append(qty)
            orderlist.append(orderdate)
            desclist.append(desc)
            masslist.append(mass)
            weightlist.append(weight)
            agelist.append(age)
            meetlist.append(meeting)
            misclist.append(misc)
            photolist.append(photo)
            meeting = datetime.datetime((numbers[i] + 2000), (numbers[i] % 12)+1, (numbers[i] % 28)+1,
                      (numbers[i] % 24), numbers[i] % 60, (numbers[i] * 3) % 60)
            table.append({'name':name, 'paid':paid, 'qty':qty, 'orderdate':orderdate, 'desc':desc,
                    'mass':mass, 'weight':weight, 'age':age, 'meeting':meeting, 'misc':misc, 'photo':photo})
        table.close()

    def tearDown(self):
        self.dbf_table.close()
        self.vfp_table.close()

    def test_top(self):
        "top, current in Tables, Lists, and Indexes"
        table = self.dbf_table
        table.open(mode=READ_WRITE)
        list = List(table)
        index = Index(table, key=lambda rec: dbf.recno(rec))
        total = len(table)
        mid = total // 2
        table.goto(mid)
        list.goto(mid)
        index.goto(mid)
        self.assertTrue(table.current != -1)
        self.assertTrue(list.current != -1)
        self.assertTrue(index.current != -1)
        table.top()
        list.top()
        index.top()
        self.assertEqual(table.current, -1)
        self.assertEqual(list.current, -1)
        self.assertEqual(index.current, -1)

    def test_bottom(self):
        "bottom, current in Tables, Lists, and Indexes"
        table = self.dbf_table
        table.open(mode=READ_WRITE)
        list = List(table)
        index = Index(table, key=lambda rec: dbf.recno(rec))
        total = len(table)
        mid = total // 2
        table.goto(mid)
        list.goto(mid)
        index.goto(mid)
        self.assertTrue(table.current != -1)
        self.assertTrue(list.current != -1)
        self.assertTrue(index.current != -1)
        table.bottom()
        list.bottom()
        index.bottom()
        self.assertEqual(table.current, total)
        self.assertEqual(list.current, total)
        self.assertEqual(index.current, total)

    def test_goto(self):
        "goto, current in Tables, Lists, and Indexes"
        table = self.dbf_table
        table.open(mode=READ_WRITE)
        list = List(table)
        index = Index(table, key=lambda rec: dbf.recno(rec))
        total = len(table)
        mid = total // 2
        table.goto(mid)
        list.goto(mid)
        index.goto(mid)
        self.assertEqual(table.current, mid)
        self.assertEqual(list.current, mid)
        self.assertEqual(index.current, mid)
        table.goto('top')
        list.goto('top')
        index.goto('top')
        self.assertEqual(table.current, -1)
        self.assertEqual(list.current, -1)
        self.assertEqual(index.current, -1)
        table.goto('bottom')
        list.goto('bottom')
        index.goto('bottom')
        self.assertEqual(table.current, total)
        self.assertEqual(list.current, total)
        self.assertEqual(index.current, total)
        dbf.delete(table[10])
        self.assertTrue(dbf.is_deleted(list[10]))
        self.assertTrue(dbf.is_deleted(index[10]))
        table.goto(10)
        list.goto(10)
        index.goto(10)
        self.assertEqual(table.current, 10)
        self.assertEqual(list.current, 10)
        self.assertEqual(index.current, 10)
        table.close()

    def test_skip(self):
        "skip, current in Tables, Lists, and Indexes"
        table = self.dbf_table
        table.open(mode=READ_WRITE)
        list = List(table)
        index = Index(table, key=lambda rec: dbf.recno(rec))
        total = len(table)
        self.assertEqual(table.current, -1)
        self.assertEqual(list.current, -1)
        self.assertEqual(index.current, -1)
        table.skip(1)
        list.skip(1)
        index.skip(1)
        self.assertEqual(table.current, 0)
        self.assertEqual(list.current, 0)
        self.assertEqual(index.current, 0)
        table.skip(10)
        list.skip(10)
        index.skip(10)
        self.assertEqual(table.current, 10)
        self.assertEqual(list.current, 10)
        self.assertEqual(index.current, 10)
        table.close()

    def test_first_record(self):
        "first_record in Tables, Lists, and Indexes"
        table = self.dbf_table
        table.open(mode=READ_WRITE)
        list = List(table)
        index = Index(table, key=lambda rec: dbf.recno(rec))
        total = len(table)
        self.assertTrue(table[0] is list[0])
        self.assertTrue(table[0] is index[0])
        self.assertTrue(table.first_record is table[0])
        self.assertTrue(list.first_record is table[0])
        self.assertTrue(index.first_record is table[0])
        table.close()

    def test_prev_record(self):
        "prev_record in Tables, Lists, and Indexes"
        table = self.dbf_table
        table.open(mode=READ_WRITE)
        list = List(table)
        index = Index(table, key=lambda rec: dbf.recno(rec))
        total = len(table)
        self.assertTrue(table[0] is list[0])
        self.assertTrue(table[0] is index[0])
        table.top()
        list.top()
        index.top()
        self.assertTrue(isinstance(table.prev_record, dbf.RecordVaporWare))
        self.assertTrue(isinstance(list.prev_record, dbf.RecordVaporWare))
        self.assertTrue(isinstance(index.prev_record, dbf.RecordVaporWare))
        table.skip()
        list.skip()
        index.skip()
        self.assertTrue(isinstance(table.prev_record, dbf.RecordVaporWare))
        self.assertTrue(isinstance(list.prev_record, dbf.RecordVaporWare))
        self.assertTrue(isinstance(index.prev_record, dbf.RecordVaporWare))
        table.skip()
        list.skip()
        index.skip()
        self.assertTrue(table.prev_record is table[0])
        self.assertTrue(list.prev_record is table[0])
        self.assertTrue(index.prev_record is table[0])
        table.close()

    def test_current_record(self):
        "current_record in Tables, Lists, and Indexes"
        table = self.dbf_table
        table.open(mode=READ_WRITE)
        list = List(table)
        index = Index(table, key=lambda rec: dbf.recno(rec))
        total = len(table)
        mid = total // 2
        table.top()
        list.top()
        index.top()
        self.assertTrue(isinstance(table.current_record, dbf.RecordVaporWare))
        self.assertTrue(isinstance(list.current_record, dbf.RecordVaporWare))
        self.assertTrue(isinstance(index.current_record, dbf.RecordVaporWare))
        table.bottom()
        list.bottom()
        index.bottom()
        self.assertTrue(isinstance(table.current_record, dbf.RecordVaporWare))
        self.assertTrue(isinstance(list.current_record, dbf.RecordVaporWare))
        self.assertTrue(isinstance(index.current_record, dbf.RecordVaporWare))
        table.goto(mid)
        list.goto(mid)
        index.goto(mid)
        self.assertTrue(table.current_record is table[mid])
        self.assertTrue(list.current_record is table[mid])
        self.assertTrue(index.current_record is table[mid])
        table.close()

    def test_next_record(self):
        "prev_record in Tables, Lists, and Indexes"
        table = self.dbf_table
        table.open(mode=READ_WRITE)
        list = List(table)
        index = Index(table, key=lambda rec: dbf.recno(rec))
        total = len(table)
        self.assertTrue(table[0] is list[0])
        self.assertTrue(table[0] is index[0])
        table.bottom()
        list.bottom()
        index.bottom()
        self.assertTrue(isinstance(table.next_record, dbf.RecordVaporWare))
        self.assertTrue(isinstance(list.next_record, dbf.RecordVaporWare))
        self.assertTrue(isinstance(index.next_record, dbf.RecordVaporWare))
        table.skip(-1)
        list.skip(-1)
        index.skip(-1)
        self.assertTrue(isinstance(table.next_record, dbf.RecordVaporWare))
        self.assertTrue(isinstance(list.next_record, dbf.RecordVaporWare))
        self.assertTrue(isinstance(index.next_record, dbf.RecordVaporWare))
        table.skip(-1)
        list.skip(-1)
        index.skip(-1)
        self.assertTrue(table.next_record is table[-1])
        self.assertTrue(list.next_record is table[-1])
        self.assertTrue(index.next_record is table[-1])
        table.close()

    def test_last_record(self):
        "last_record in Tables, Lists, and Indexes"
        table = self.dbf_table
        table.open(mode=READ_WRITE)
        list = List(table)
        index = Index(table, key=lambda rec: dbf.recno(rec))
        total = len(table)
        self.assertTrue(table[-1] is list[-1])
        self.assertTrue(table[-1] is index[-1])
        self.assertTrue(table.last_record is table[-1])
        self.assertTrue(list.last_record is table[-1])
        self.assertTrue(index.last_record is table[-1])
        table.close()


class TestDbfLists(TestCase):
    "DbfList tests"

    def setUp(self):
        "create a dbf table"
        self.dbf_table = table = Table(
            os.path.join(tempdir, 'temptable'),
            'name C(25); paid L; qty N(11,5); orderdate D; desc M', dbf_type='db3'
            )
        table.open(mode=READ_WRITE)
        records = []
        for i in range(len(floats)):
            name = words[i]
            paid = len(words[i]) % 3 == 0
            qty = round(floats[i], 5)
            orderdate = datetime.date((numbers[i] + 1) * 2, (numbers[i] % 12) +1, (numbers[i] % 27) + 1)
            desc = ' '.join(words[i:i+50])
            data = {'name':name, 'paid':paid, 'qty':qty, 'orderdate':orderdate, 'desc':desc}
            table.append(data)
            records.append(data)
        table.close()
        table.open(mode=READ_WRITE)
        for trec, drec in zip(table, records):
            self.assertEqual(trec.name.strip(), drec['name'])
            self.assertEqual(trec.paid, drec['paid'])
            self.assertEqual(trec.qty, drec['qty'])
            self.assertEqual(trec.orderdate, drec['orderdate'])
            self.assertEqual(trec.desc, drec['desc'])
        table.close()

    def tearDown(self):
        self.dbf_table.close()

    def test_exceptions(self):
        table = self.dbf_table
        table.open(mode=READ_WRITE)
        list = table[::5]
        record = table[5]
        dbf.delete(record)
        self.assertTrue(list[0] is table[0])
        self.assertTrue(record in list)
        self.assertRaises(TypeError, list.__contains__, 'some string')
        self.assertRaises(TypeError, list.__getitem__, 'some string')
        self.assertRaises(TypeError, list.__delitem__, 'some string')
        self.assertRaises(TypeError, list.remove, 'some string')
        self.assertRaises(TypeError, list.index, 'some string')
        self.assertRaises(IndexError, list.__getitem__, 100)
        self.assertRaises(IndexError, list.pop, 1000)
        self.assertRaises(IndexError, list.goto, 1000)
        list.top()
        self.assertRaises(Bof, list.skip, -1)
        list.bottom()
        self.assertRaises(Eof, list.skip)
        table.pack()
        self.assertRaises(DbfError, list.__contains__, record)

        list = List()
        self.assertRaises(IndexError, list.goto, 0)
        self.assertRaises(Bof, list.skip, -1)
        self.assertRaises(Eof, list.skip)
        self.assertRaises(ValueError, list.remove, table[0])
        self.assertRaises(ValueError, list.index, table[1])

    def test_add_subtract(self):
        "addition and subtraction"
        table1 = self.dbf_table
        table1.open(mode=READ_WRITE)
        list1 = table1[::2]
        list2 = table1[::3]
        list3 = table1[:] - list1 - list2
        self.assertEqual(100, len(table1))
        self.assertEqual(list1[0], list2[0])
        self.assertEqual(list1[3], list2[2])
        self.assertEqual(50, len(list1))
        self.assertEqual(34, len(list2))
        self.assertEqual(33, len(list3))
        self.assertEqual(117, len(list1) + len(list2) + len(list3))
        self.assertEqual(len(table1), len(list1 + list2 + list3))
        self.assertEqual(67, len(list1 + list2))
        self.assertEqual(33, len(list1 - list2))
        self.assertEqual(17, len(list2 - list1))
        table1.close()

    def test_append_extend(self):
        "appending and extending"
        table1 = self.dbf_table
        table1.open(mode=READ_WRITE)
        list1 = table1[::2]
        list2 = table1[::3]
        list3 = table1[:] - list1 - list2
        list1.extend(list2)
        list2.append(table1[1])
        self.assertEqual(67, len(list1))
        self.assertEqual(35, len(list2))
        list1.append(table1[1])
        list2.extend(list3)
        self.assertEqual(68, len(list1))
        self.assertEqual(67, len(list2))
        table1.close()

    def test_index(self):
        "indexing"
        table1 = self.dbf_table
        table1.open(mode=READ_WRITE)
        list1 = table1[::2]
        list2 = table1[::3]
        list3 = table1[:] - list1 - list2
        for i, rec in enumerate(list1):
            self.assertEqual(i, list1.index(rec))
        for rec in list3:
            self.assertRaises(ValueError, list1.index, rec )
        table1.close()

    def test_sort(self):
        "sorting"
        table1 = self.dbf_table
        table1.open(mode=READ_WRITE)
        list1 = table1[::2]
        list2 = table1[::3]
        table1[:] - list1 - list2
        list4 = table1[:]
        index = table1.create_index(key = lambda rec: rec.name )
        list4.sort(key=lambda rec: rec.name)
        for trec, lrec in zip(index, list4):
            self.assertEqual(dbf.recno(trec), dbf.recno(lrec))
        table1.close()

    def test_keys(self):
        "keys"
        table1 = self.dbf_table
        table1.open(mode=READ_WRITE)
        field = table1.field_names[0]
        list1 = List(table1, key=lambda rec: rec[field])
        unique = set()
        for rec in table1:
            if rec[field] not in unique:
                unique.add(rec[field])
            else:
                self.assertRaises(NotFoundError, list1.index, rec)
                self.assertFalse(rec in list1)
            self.assertTrue(rec[field] in unique)
        self.assertEqual(len(unique), len(list1))
        table1.close()

    def test_contains(self):
        table = self.dbf_table
        table.open(mode=READ_WRITE)
        list = List(table)
        i = 0
        for record in list:
            self.assertEqual(record, list[i])
            self.assertTrue(record in list)
            self.assertTrue(tuple(record) in list)
            self.assertTrue(scatter(record) in list)
            self.assertTrue(create_template(record) in list)
            i += 1
        self.assertEqual(i, len(list))
        table.close()


class TestFieldnameLists(TestCase):
    "FieldnameList tests"

    def test_exceptions(self):
        self.assertRaises(TypeError, FieldnameList, [1])
        self.assertRaises(TypeError, FieldnameList, ([u'1toy', int]))
        list1 = FieldnameList(unicodify(['lower', 'UPPER', 'MiXeD']))
        self.assertRaises(TypeError, list1.__add__, [7])
        self.assertRaises(TypeError, list1.__contains__, 7)
        self.assertRaises(TypeError, list1.__iadd__, [7])
        self.assertRaises(TypeError, list1.__radd__, [7])
        self.assertRaises(TypeError, list1.__setitem__, 0, 7)
        self.assertRaises(TypeError, list1.append, 7)
        self.assertRaises(TypeError, list1.count, 7)
        self.assertRaises(TypeError, list1.index, 7)
        self.assertRaises(TypeError, list1.insert, 7)
        self.assertRaises(TypeError, list1.remove, 7)


    def test_create(self):
        list1 = FieldnameList(['_this', 'that', 'somemore8'])
        list2 = list(list1)
        self.assertEqual(list2, unicodify(['_THIS', 'THAT', 'SOMEMORE8']))
        self.assertEqual(list1, list2)

    def test_add(self):
        "addition"
        list1 = FieldnameList(unicodify(['lower', 'UPPER', 'MiXeD']))
        list2 = FieldnameList(['wah', u'a\xf1o'])
        list3 = FieldnameList(unicodify(['heh', 'hah']))
        #
        list4 = list1 + list2
        self.assertEqual(list1, ['Lower', 'uppeR', 'Mixed'])
        self.assertEqual(list2, unicodify(['wah', u'A\xf1o']))
        self.assertEqual(list4, unicodify(['loWer', 'UPpER', 'mixEd', 'wah', u'a\xf1O']))
        self.assertTrue(isinstance(list4, FieldnameList))
        #
        list4 += list3
        self.assertEqual(list3, unicodify(['heh', 'hah']))
        self.assertEqual(list4, unicodify(['LOWER', 'upper', 'MIxeD', 'wah', u'A\xf1O', 'heh', 'hah']))
        self.assertTrue(isinstance(list4, FieldnameList))
        #
        unicode_list = unicodify(['uhhuh', 'UhUh', 'zero'])
        self.assertEqual(unicode_list, [u'uhhuh', u'UhUh', u'zero'])
        list5 = unicode_list + list1
        self.assertEqual(list1, unicodify(['LoWeR', 'uPpEr', 'MixED']))
        self.assertEqual(list5, unicodify(['UhHuh', 'uHuH', 'zero', 'lowER', 'UPPer', 'miXeD']))
        self.assertTrue(isinstance(list5, FieldnameList))

    def test_append_extend(self):
        "appending and extending"
        list1 = FieldnameList(unicodify(['lowER', 'UPPer', 'miXeD']))
        list2 = FieldnameList(['wah', u'a\xd1o'])
        list3 = FieldnameList(unicodify(['heh', 'hah']))
        #
        list1.append('ten')
        self.assertEqual(list1, ['LOWer', 'uppER', 'MIxEd', 'ten'])
        list2.extend(unicodify(['prime', 'Maybe']))
        self.assertEqual(list2, unicodify(['wah', u'A\xd1o', 'PRIME', 'maybe']))
        #
        list3.extend(list1)
        self.assertEqual(list1, unicodify(['lower', 'UPPER', 'miXEd', 'ten']))
        self.assertEqual(list3, unicodify(['heh', 'hah', 'Lower', 'uPPER', 'MiXEd', 'ten']))

    def test_index(self):
        "indexing"
        list1 = FieldnameList(unicodify(['lOwEr', 'UpPeR', 'mIXed']))
        list2 = FieldnameList(['wah', u'a\xd1O'])
        list3 = FieldnameList(unicodify(['heh', 'hah']))
        #
        self.assertEqual(list1.index('lower'), 0)
        self.assertEqual(list2.index(u'A\xd1O'), 1)
        self.assertRaises(ValueError, list3.index, u'not there')
        self.assertRaises(ValueError, list3.index, 'not there')
        #
        slice1 = list1[:]
        slice2 = list2[:1]
        slice3 = list3[1:]
        self.assertTrue(isinstance(slice1, FieldnameList))
        self.assertTrue(isinstance(slice2, FieldnameList))
        self.assertTrue(isinstance(slice3, FieldnameList))
        self.assertEqual(slice1, ['LOWER', 'UPPER', 'MIXED'])
        self.assertEqual(slice2, unicodify(['WAH']))
        self.assertEqual(slice3, unicodify(['HAH']))

    def test_sort(self):
        "sorting"
        list1 = FieldnameList(unicodify(['LoweR', 'uPPEr', 'MiXED']))
        list2 = FieldnameList(['wah', u'A\xd1O'])
        list3 = FieldnameList(unicodify(['heh', 'hah']))
        list1.sort()
        list2.sort()
        list3.sort()
        #
        self.assertEqual(list1, ['LOWER', 'MIXED', 'UPPER'])
        self.assertEqual(list2, unicodify([u'A\xD1O', 'WAH']))
        self.assertEqual(list3, unicodify(['HAH', 'HEH']))
        self.assertFalse(list3 != list3)
        self.assertFalse(list2 < list2)
        self.assertFalse(list1 > list1)
        #
        list4 = list2[:]
        list5 = list2[:] + ['bar']
        list6 = list2[:] + unicodify(['size'])
        list4.sort()
        list5.sort()
        list6.sort()
        #
        self.assertTrue(list2 < list1)
        self.assertTrue(list2 <= list1)
        self.assertFalse(list2 == list1)
        self.assertFalse(list2 >= list1)
        self.assertFalse(list2 > list1)
        self.assertTrue(list2 == list4)
        self.assertTrue(list4 > list5)
        self.assertTrue(list5 < list6)
        self.assertTrue(list5 <= list6)
        self.assertTrue(list5 != list6)
        self.assertFalse(list5 >= list6)
        self.assertFalse(list5 > list6)
        self.assertTrue(list6 > list5)
        self.assertTrue(list6 < list4)

    def test_contains(self):
        list1 = FieldnameList(unicodify(['lower', 'UPPER', 'MiXeD']))
        list2 = FieldnameList(['wah', u'a\xf1o'])
        list3 = FieldnameList(unicodify(['heh', 'hah']))
        #
        self.assertTrue('Mixed' in list1)
        self.assertFalse(u'a\xf1o' in list1)
        self.assertTrue(u'A\xf1O' in list2)
        self.assertFalse('HEH' in list2)
        self.assertTrue(u'HEH' in list3)
        self.assertFalse(u'Mixed' in list3)


class TestReadWriteDefaultOpen(TestCase):
    "test __enter__/__exit__"

    def setUp(self):
        "create a dbf table"
        self.dbf_table = table = Table(
            os.path.join(tempdir, 'temptable'),
            'name C(25); paid L; qty N(11,5); orderdate D; desc M', dbf_type='db3'
            )
        table.open(READ_WRITE)
        table.append(('Rose Petals', True, 115, Date(2018, 2, 14), 'lightly scented, pink & red'))
        table.close()

    def tearDown(self):
        os.chmod(self.dbf_table.filename, stat.S_IWRITE|stat.S_IREAD)
        os.chmod(self.dbf_table._meta.memoname, stat.S_IWRITE|stat.S_IREAD)
        self.dbf_table.close()

    def test_context_manager(self):
        with self.dbf_table as t:
            t.append(dict(name='Stoneleaf', paid=True, qty=1))

    def test_delete_fields(self):
        dbf.delete_fields(self.dbf_table.filename, 'orderdate')

    def test_add_fields(self):
        dbf.add_fields(self.dbf_table.filename, 'alias C(25)')

    def test_processing(self):
        for rec in dbf.Process(self.dbf_table):
            rec.name = 'Carnations'

    def test_read_only(self):
        table = self.dbf_table
        os.chmod(table.filename, stat.S_IREAD)
        os.chmod(table._meta.memoname, stat.S_IREAD)
        table.open(READ_ONLY)
        table.close()
        self.assertRaises((IOError, OSError), table.open, READ_WRITE)


class TestDBC(TestCase):
    "test DBC handling"


class TestVapor(TestCase):
    "test Vapor objects"

    def test_falsey(self):
        self.assertFalse(dbf.Vapor)


class TestMisc(TestCase):
    "miscellaneous tests"

    def setUp(self):
        self.table = Table(
                os.path.join(tempdir, 'dbf_table.'),
                'name C(25); paid L; qty N(11,5); orderdate D; desc M',
                dbf_type='db3',
                )
        self.table_dbf = Table(
                os.path.join(tempdir, 'dbf_table.dbf'),
                'name C(25); paid L; qty N(11,5); orderdate D; desc M',
                dbf_type='db3',
                )
        self.table_implicit = Table(
                os.path.join(tempdir, 'dbf_table'),
                'name C(25); paid L; qty N(11,5); orderdate D; desc M',
                dbf_type='db3',
                )
        self.table_wierd = Table(
                os.path.join(tempdir, 'dbf_table.blah'),
                'name C(25); paid L; qty N(11,5); orderdate D; desc M',
                dbf_type='db3',
                )
        self.table.close()
        self.table_dbf.close()
        self.table_implicit.close()
        self.table_wierd.close()

    def test_table_type_with_dbf(self):
        dbf.table_type(self.table.filename)
        dbf.table_type(self.table_dbf.filename)
        dbf.table_type(self.table_implicit.filename)
        dbf.table_type(self.table_wierd.filename)
        dbf.Table(self.table.filename)
        dbf.Table(self.table_dbf.filename)
        dbf.Table(self.table_implicit.filename)
        dbf.Table(self.table_wierd.filename)


class TestWhatever(TestCase):
    "move tests here to run one at a time while debugging"

    def setUp(self):
        "create a dbf and vfp table"
        self.dbf_table = table = Table(
            os.path.join(tempdir, 'temptable'),
            'name C(25); paid L; qty N(11,5); orderdate D; desc M', dbf_type='db3'
            )
        table.open(mode=READ_WRITE)
        namelist = self.dbf_namelist = []
        paidlist = self.dbf_paidlist = []
        qtylist = self.dbf_qtylist = []
        orderlist = self.dbf_orderlist = []
        desclist = self.dbf_desclist = []
        for i in range(len(floats)):
            name = '%-25s' % words[i]
            paid = len(words[i]) % 3 == 0
            qty = round(floats[i], 5)
            orderdate = datetime.date((numbers[i] + 1) * 2, (numbers[i] % 12) +1, (numbers[i] % 27) + 1)
            desc = ' '.join(words[i:i+50])
            namelist.append(name)
            paidlist.append(paid)
            qtylist.append(qty)
            orderlist.append(orderdate)
            desclist.append(desc)
            table.append({'name':name, 'paid':paid, 'qty':qty, 'orderdate':orderdate, 'desc':desc})
        table.close()

        self.vfp_table = table = Table(
                os.path.join(tempdir, 'tempvfp'),
                'name C(25); paid L; qty N(11,5); orderdate D; desc M; mass B;'
                ' weight F(18,3); age I; meeting T; misc G; photo P',
                dbf_type='vfp',
                )
        table.open(mode=READ_WRITE)
        namelist = self.vfp_namelist = []
        paidlist = self.vfp_paidlist = []
        qtylist = self.vfp_qtylist = []
        orderlist = self.vfp_orderlist = []
        desclist = self.vfp_desclist = []
        masslist = self.vfp_masslist = []
        weightlist = self.vfp_weightlist = []
        agelist = self.vfp_agelist = []
        meetlist = self.vfp_meetlist = []
        misclist = self.vfp_misclist = []
        photolist = self.vfp_photolist = []
        for i in range(len(floats)):
            name = words[i]
            paid = len(words[i]) % 3 == 0
            qty = round(floats[i], 5)
            orderdate = datetime.date((numbers[i] + 1) * 2, (numbers[i] % 12) +1, (numbers[i] % 27) + 1)
            desc = ' '.join(words[i:i+50])
            mass = floats[i] * floats[i] / 2.0
            weight = round(floats[i] * 3, 3)
            age = numbers[i]
            meeting = datetime.datetime((numbers[i] + 2000), (numbers[i] % 12)+1, (numbers[i] % 28)+1, \
                      (numbers[i] % 24), numbers[i] % 60, (numbers[i] * 3) % 60)
            misc = ' '.join(words[i:i+50:3]).encode('ascii')
            photo = ' '.join(words[i:i+50:7]).encode('ascii')
            namelist.append('%-25s' % name)
            paidlist.append(paid)
            qtylist.append(qty)
            orderlist.append(orderdate)
            desclist.append(desc)
            masslist.append(mass)
            weightlist.append(weight)
            agelist.append(age)
            meetlist.append(meeting)
            misclist.append(misc)
            photolist.append(photo)
            meeting = datetime.datetime((numbers[i] + 2000), (numbers[i] % 12)+1, (numbers[i] % 28)+1,
                      (numbers[i] % 24), numbers[i] % 60, (numbers[i] * 3) % 60)
            table.append({'name':name, 'paid':paid, 'qty':qty, 'orderdate':orderdate, 'desc':desc,
                    'mass':mass, 'weight':weight, 'age':age, 'meeting':meeting, 'misc':misc, 'photo':photo})
        table.close()

    def tearDown(self):
        self.dbf_table.close()
        self.vfp_table.close()


# main
if __name__ == '__main__':
    tempdir = tempfile.mkdtemp()
    try:
        unittest.main()
    finally:
        shutil.rmtree(tempdir, True)
