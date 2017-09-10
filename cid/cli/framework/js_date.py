__all__ = ['js_date']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers([])
PyJs_Object_1_ = Js({'shortDate':Js('M/d/yyyy'),'longDate':Js('dddd, MMMM dd, yyyy'),'shortTime':Js('h:mm tt'),'longTime':Js('h:mm:ss tt'),'fullDateTime':Js('dddd, MMMM dd, yyyy h:mm:ss tt'),'sortableDateTime':Js('yyyy-MM-ddTHH:mm:ss'),'universalSortableDateTime':Js('yyyy-MM-dd HH:mm:ssZ'),'rfc1123':Js('ddd, dd MMM yyyy HH:mm:ss GMT'),'monthDay':Js('MMMM dd'),'yearMonth':Js('MMMM, yyyy')})
PyJs_Object_2_ = Js({'jan':JsRegExp('/^jan(uary)?/i'),'feb':JsRegExp('/^feb(ruary)?/i'),'mar':JsRegExp('/^mar(ch)?/i'),'apr':JsRegExp('/^apr(il)?/i'),'may':JsRegExp('/^may/i'),'jun':JsRegExp('/^jun(e)?/i'),'jul':JsRegExp('/^jul(y)?/i'),'aug':JsRegExp('/^aug(ust)?/i'),'sep':JsRegExp('/^sep(t(ember)?)?/i'),'oct':JsRegExp('/^oct(ober)?/i'),'nov':JsRegExp('/^nov(ember)?/i'),'dec':JsRegExp('/^dec(ember)?/i'),'sun':JsRegExp('/^su(n(day)?)?/i'),'mon':JsRegExp('/^mo(n(day)?)?/i'),'tue':JsRegExp('/^tu(e(s(day)?)?)?/i'),'wed':JsRegExp('/^we(d(nesday)?)?/i'),'thu':JsRegExp('/^th(u(r(s(day)?)?)?)?/i'),'fri':JsRegExp('/^fr(i(day)?)?/i'),'sat':JsRegExp('/^sa(t(urday)?)?/i'),'future':JsRegExp('/^next/i'),'past':JsRegExp('/^last|past|prev(ious)?/i'),'add':JsRegExp('/^(\\+|after|from)/i'),'subtract':JsRegExp('/^(\\-|before|ago)/i'),'yesterday':JsRegExp('/^yesterday/i'),'today':JsRegExp('/^t(oday)?/i'),'tomorrow':JsRegExp('/^tomorrow/i'),'now':JsRegExp('/^n(ow)?/i'),'millisecond':JsRegExp('/^ms|milli(second)?s?/i'),'second':JsRegExp('/^sec(ond)?s?/i'),'minute':JsRegExp('/^min(ute)?s?/i'),'hour':JsRegExp('/^h(ou)?rs?/i'),'week':JsRegExp('/^w(ee)?k/i'),'month':JsRegExp('/^m(o(nth)?s?)?/i'),'day':JsRegExp('/^d(ays?)?/i'),'year':JsRegExp('/^y((ea)?rs?)?/i'),'shortMeridian':JsRegExp('/^(a|p)/i'),'longMeridian':JsRegExp('/^(a\\.?m?\\.?|p\\.?m?\\.?)/i'),'timezone':JsRegExp('/^((e(s|d)t|c(s|d)t|m(s|d)t|p(s|d)t)|((gmt)?\\s*(\\+|\\-)\\s*\\d\\d\\d\\d?)|gmt)/i'),'ordinalSuffix':JsRegExp('/^\\s*(st|nd|rd|th)/i'),'timeContext':JsRegExp('/^\\s*(\\:|a|p)/i')})
PyJs_Object_3_ = Js({'GMT':Js('-000'),'EST':Js('-0400'),'CST':Js('-0500'),'MST':Js('-0600'),'PST':Js('-0700')})
PyJs_Object_4_ = Js({'GMT':Js('-000'),'EDT':Js('-0500'),'CDT':Js('-0600'),'MDT':Js('-0700'),'PDT':Js('-0800')})
PyJs_Object_0_ = Js({'name':Js('en-US'),'englishName':Js('English (United States)'),'nativeName':Js('English (United States)'),'dayNames':Js([Js('Sunday'), Js('Monday'), Js('Tuesday'), Js('Wednesday'), Js('Thursday'), Js('Friday'), Js('Saturday')]),'abbreviatedDayNames':Js([Js('Sun'), Js('Mon'), Js('Tue'), Js('Wed'), Js('Thu'), Js('Fri'), Js('Sat')]),'shortestDayNames':Js([Js('Su'), Js('Mo'), Js('Tu'), Js('We'), Js('Th'), Js('Fr'), Js('Sa')]),'firstLetterDayNames':Js([Js('S'), Js('M'), Js('T'), Js('W'), Js('T'), Js('F'), Js('S')]),'monthNames':Js([Js('January'), Js('February'), Js('March'), Js('April'), Js('May'), Js('June'), Js('July'), Js('August'), Js('September'), Js('October'), Js('November'), Js('December')]),'abbreviatedMonthNames':Js([Js('Jan'), Js('Feb'), Js('Mar'), Js('Apr'), Js('May'), Js('Jun'), Js('Jul'), Js('Aug'), Js('Sep'), Js('Oct'), Js('Nov'), Js('Dec')]),'amDesignator':Js('AM'),'pmDesignator':Js('PM'),'firstDayOfWeek':Js(0.0),'twoDigitYearMax':Js(2029.0),'dateElementOrder':Js('mdy'),'formatPatterns':PyJs_Object_1_,'regexPatterns':PyJs_Object_2_,'abbreviatedTimeZoneStandard':PyJs_Object_3_,'abbreviatedTimeZoneDST':PyJs_Object_4_})
var.get('Date').put('CultureInfo', PyJs_Object_0_)
@Js
def PyJs_anonymous_5_(name, this, arguments, var=var):
    var = Scope({'name':name, 'this':this, 'arguments':arguments}, var)
    var.registers(['i', 'n', 's', 'm', 'name'])
    var.put('n', var.get('Date').get('CultureInfo').get('monthNames'))
    var.put('m', var.get('Date').get('CultureInfo').get('abbreviatedMonthNames'))
    var.put('s', var.get('name').callprop('toLowerCase'))
    #for JS loop
    var.put('i', Js(0.0))
    while (var.get('i')<var.get('n').get('length')):
        try:
            if ((var.get('n').get(var.get('i')).callprop('toLowerCase')==var.get('s')) or (var.get('m').get(var.get('i')).callprop('toLowerCase')==var.get('s'))):
                return var.get('i')
        finally:
                (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
    return (-Js(1.0))
PyJs_anonymous_5_._set_name('anonymous')
var.get('Date').put('getMonthNumberFromName', PyJs_anonymous_5_)
@Js
def PyJs_anonymous_6_(name, this, arguments, var=var):
    var = Scope({'name':name, 'this':this, 'arguments':arguments}, var)
    var.registers(['i', 'n', 's', 'm', 'o', 'name'])
    var.put('n', var.get('Date').get('CultureInfo').get('dayNames'))
    var.put('m', var.get('Date').get('CultureInfo').get('abbreviatedDayNames'))
    var.put('o', var.get('Date').get('CultureInfo').get('shortestDayNames'))
    var.put('s', var.get('name').callprop('toLowerCase'))
    #for JS loop
    var.put('i', Js(0.0))
    while (var.get('i')<var.get('n').get('length')):
        try:
            if ((var.get('n').get(var.get('i')).callprop('toLowerCase')==var.get('s')) or (var.get('m').get(var.get('i')).callprop('toLowerCase')==var.get('s'))):
                return var.get('i')
        finally:
                (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
    return (-Js(1.0))
PyJs_anonymous_6_._set_name('anonymous')
var.get('Date').put('getDayNumberFromName', PyJs_anonymous_6_)
@Js
def PyJs_anonymous_7_(year, this, arguments, var=var):
    var = Scope({'year':year, 'this':this, 'arguments':arguments}, var)
    var.registers(['year'])
    return ((PyJsStrictEq((var.get('year')%Js(4.0)),Js(0.0)) and PyJsStrictNeq((var.get('year')%Js(100.0)),Js(0.0))) or PyJsStrictEq((var.get('year')%Js(400.0)),Js(0.0)))
PyJs_anonymous_7_._set_name('anonymous')
var.get('Date').put('isLeapYear', PyJs_anonymous_7_)
@Js
def PyJs_anonymous_8_(year, month, this, arguments, var=var):
    var = Scope({'year':year, 'month':month, 'this':this, 'arguments':arguments}, var)
    var.registers(['month', 'year'])
    return Js([Js(31.0), (Js(29.0) if var.get('Date').callprop('isLeapYear', var.get('year')) else Js(28.0)), Js(31.0), Js(30.0), Js(31.0), Js(30.0), Js(31.0), Js(31.0), Js(30.0), Js(31.0), Js(30.0), Js(31.0)]).get(var.get('month'))
PyJs_anonymous_8_._set_name('anonymous')
var.get('Date').put('getDaysInMonth', PyJs_anonymous_8_)
@Js
def PyJs_anonymous_9_(s, dst, this, arguments, var=var):
    var = Scope({'s':s, 'dst':dst, 'this':this, 'arguments':arguments}, var)
    var.registers(['dst', 's'])
    return (var.get('Date').get('CultureInfo').get('abbreviatedTimeZoneDST').get(var.get('s').callprop('toUpperCase')) if (var.get('dst') or Js(False)) else var.get('Date').get('CultureInfo').get('abbreviatedTimeZoneStandard').get(var.get('s').callprop('toUpperCase')))
PyJs_anonymous_9_._set_name('anonymous')
var.get('Date').put('getTimezoneOffset', PyJs_anonymous_9_)
@Js
def PyJs_anonymous_10_(offset, dst, this, arguments, var=var):
    var = Scope({'offset':offset, 'dst':dst, 'this':this, 'arguments':arguments}, var)
    var.registers(['p', 'dst', 'n', 'offset'])
    var.put('n', (var.get('Date').get('CultureInfo').get('abbreviatedTimeZoneDST') if (var.get('dst') or Js(False)) else var.get('Date').get('CultureInfo').get('abbreviatedTimeZoneStandard')))
    for PyJsTemp in var.get('n'):
        var.put('p', PyJsTemp)
        if PyJsStrictEq(var.get('n').get(var.get('p')),var.get('offset')):
            return var.get('p')
    return var.get(u"null")
PyJs_anonymous_10_._set_name('anonymous')
var.get('Date').put('getTimezoneAbbreviation', PyJs_anonymous_10_)
@Js
def PyJs_anonymous_11_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    return var.get('Date').create(var.get(u"this").callprop('getTime'))
PyJs_anonymous_11_._set_name('anonymous')
var.get('Date').get('prototype').put('clone', PyJs_anonymous_11_)
@Js
def PyJs_anonymous_12_(date, this, arguments, var=var):
    var = Scope({'date':date, 'this':this, 'arguments':arguments}, var)
    var.registers(['date'])
    if var.get('isNaN')(var.get(u"this")):
        PyJsTempException = JsToPyException(var.get('Error').create(var.get(u"this")))
        raise PyJsTempException
    if (var.get('date').instanceof(var.get('Date')) and var.get('isNaN')(var.get('date')).neg()):
        return (Js(1.0) if (var.get(u"this")>var.get('date')) else ((-Js(1.0)) if (var.get(u"this")<var.get('date')) else Js(0.0)))
    else:
        PyJsTempException = JsToPyException(var.get('TypeError').create(var.get('date')))
        raise PyJsTempException
PyJs_anonymous_12_._set_name('anonymous')
var.get('Date').get('prototype').put('compareTo', PyJs_anonymous_12_)
@Js
def PyJs_anonymous_13_(date, this, arguments, var=var):
    var = Scope({'date':date, 'this':this, 'arguments':arguments}, var)
    var.registers(['date'])
    return PyJsStrictEq(var.get(u"this").callprop('compareTo', var.get('date')),Js(0.0))
PyJs_anonymous_13_._set_name('anonymous')
var.get('Date').get('prototype').put('equals', PyJs_anonymous_13_)
@Js
def PyJs_anonymous_14_(start, end, this, arguments, var=var):
    var = Scope({'start':start, 'end':end, 'this':this, 'arguments':arguments}, var)
    var.registers(['end', 'start', 't'])
    var.put('t', var.get(u"this").callprop('getTime'))
    return ((var.get('t')>=var.get('start').callprop('getTime')) and (var.get('t')<=var.get('end').callprop('getTime')))
PyJs_anonymous_14_._set_name('anonymous')
var.get('Date').get('prototype').put('between', PyJs_anonymous_14_)
@Js
def PyJs_anonymous_15_(value, this, arguments, var=var):
    var = Scope({'value':value, 'this':this, 'arguments':arguments}, var)
    var.registers(['value'])
    var.get(u"this").callprop('setMilliseconds', (var.get(u"this").callprop('getMilliseconds')+var.get('value')))
    return var.get(u"this")
PyJs_anonymous_15_._set_name('anonymous')
var.get('Date').get('prototype').put('addMilliseconds', PyJs_anonymous_15_)
@Js
def PyJs_anonymous_16_(value, this, arguments, var=var):
    var = Scope({'value':value, 'this':this, 'arguments':arguments}, var)
    var.registers(['value'])
    return var.get(u"this").callprop('addMilliseconds', (var.get('value')*Js(1000.0)))
PyJs_anonymous_16_._set_name('anonymous')
var.get('Date').get('prototype').put('addSeconds', PyJs_anonymous_16_)
@Js
def PyJs_anonymous_17_(value, this, arguments, var=var):
    var = Scope({'value':value, 'this':this, 'arguments':arguments}, var)
    var.registers(['value'])
    return var.get(u"this").callprop('addMilliseconds', (var.get('value')*Js(60000.0)))
PyJs_anonymous_17_._set_name('anonymous')
var.get('Date').get('prototype').put('addMinutes', PyJs_anonymous_17_)
@Js
def PyJs_anonymous_18_(value, this, arguments, var=var):
    var = Scope({'value':value, 'this':this, 'arguments':arguments}, var)
    var.registers(['value'])
    return var.get(u"this").callprop('addMilliseconds', (var.get('value')*Js(3600000.0)))
PyJs_anonymous_18_._set_name('anonymous')
var.get('Date').get('prototype').put('addHours', PyJs_anonymous_18_)
@Js
def PyJs_anonymous_19_(value, this, arguments, var=var):
    var = Scope({'value':value, 'this':this, 'arguments':arguments}, var)
    var.registers(['value'])
    return var.get(u"this").callprop('addMilliseconds', (var.get('value')*Js(86400000.0)))
PyJs_anonymous_19_._set_name('anonymous')
var.get('Date').get('prototype').put('addDays', PyJs_anonymous_19_)
@Js
def PyJs_anonymous_20_(value, this, arguments, var=var):
    var = Scope({'value':value, 'this':this, 'arguments':arguments}, var)
    var.registers(['value'])
    return var.get(u"this").callprop('addMilliseconds', (var.get('value')*Js(604800000.0)))
PyJs_anonymous_20_._set_name('anonymous')
var.get('Date').get('prototype').put('addWeeks', PyJs_anonymous_20_)
@Js
def PyJs_anonymous_21_(value, this, arguments, var=var):
    var = Scope({'value':value, 'this':this, 'arguments':arguments}, var)
    var.registers(['value', 'n'])
    var.put('n', var.get(u"this").callprop('getDate'))
    var.get(u"this").callprop('setDate', Js(1.0))
    var.get(u"this").callprop('setMonth', (var.get(u"this").callprop('getMonth')+var.get('value')))
    var.get(u"this").callprop('setDate', var.get('Math').callprop('min', var.get('n'), var.get(u"this").callprop('getDaysInMonth')))
    return var.get(u"this")
PyJs_anonymous_21_._set_name('anonymous')
var.get('Date').get('prototype').put('addMonths', PyJs_anonymous_21_)
@Js
def PyJs_anonymous_22_(value, this, arguments, var=var):
    var = Scope({'value':value, 'this':this, 'arguments':arguments}, var)
    var.registers(['value'])
    return var.get(u"this").callprop('addMonths', (var.get('value')*Js(12.0)))
PyJs_anonymous_22_._set_name('anonymous')
var.get('Date').get('prototype').put('addYears', PyJs_anonymous_22_)
@Js
def PyJs_anonymous_23_(config, this, arguments, var=var):
    var = Scope({'config':config, 'this':this, 'arguments':arguments}, var)
    var.registers(['config', 'x'])
    if (var.get('config',throw=False).typeof()==Js('number')):
        var.get(u"this").put('_orient', var.get('config'))
        return var.get(u"this")
    var.put('x', var.get('config'))
    if (var.get('x').get('millisecond') or var.get('x').get('milliseconds')):
        var.get(u"this").callprop('addMilliseconds', (var.get('x').get('millisecond') or var.get('x').get('milliseconds')))
    if (var.get('x').get('second') or var.get('x').get('seconds')):
        var.get(u"this").callprop('addSeconds', (var.get('x').get('second') or var.get('x').get('seconds')))
    if (var.get('x').get('minute') or var.get('x').get('minutes')):
        var.get(u"this").callprop('addMinutes', (var.get('x').get('minute') or var.get('x').get('minutes')))
    if (var.get('x').get('hour') or var.get('x').get('hours')):
        var.get(u"this").callprop('addHours', (var.get('x').get('hour') or var.get('x').get('hours')))
    if (var.get('x').get('month') or var.get('x').get('months')):
        var.get(u"this").callprop('addMonths', (var.get('x').get('month') or var.get('x').get('months')))
    if (var.get('x').get('year') or var.get('x').get('years')):
        var.get(u"this").callprop('addYears', (var.get('x').get('year') or var.get('x').get('years')))
    if (var.get('x').get('day') or var.get('x').get('days')):
        var.get(u"this").callprop('addDays', (var.get('x').get('day') or var.get('x').get('days')))
    return var.get(u"this")
PyJs_anonymous_23_._set_name('anonymous')
var.get('Date').get('prototype').put('add', PyJs_anonymous_23_)
@Js
def PyJs_anonymous_24_(value, min, max, name, this, arguments, var=var):
    var = Scope({'value':value, 'min':min, 'max':max, 'name':name, 'this':this, 'arguments':arguments}, var)
    var.registers(['value', 'max', 'name', 'min'])
    if (var.get('value',throw=False).typeof()!=Js('number')):
        PyJsTempException = JsToPyException(var.get('TypeError').create((var.get('value')+Js(' is not a Number.'))))
        raise PyJsTempException
    else:
        if ((var.get('value')<var.get('min')) or (var.get('value')>var.get('max'))):
            PyJsTempException = JsToPyException(var.get('RangeError').create((((var.get('value')+Js(' is not a valid value for '))+var.get('name'))+Js('.'))))
            raise PyJsTempException
    return Js(True)
PyJs_anonymous_24_._set_name('anonymous')
var.get('Date').put('_validate', PyJs_anonymous_24_)
@Js
def PyJs_anonymous_25_(n, this, arguments, var=var):
    var = Scope({'n':n, 'this':this, 'arguments':arguments}, var)
    var.registers(['n'])
    return var.get('Date').callprop('_validate', var.get('n'), Js(0.0), Js(999.0), Js('milliseconds'))
PyJs_anonymous_25_._set_name('anonymous')
var.get('Date').put('validateMillisecond', PyJs_anonymous_25_)
@Js
def PyJs_anonymous_26_(n, this, arguments, var=var):
    var = Scope({'n':n, 'this':this, 'arguments':arguments}, var)
    var.registers(['n'])
    return var.get('Date').callprop('_validate', var.get('n'), Js(0.0), Js(59.0), Js('seconds'))
PyJs_anonymous_26_._set_name('anonymous')
var.get('Date').put('validateSecond', PyJs_anonymous_26_)
@Js
def PyJs_anonymous_27_(n, this, arguments, var=var):
    var = Scope({'n':n, 'this':this, 'arguments':arguments}, var)
    var.registers(['n'])
    return var.get('Date').callprop('_validate', var.get('n'), Js(0.0), Js(59.0), Js('minutes'))
PyJs_anonymous_27_._set_name('anonymous')
var.get('Date').put('validateMinute', PyJs_anonymous_27_)
@Js
def PyJs_anonymous_28_(n, this, arguments, var=var):
    var = Scope({'n':n, 'this':this, 'arguments':arguments}, var)
    var.registers(['n'])
    return var.get('Date').callprop('_validate', var.get('n'), Js(0.0), Js(23.0), Js('hours'))
PyJs_anonymous_28_._set_name('anonymous')
var.get('Date').put('validateHour', PyJs_anonymous_28_)
@Js
def PyJs_anonymous_29_(n, year, month, this, arguments, var=var):
    var = Scope({'n':n, 'year':year, 'month':month, 'this':this, 'arguments':arguments}, var)
    var.registers(['month', 'year', 'n'])
    return var.get('Date').callprop('_validate', var.get('n'), Js(1.0), var.get('Date').callprop('getDaysInMonth', var.get('year'), var.get('month')), Js('days'))
PyJs_anonymous_29_._set_name('anonymous')
var.get('Date').put('validateDay', PyJs_anonymous_29_)
@Js
def PyJs_anonymous_30_(n, this, arguments, var=var):
    var = Scope({'n':n, 'this':this, 'arguments':arguments}, var)
    var.registers(['n'])
    return var.get('Date').callprop('_validate', var.get('n'), Js(0.0), Js(11.0), Js('months'))
PyJs_anonymous_30_._set_name('anonymous')
var.get('Date').put('validateMonth', PyJs_anonymous_30_)
@Js
def PyJs_anonymous_31_(n, this, arguments, var=var):
    var = Scope({'n':n, 'this':this, 'arguments':arguments}, var)
    var.registers(['n'])
    return var.get('Date').callprop('_validate', var.get('n'), Js(1.0), Js(9999.0), Js('seconds'))
PyJs_anonymous_31_._set_name('anonymous')
var.get('Date').put('validateYear', PyJs_anonymous_31_)
@Js
def PyJs_anonymous_32_(config, this, arguments, var=var):
    var = Scope({'config':config, 'this':this, 'arguments':arguments}, var)
    var.registers(['config', 'x'])
    var.put('x', var.get('config'))
    if (var.get('x').get('millisecond').neg() and PyJsStrictNeq(var.get('x').get('millisecond'),Js(0.0))):
        var.get('x').put('millisecond', (-Js(1.0)))
    if (var.get('x').get('second').neg() and PyJsStrictNeq(var.get('x').get('second'),Js(0.0))):
        var.get('x').put('second', (-Js(1.0)))
    if (var.get('x').get('minute').neg() and PyJsStrictNeq(var.get('x').get('minute'),Js(0.0))):
        var.get('x').put('minute', (-Js(1.0)))
    if (var.get('x').get('hour').neg() and PyJsStrictNeq(var.get('x').get('hour'),Js(0.0))):
        var.get('x').put('hour', (-Js(1.0)))
    if (var.get('x').get('day').neg() and PyJsStrictNeq(var.get('x').get('day'),Js(0.0))):
        var.get('x').put('day', (-Js(1.0)))
    if (var.get('x').get('month').neg() and PyJsStrictNeq(var.get('x').get('month'),Js(0.0))):
        var.get('x').put('month', (-Js(1.0)))
    if (var.get('x').get('year').neg() and PyJsStrictNeq(var.get('x').get('year'),Js(0.0))):
        var.get('x').put('year', (-Js(1.0)))
    if ((var.get('x').get('millisecond')!=(-Js(1.0))) and var.get('Date').callprop('validateMillisecond', var.get('x').get('millisecond'))):
        var.get(u"this").callprop('addMilliseconds', (var.get('x').get('millisecond')-var.get(u"this").callprop('getMilliseconds')))
    if ((var.get('x').get('second')!=(-Js(1.0))) and var.get('Date').callprop('validateSecond', var.get('x').get('second'))):
        var.get(u"this").callprop('addSeconds', (var.get('x').get('second')-var.get(u"this").callprop('getSeconds')))
    if ((var.get('x').get('minute')!=(-Js(1.0))) and var.get('Date').callprop('validateMinute', var.get('x').get('minute'))):
        var.get(u"this").callprop('addMinutes', (var.get('x').get('minute')-var.get(u"this").callprop('getMinutes')))
    if ((var.get('x').get('hour')!=(-Js(1.0))) and var.get('Date').callprop('validateHour', var.get('x').get('hour'))):
        var.get(u"this").callprop('addHours', (var.get('x').get('hour')-var.get(u"this").callprop('getHours')))
    if (PyJsStrictNeq(var.get('x').get('month'),(-Js(1.0))) and var.get('Date').callprop('validateMonth', var.get('x').get('month'))):
        var.get(u"this").callprop('addMonths', (var.get('x').get('month')-var.get(u"this").callprop('getMonth')))
    if ((var.get('x').get('year')!=(-Js(1.0))) and var.get('Date').callprop('validateYear', var.get('x').get('year'))):
        var.get(u"this").callprop('addYears', (var.get('x').get('year')-var.get(u"this").callprop('getFullYear')))
    if ((var.get('x').get('day')!=(-Js(1.0))) and var.get('Date').callprop('validateDay', var.get('x').get('day'), var.get(u"this").callprop('getFullYear'), var.get(u"this").callprop('getMonth'))):
        var.get(u"this").callprop('addDays', (var.get('x').get('day')-var.get(u"this").callprop('getDate')))
    if var.get('x').get('timezone'):
        var.get(u"this").callprop('setTimezone', var.get('x').get('timezone'))
    if var.get('x').get('timezoneOffset'):
        var.get(u"this").callprop('setTimezoneOffset', var.get('x').get('timezoneOffset'))
    return var.get(u"this")
PyJs_anonymous_32_._set_name('anonymous')
var.get('Date').get('prototype').put('set', PyJs_anonymous_32_)
@Js
def PyJs_anonymous_33_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    var.get(u"this").callprop('setHours', Js(0.0))
    var.get(u"this").callprop('setMinutes', Js(0.0))
    var.get(u"this").callprop('setSeconds', Js(0.0))
    var.get(u"this").callprop('setMilliseconds', Js(0.0))
    return var.get(u"this")
PyJs_anonymous_33_._set_name('anonymous')
var.get('Date').get('prototype').put('clearTime', PyJs_anonymous_33_)
@Js
def PyJs_anonymous_34_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['y'])
    var.put('y', var.get(u"this").callprop('getFullYear'))
    return ((PyJsStrictEq((var.get('y')%Js(4.0)),Js(0.0)) and PyJsStrictNeq((var.get('y')%Js(100.0)),Js(0.0))) or PyJsStrictEq((var.get('y')%Js(400.0)),Js(0.0)))
PyJs_anonymous_34_._set_name('anonymous')
var.get('Date').get('prototype').put('isLeapYear', PyJs_anonymous_34_)
@Js
def PyJs_anonymous_35_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    return (var.get(u"this").callprop('is').callprop('sat') or var.get(u"this").callprop('is').callprop('sun')).neg()
PyJs_anonymous_35_._set_name('anonymous')
var.get('Date').get('prototype').put('isWeekday', PyJs_anonymous_35_)
@Js
def PyJs_anonymous_36_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    return var.get('Date').callprop('getDaysInMonth', var.get(u"this").callprop('getFullYear'), var.get(u"this").callprop('getMonth'))
PyJs_anonymous_36_._set_name('anonymous')
var.get('Date').get('prototype').put('getDaysInMonth', PyJs_anonymous_36_)
@Js
def PyJs_anonymous_37_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    PyJs_Object_38_ = Js({'day':Js(1.0)})
    return var.get(u"this").callprop('set', PyJs_Object_38_)
PyJs_anonymous_37_._set_name('anonymous')
var.get('Date').get('prototype').put('moveToFirstDayOfMonth', PyJs_anonymous_37_)
@Js
def PyJs_anonymous_39_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    PyJs_Object_40_ = Js({'day':var.get(u"this").callprop('getDaysInMonth')})
    return var.get(u"this").callprop('set', PyJs_Object_40_)
PyJs_anonymous_39_._set_name('anonymous')
var.get('Date').get('prototype').put('moveToLastDayOfMonth', PyJs_anonymous_39_)
@Js
def PyJs_anonymous_41_(day, orient, this, arguments, var=var):
    var = Scope({'day':day, 'orient':orient, 'this':this, 'arguments':arguments}, var)
    var.registers(['orient', 'diff', 'day'])
    var.put('diff', (((var.get('day')-var.get(u"this").callprop('getDay'))+(Js(7.0)*(var.get('orient') or (+Js(1.0)))))%Js(7.0)))
    return var.get(u"this").callprop('addDays', (var.put('diff', (Js(7.0)*(var.get('orient') or (+Js(1.0)))), '+') if PyJsStrictEq(var.get('diff'),Js(0.0)) else var.get('diff')))
PyJs_anonymous_41_._set_name('anonymous')
var.get('Date').get('prototype').put('moveToDayOfWeek', PyJs_anonymous_41_)
@Js
def PyJs_anonymous_42_(month, orient, this, arguments, var=var):
    var = Scope({'month':month, 'orient':orient, 'this':this, 'arguments':arguments}, var)
    var.registers(['orient', 'diff', 'month'])
    var.put('diff', (((var.get('month')-var.get(u"this").callprop('getMonth'))+(Js(12.0)*(var.get('orient') or (+Js(1.0)))))%Js(12.0)))
    return var.get(u"this").callprop('addMonths', (var.put('diff', (Js(12.0)*(var.get('orient') or (+Js(1.0)))), '+') if PyJsStrictEq(var.get('diff'),Js(0.0)) else var.get('diff')))
PyJs_anonymous_42_._set_name('anonymous')
var.get('Date').get('prototype').put('moveToMonth', PyJs_anonymous_42_)
@Js
def PyJs_anonymous_43_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    return var.get('Math').callprop('floor', ((var.get(u"this")-var.get('Date').create(var.get(u"this").callprop('getFullYear'), Js(0.0), Js(1.0)))/Js(86400000.0)))
PyJs_anonymous_43_._set_name('anonymous')
var.get('Date').get('prototype').put('getDayOfYear', PyJs_anonymous_43_)
@Js
def PyJs_anonymous_44_(firstDayOfWeek, this, arguments, var=var):
    var = Scope({'firstDayOfWeek':firstDayOfWeek, 'this':this, 'arguments':arguments}, var)
    var.registers(['dow', 'y', 'firstDayOfWeek', 'prevOffset', 'm', 'offset', 'd', 'w', 'daynum'])
    var.put('y', var.get(u"this").callprop('getFullYear'))
    var.put('m', var.get(u"this").callprop('getMonth'))
    var.put('d', var.get(u"this").callprop('getDate'))
    var.put('dow', (var.get('firstDayOfWeek') or var.get('Date').get('CultureInfo').get('firstDayOfWeek')))
    var.put('offset', ((Js(7.0)+Js(1.0))-var.get('Date').create(var.get('y'), Js(0.0), Js(1.0)).callprop('getDay')))
    if (var.get('offset')==Js(8.0)):
        var.put('offset', Js(1.0))
    var.put('daynum', (((var.get('Date').callprop('UTC', var.get('y'), var.get('m'), var.get('d'), Js(0.0), Js(0.0), Js(0.0))-var.get('Date').callprop('UTC', var.get('y'), Js(0.0), Js(1.0), Js(0.0), Js(0.0), Js(0.0)))/Js(86400000.0))+Js(1.0)))
    var.put('w', var.get('Math').callprop('floor', (((var.get('daynum')-var.get('offset'))+Js(7.0))/Js(7.0))))
    if PyJsStrictEq(var.get('w'),var.get('dow')):
        (var.put('y',Js(var.get('y').to_number())-Js(1))+Js(1))
        var.put('prevOffset', ((Js(7.0)+Js(1.0))-var.get('Date').create(var.get('y'), Js(0.0), Js(1.0)).callprop('getDay')))
        if ((var.get('prevOffset')==Js(2.0)) or (var.get('prevOffset')==Js(8.0))):
            var.put('w', Js(53.0))
        else:
            var.put('w', Js(52.0))
    return var.get('w')
PyJs_anonymous_44_._set_name('anonymous')
var.get('Date').get('prototype').put('getWeekOfYear', PyJs_anonymous_44_)
@Js
def PyJs_anonymous_45_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    var.get('console').callprop('log', Js('isDST'))
    return (var.get(u"this").callprop('toString').callprop('match', JsRegExp('/(E|C|M|P)(S|D)T/')).get('2')==Js('D'))
PyJs_anonymous_45_._set_name('anonymous')
var.get('Date').get('prototype').put('isDST', PyJs_anonymous_45_)
@Js
def PyJs_anonymous_46_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    return var.get('Date').callprop('getTimezoneAbbreviation', var.get(u"this").get('getUTCOffset'), var.get(u"this").callprop('isDST'))
PyJs_anonymous_46_._set_name('anonymous')
var.get('Date').get('prototype').put('getTimezone', PyJs_anonymous_46_)
@Js
def PyJs_anonymous_47_(s, this, arguments, var=var):
    var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
    var.registers(['there', 'here', 's'])
    var.put('here', var.get(u"this").callprop('getTimezoneOffset'))
    var.put('there', ((var.get('Number')(var.get('s'))*(-Js(6.0)))/Js(10.0)))
    var.get(u"this").callprop('addMinutes', (var.get('there')-var.get('here')))
    return var.get(u"this")
PyJs_anonymous_47_._set_name('anonymous')
var.get('Date').get('prototype').put('setTimezoneOffset', PyJs_anonymous_47_)
@Js
def PyJs_anonymous_48_(s, this, arguments, var=var):
    var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
    var.registers(['s'])
    return var.get(u"this").callprop('setTimezoneOffset', var.get('Date').callprop('getTimezoneOffset', var.get('s')))
PyJs_anonymous_48_._set_name('anonymous')
var.get('Date').get('prototype').put('setTimezone', PyJs_anonymous_48_)
@Js
def PyJs_anonymous_49_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['r', 'n'])
    var.put('n', ((var.get(u"this").callprop('getTimezoneOffset')*(-Js(10.0)))/Js(6.0)))
    if (var.get('n')<Js(0.0)):
        var.put('r', (var.get('n')-Js(10000.0)).callprop('toString'))
        return (var.get('r').get('0')+var.get('r').callprop('substr', Js(2.0)))
    else:
        var.put('r', (var.get('n')+Js(10000.0)).callprop('toString'))
        return (Js('+')+var.get('r').callprop('substr', Js(1.0)))
PyJs_anonymous_49_._set_name('anonymous')
var.get('Date').get('prototype').put('getUTCOffset', PyJs_anonymous_49_)
@Js
def PyJs_anonymous_50_(abbrev, this, arguments, var=var):
    var = Scope({'abbrev':abbrev, 'this':this, 'arguments':arguments}, var)
    var.registers(['abbrev'])
    return (var.get('Date').get('CultureInfo').get('abbreviatedDayNames').get(var.get(u"this").callprop('getDay')) if var.get('abbrev') else var.get('Date').get('CultureInfo').get('dayNames').get(var.get(u"this").callprop('getDay')))
PyJs_anonymous_50_._set_name('anonymous')
var.get('Date').get('prototype').put('getDayName', PyJs_anonymous_50_)
@Js
def PyJs_anonymous_51_(abbrev, this, arguments, var=var):
    var = Scope({'abbrev':abbrev, 'this':this, 'arguments':arguments}, var)
    var.registers(['abbrev'])
    return (var.get('Date').get('CultureInfo').get('abbreviatedMonthNames').get(var.get(u"this").callprop('getMonth')) if var.get('abbrev') else var.get('Date').get('CultureInfo').get('monthNames').get(var.get(u"this").callprop('getMonth')))
PyJs_anonymous_51_._set_name('anonymous')
var.get('Date').get('prototype').put('getMonthName', PyJs_anonymous_51_)
var.get('Date').get('prototype').put('_toString', var.get('Date').get('prototype').get('toString'))
@Js
def PyJs_anonymous_52_(format, this, arguments, var=var):
    var = Scope({'format':format, 'this':this, 'arguments':arguments}, var)
    var.registers(['p', 'self', 'format'])
    var.put('self', var.get(u"this"))
    @Js
    def PyJs_p_53_(s, this, arguments, var=var):
        var = Scope({'s':s, 'this':this, 'arguments':arguments, 'p':PyJs_p_53_}, var)
        var.registers(['s'])
        return ((Js('0')+var.get('s')) if (var.get('s').callprop('toString').get('length')==Js(1.0)) else var.get('s'))
    PyJs_p_53_._set_name('p')
    var.put('p', PyJs_p_53_)
    @Js
    def PyJs_anonymous_54_(format, this, arguments, var=var):
        var = Scope({'format':format, 'this':this, 'arguments':arguments}, var)
        var.registers(['format'])
        while 1:
            SWITCHED = False
            CONDITION = (var.get('format'))
            if SWITCHED or PyJsStrictEq(CONDITION, Js('hh')):
                SWITCHED = True
                return var.get('p')((var.get('self').callprop('getHours') if (var.get('self').callprop('getHours')<Js(13.0)) else (var.get('self').callprop('getHours')-Js(12.0))))
            if SWITCHED or PyJsStrictEq(CONDITION, Js('h')):
                SWITCHED = True
                return (var.get('self').callprop('getHours') if (var.get('self').callprop('getHours')<Js(13.0)) else (var.get('self').callprop('getHours')-Js(12.0)))
            if SWITCHED or PyJsStrictEq(CONDITION, Js('HH')):
                SWITCHED = True
                return var.get('p')(var.get('self').callprop('getHours'))
            if SWITCHED or PyJsStrictEq(CONDITION, Js('H')):
                SWITCHED = True
                return var.get('self').callprop('getHours')
            if SWITCHED or PyJsStrictEq(CONDITION, Js('mm')):
                SWITCHED = True
                return var.get('p')(var.get('self').callprop('getMinutes'))
            if SWITCHED or PyJsStrictEq(CONDITION, Js('m')):
                SWITCHED = True
                return var.get('self').callprop('getMinutes')
            if SWITCHED or PyJsStrictEq(CONDITION, Js('ss')):
                SWITCHED = True
                return var.get('p')(var.get('self').callprop('getSeconds'))
            if SWITCHED or PyJsStrictEq(CONDITION, Js('s')):
                SWITCHED = True
                return var.get('self').callprop('getSeconds')
            if SWITCHED or PyJsStrictEq(CONDITION, Js('yyyy')):
                SWITCHED = True
                return var.get('self').callprop('getFullYear')
            if SWITCHED or PyJsStrictEq(CONDITION, Js('yy')):
                SWITCHED = True
                return var.get('self').callprop('getFullYear').callprop('toString').callprop('substring', Js(2.0), Js(4.0))
            if SWITCHED or PyJsStrictEq(CONDITION, Js('dddd')):
                SWITCHED = True
                return var.get('self').callprop('getDayName')
            if SWITCHED or PyJsStrictEq(CONDITION, Js('ddd')):
                SWITCHED = True
                return var.get('self').callprop('getDayName', Js(True))
            if SWITCHED or PyJsStrictEq(CONDITION, Js('dd')):
                SWITCHED = True
                return var.get('p')(var.get('self').callprop('getDate'))
            if SWITCHED or PyJsStrictEq(CONDITION, Js('d')):
                SWITCHED = True
                return var.get('self').callprop('getDate').callprop('toString')
            if SWITCHED or PyJsStrictEq(CONDITION, Js('MMMM')):
                SWITCHED = True
                return var.get('self').callprop('getMonthName')
            if SWITCHED or PyJsStrictEq(CONDITION, Js('MMM')):
                SWITCHED = True
                return var.get('self').callprop('getMonthName', Js(True))
            if SWITCHED or PyJsStrictEq(CONDITION, Js('MM')):
                SWITCHED = True
                return var.get('p')((var.get('self').callprop('getMonth')+Js(1.0)))
            if SWITCHED or PyJsStrictEq(CONDITION, Js('M')):
                SWITCHED = True
                return (var.get('self').callprop('getMonth')+Js(1.0))
            if SWITCHED or PyJsStrictEq(CONDITION, Js('t')):
                SWITCHED = True
                return (var.get('Date').get('CultureInfo').get('amDesignator').callprop('substring', Js(0.0), Js(1.0)) if (var.get('self').callprop('getHours')<Js(12.0)) else var.get('Date').get('CultureInfo').get('pmDesignator').callprop('substring', Js(0.0), Js(1.0)))
            if SWITCHED or PyJsStrictEq(CONDITION, Js('tt')):
                SWITCHED = True
                return (var.get('Date').get('CultureInfo').get('amDesignator') if (var.get('self').callprop('getHours')<Js(12.0)) else var.get('Date').get('CultureInfo').get('pmDesignator'))
            if SWITCHED or PyJsStrictEq(CONDITION, Js('zzz')):
                SWITCHED = True
                pass
            if SWITCHED or PyJsStrictEq(CONDITION, Js('zz')):
                SWITCHED = True
                pass
            if SWITCHED or PyJsStrictEq(CONDITION, Js('z')):
                SWITCHED = True
                return Js('')
            SWITCHED = True
            break
    PyJs_anonymous_54_._set_name('anonymous')
    return (var.get('format').callprop('replace', JsRegExp('/dd?d?d?|MM?M?M?|yy?y?y?|hh?|HH?|mm?|ss?|tt?|zz?z?/g'), PyJs_anonymous_54_) if var.get('format') else var.get(u"this").callprop('_toString'))
PyJs_anonymous_52_._set_name('anonymous')
var.get('Date').get('prototype').put('toString', PyJs_anonymous_52_)
@Js
def PyJs_anonymous_55_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    return var.get('Date').create()
PyJs_anonymous_55_._set_name('anonymous')
var.get('Date').put('now', PyJs_anonymous_55_)
@Js
def PyJs_anonymous_56_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    return var.get('Date').callprop('now').callprop('clearTime')
PyJs_anonymous_56_._set_name('anonymous')
var.get('Date').put('today', PyJs_anonymous_56_)
var.get('Date').get('prototype').put('_orient', (+Js(1.0)))
@Js
def PyJs_anonymous_57_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    var.get(u"this").put('_orient', (+Js(1.0)))
    return var.get(u"this")
PyJs_anonymous_57_._set_name('anonymous')
var.get('Date').get('prototype').put('next', PyJs_anonymous_57_)
@Js
def PyJs_anonymous_58_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    var.get(u"this").put('_orient', (-Js(1.0)))
    return var.get(u"this")
PyJs_anonymous_58_._set_name('anonymous')
var.get('Date').get('prototype').put('last', var.get('Date').get('prototype').put('prev', var.get('Date').get('prototype').put('previous', PyJs_anonymous_58_)))
var.get('Date').get('prototype').put('_is', Js(False))
@Js
def PyJs_anonymous_59_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    var.get(u"this").put('_is', Js(True))
    return var.get(u"this")
PyJs_anonymous_59_._set_name('anonymous')
var.get('Date').get('prototype').put('is', PyJs_anonymous_59_)
var.get('Number').get('prototype').put('_dateElement', Js('day'))
@Js
def PyJs_anonymous_60_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['c'])
    PyJs_Object_61_ = Js({})
    var.put('c', PyJs_Object_61_)
    var.get('c').put(var.get(u"this").get('_dateElement'), var.get(u"this"))
    return var.get('Date').callprop('now').callprop('add', var.get('c'))
PyJs_anonymous_60_._set_name('anonymous')
var.get('Number').get('prototype').put('fromNow', PyJs_anonymous_60_)
@Js
def PyJs_anonymous_62_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['c'])
    PyJs_Object_63_ = Js({})
    var.put('c', PyJs_Object_63_)
    var.get('c').put(var.get(u"this").get('_dateElement'), (var.get(u"this")*(-Js(1.0))))
    return var.get('Date').callprop('now').callprop('add', var.get('c'))
PyJs_anonymous_62_._set_name('anonymous')
var.get('Number').get('prototype').put('ago', PyJs_anonymous_62_)
@Js
def PyJs_anonymous_64_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['mx', 'i', 'de', 'px', 'j', 'dx', 'ef', 'k', 'nf', 'mf', '$D', '$N', 'df'])
    var.put('$D', var.get('Date').get('prototype'))
    var.put('$N', var.get('Number').get('prototype'))
    var.put('dx', Js('sunday monday tuesday wednesday thursday friday saturday').callprop('split', JsRegExp('/\\s/')))
    var.put('mx', Js('january february march april may june july august september october november december').callprop('split', JsRegExp('/\\s/')))
    var.put('px', Js('Millisecond Second Minute Hour Day Week Month Year').callprop('split', JsRegExp('/\\s/')))
    @Js
    def PyJs_anonymous_65_(n, this, arguments, var=var):
        var = Scope({'n':n, 'this':this, 'arguments':arguments}, var)
        var.registers(['n'])
        @Js
        def PyJs_anonymous_66_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            if var.get(u"this").get('_is'):
                var.get(u"this").put('_is', Js(False))
                return (var.get(u"this").callprop('getDay')==var.get('n'))
            return var.get(u"this").callprop('moveToDayOfWeek', var.get('n'), var.get(u"this").get('_orient'))
        PyJs_anonymous_66_._set_name('anonymous')
        return PyJs_anonymous_66_
    PyJs_anonymous_65_._set_name('anonymous')
    var.put('df', PyJs_anonymous_65_)
    #for JS loop
    var.put('i', Js(0.0))
    while (var.get('i')<var.get('dx').get('length')):
        try:
            var.get('$D').put(var.get('dx').get(var.get('i')), var.get('$D').put(var.get('dx').get(var.get('i')).callprop('substring', Js(0.0), Js(3.0)), var.get('df')(var.get('i'))))
        finally:
                (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
    @Js
    def PyJs_anonymous_67_(n, this, arguments, var=var):
        var = Scope({'n':n, 'this':this, 'arguments':arguments}, var)
        var.registers(['n'])
        @Js
        def PyJs_anonymous_68_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            if var.get(u"this").get('_is'):
                var.get(u"this").put('_is', Js(False))
                return PyJsStrictEq(var.get(u"this").callprop('getMonth'),var.get('n'))
            return var.get(u"this").callprop('moveToMonth', var.get('n'), var.get(u"this").get('_orient'))
        PyJs_anonymous_68_._set_name('anonymous')
        return PyJs_anonymous_68_
    PyJs_anonymous_67_._set_name('anonymous')
    var.put('mf', PyJs_anonymous_67_)
    #for JS loop
    var.put('j', Js(0.0))
    while (var.get('j')<var.get('mx').get('length')):
        try:
            var.get('$D').put(var.get('mx').get(var.get('j')), var.get('$D').put(var.get('mx').get(var.get('j')).callprop('substring', Js(0.0), Js(3.0)), var.get('mf')(var.get('j'))))
        finally:
                (var.put('j',Js(var.get('j').to_number())+Js(1))-Js(1))
    @Js
    def PyJs_anonymous_69_(j, this, arguments, var=var):
        var = Scope({'j':j, 'this':this, 'arguments':arguments}, var)
        var.registers(['j'])
        @Js
        def PyJs_anonymous_70_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            if (var.get('j').callprop('substring', (var.get('j').get('length')-Js(1.0)))!=Js('s')):
                var.put('j', Js('s'), '+')
            return var.get(u"this").callprop((Js('add')+var.get('j')), var.get(u"this").get('_orient'))
        PyJs_anonymous_70_._set_name('anonymous')
        return PyJs_anonymous_70_
    PyJs_anonymous_69_._set_name('anonymous')
    var.put('ef', PyJs_anonymous_69_)
    @Js
    def PyJs_anonymous_71_(n, this, arguments, var=var):
        var = Scope({'n':n, 'this':this, 'arguments':arguments}, var)
        var.registers(['n'])
        @Js
        def PyJs_anonymous_72_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            var.get(u"this").put('_dateElement', var.get('n'))
            return var.get(u"this")
        PyJs_anonymous_72_._set_name('anonymous')
        return PyJs_anonymous_72_
    PyJs_anonymous_71_._set_name('anonymous')
    var.put('nf', PyJs_anonymous_71_)
    #for JS loop
    var.put('k', Js(0.0))
    while (var.get('k')<var.get('px').get('length')):
        try:
            var.put('de', var.get('px').get(var.get('k')).callprop('toLowerCase'))
            var.get('$D').put(var.get('de'), var.get('$D').put((var.get('de')+Js('s')), var.get('ef')(var.get('px').get(var.get('k')))))
            var.get('$N').put(var.get('de'), var.get('$N').put((var.get('de')+Js('s')), var.get('nf')(var.get('de'))))
        finally:
                (var.put('k',Js(var.get('k').to_number())+Js(1))-Js(1))
PyJs_anonymous_64_._set_name('anonymous')
PyJs_anonymous_64_()
@Js
def PyJs_anonymous_73_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    return var.get(u"this").callprop('toString', Js('yyyy-MM-ddThh:mm:ssZ'))
PyJs_anonymous_73_._set_name('anonymous')
var.get('Date').get('prototype').put('toJSONString', PyJs_anonymous_73_)
@Js
def PyJs_anonymous_74_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    return var.get(u"this").callprop('toString', var.get('Date').get('CultureInfo').get('formatPatterns').get('shortDatePattern'))
PyJs_anonymous_74_._set_name('anonymous')
var.get('Date').get('prototype').put('toShortDateString', PyJs_anonymous_74_)
@Js
def PyJs_anonymous_75_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    return var.get(u"this").callprop('toString', var.get('Date').get('CultureInfo').get('formatPatterns').get('longDatePattern'))
PyJs_anonymous_75_._set_name('anonymous')
var.get('Date').get('prototype').put('toLongDateString', PyJs_anonymous_75_)
@Js
def PyJs_anonymous_76_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    return var.get(u"this").callprop('toString', var.get('Date').get('CultureInfo').get('formatPatterns').get('shortTimePattern'))
PyJs_anonymous_76_._set_name('anonymous')
var.get('Date').get('prototype').put('toShortTimeString', PyJs_anonymous_76_)
@Js
def PyJs_anonymous_77_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    return var.get(u"this").callprop('toString', var.get('Date').get('CultureInfo').get('formatPatterns').get('longTimePattern'))
PyJs_anonymous_77_._set_name('anonymous')
var.get('Date').get('prototype').put('toLongTimeString', PyJs_anonymous_77_)
@Js
def PyJs_anonymous_78_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers([])
    while 1:
        SWITCHED = False
        CONDITION = (var.get(u"this").callprop('getDate'))
        if SWITCHED or PyJsStrictEq(CONDITION, Js(1.0)):
            SWITCHED = True
            pass
        if SWITCHED or PyJsStrictEq(CONDITION, Js(21.0)):
            SWITCHED = True
            pass
        if SWITCHED or PyJsStrictEq(CONDITION, Js(31.0)):
            SWITCHED = True
            return Js('st')
        if SWITCHED or PyJsStrictEq(CONDITION, Js(2.0)):
            SWITCHED = True
            pass
        if SWITCHED or PyJsStrictEq(CONDITION, Js(22.0)):
            SWITCHED = True
            return Js('nd')
        if SWITCHED or PyJsStrictEq(CONDITION, Js(3.0)):
            SWITCHED = True
            pass
        if SWITCHED or PyJsStrictEq(CONDITION, Js(23.0)):
            SWITCHED = True
            return Js('rd')
        if True:
            SWITCHED = True
            return Js('th')
        SWITCHED = True
        break
PyJs_anonymous_78_._set_name('anonymous')
var.get('Date').get('prototype').put('getOrdinal', PyJs_anonymous_78_)
@Js
def PyJs_anonymous_79_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['_', 'gx', '_vector', 'i', '_generator', 'vx', '$P', 'j'])
    @Js
    def PyJs_anonymous_81_(s, this, arguments, var=var):
        var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
        var.registers(['s'])
        var.get(u"this").put('message', ((Js("Parse error at '")+var.get('s').callprop('substring', Js(0.0), Js(10.0)))+Js(" ...'")))
    PyJs_anonymous_81_._set_name('anonymous')
    PyJs_Object_80_ = Js({'Exception':PyJs_anonymous_81_})
    var.get('Date').put('Parsing', PyJs_Object_80_)
    var.put('$P', var.get('Date').get('Parsing'))
    @Js
    def PyJs_anonymous_83_(r, this, arguments, var=var):
        var = Scope({'r':r, 'this':this, 'arguments':arguments}, var)
        var.registers(['r'])
        @Js
        def PyJs_anonymous_84_(s, this, arguments, var=var):
            var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
            var.registers(['s', 'mx'])
            var.put('mx', var.get('s').callprop('match', var.get('r')))
            if var.get('mx'):
                return Js([var.get('mx').get('0'), var.get('s').callprop('substring', var.get('mx').get('0').get('length'))])
            else:
                PyJsTempException = JsToPyException(var.get('$P').get('Exception').create(var.get('s')))
                raise PyJsTempException
        PyJs_anonymous_84_._set_name('anonymous')
        return PyJs_anonymous_84_
    PyJs_anonymous_83_._set_name('anonymous')
    @Js
    def PyJs_anonymous_85_(s, this, arguments, var=var):
        var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
        var.registers(['s'])
        @Js
        def PyJs_anonymous_86_(s, this, arguments, var=var):
            var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
            var.registers(['s'])
            return var.get('_').callprop('rtoken', var.get('RegExp').create(((Js('^s*')+var.get('s'))+Js('s*'))))(var.get('s'))
        PyJs_anonymous_86_._set_name('anonymous')
        return PyJs_anonymous_86_
    PyJs_anonymous_85_._set_name('anonymous')
    @Js
    def PyJs_anonymous_87_(s, this, arguments, var=var):
        var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
        var.registers(['s'])
        return var.get('_').callprop('rtoken', var.get('RegExp').create((Js('^')+var.get('s'))))
    PyJs_anonymous_87_._set_name('anonymous')
    @Js
    def PyJs_anonymous_88_(p, this, arguments, var=var):
        var = Scope({'p':p, 'this':this, 'arguments':arguments}, var)
        var.registers(['p'])
        @Js
        def PyJs_anonymous_89_(s, this, arguments, var=var):
            var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
            var.registers(['rx', 'qx', 's'])
            var.put('qx', Js([]))
            var.put('rx', var.get(u"null"))
            while var.get('s').get('length'):
                try:
                    var.put('rx', var.get('p').callprop('call', var.get(u"this"), var.get('s')))
                except PyJsException as PyJsTempException:
                    PyJsHolder_65_2971719 = var.own.get('e')
                    var.force_own_put('e', PyExceptionToJs(PyJsTempException))
                    try:
                        var.get('qx').callprop('push', var.get('rx').get('0'))
                        var.put('s', var.get('rx').get('1'))
                        continue
                    finally:
                        if PyJsHolder_65_2971719 is not None:
                            var.own['e'] = PyJsHolder_65_2971719
                        else:
                            del var.own['e']
                        del PyJsHolder_65_2971719
                break
            return Js([var.get('qx'), var.get('s')])
        PyJs_anonymous_89_._set_name('anonymous')
        return PyJs_anonymous_89_
    PyJs_anonymous_88_._set_name('anonymous')
    @Js
    def PyJs_anonymous_90_(p, this, arguments, var=var):
        var = Scope({'p':p, 'this':this, 'arguments':arguments}, var)
        var.registers(['p'])
        @Js
        def PyJs_anonymous_91_(s, this, arguments, var=var):
            var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
            var.registers(['r', 'rx', 's'])
            var.put('rx', Js([]))
            var.put('r', var.get(u"null"))
            while var.get('s').get('length'):
                try:
                    var.put('r', var.get('p').callprop('call', var.get(u"this"), var.get('s')))
                except PyJsException as PyJsTempException:
                    PyJsHolder_65_71953070 = var.own.get('e')
                    var.force_own_put('e', PyExceptionToJs(PyJsTempException))
                    try:
                        return Js([var.get('rx'), var.get('s')])
                    finally:
                        if PyJsHolder_65_71953070 is not None:
                            var.own['e'] = PyJsHolder_65_71953070
                        else:
                            del var.own['e']
                        del PyJsHolder_65_71953070
                var.get('rx').callprop('push', var.get('r').get('0'))
                var.put('s', var.get('r').get('1'))
            return Js([var.get('rx'), var.get('s')])
        PyJs_anonymous_91_._set_name('anonymous')
        return PyJs_anonymous_91_
    PyJs_anonymous_90_._set_name('anonymous')
    @Js
    def PyJs_anonymous_92_(p, this, arguments, var=var):
        var = Scope({'p':p, 'this':this, 'arguments':arguments}, var)
        var.registers(['p'])
        @Js
        def PyJs_anonymous_93_(s, this, arguments, var=var):
            var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
            var.registers(['r', 's'])
            var.put('r', var.get(u"null"))
            try:
                var.put('r', var.get('p').callprop('call', var.get(u"this"), var.get('s')))
            except PyJsException as PyJsTempException:
                PyJsHolder_65_84358109 = var.own.get('e')
                var.force_own_put('e', PyExceptionToJs(PyJsTempException))
                try:
                    return Js([var.get(u"null"), var.get('s')])
                finally:
                    if PyJsHolder_65_84358109 is not None:
                        var.own['e'] = PyJsHolder_65_84358109
                    else:
                        del var.own['e']
                    del PyJsHolder_65_84358109
            return Js([var.get('r').get('0'), var.get('r').get('1')])
        PyJs_anonymous_93_._set_name('anonymous')
        return PyJs_anonymous_93_
    PyJs_anonymous_92_._set_name('anonymous')
    @Js
    def PyJs_anonymous_94_(p, this, arguments, var=var):
        var = Scope({'p':p, 'this':this, 'arguments':arguments}, var)
        var.registers(['p'])
        @Js
        def PyJs_anonymous_95_(s, this, arguments, var=var):
            var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
            var.registers(['s'])
            try:
                var.get('p').callprop('call', var.get(u"this"), var.get('s'))
            except PyJsException as PyJsTempException:
                PyJsHolder_65_67393771 = var.own.get('e')
                var.force_own_put('e', PyExceptionToJs(PyJsTempException))
                try:
                    return Js([var.get(u"null"), var.get('s')])
                finally:
                    if PyJsHolder_65_67393771 is not None:
                        var.own['e'] = PyJsHolder_65_67393771
                    else:
                        del var.own['e']
                    del PyJsHolder_65_67393771
            PyJsTempException = JsToPyException(var.get('$P').get('Exception').create(var.get('s')))
            raise PyJsTempException
        PyJs_anonymous_95_._set_name('anonymous')
        return PyJs_anonymous_95_
    PyJs_anonymous_94_._set_name('anonymous')
    @Js
    def PyJs_anonymous_96_(p, this, arguments, var=var):
        var = Scope({'p':p, 'this':this, 'arguments':arguments}, var)
        var.registers(['p'])
        @Js
        def PyJs_anonymous_97_(s, this, arguments, var=var):
            var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
            var.registers(['r', 's'])
            var.put('r', var.get(u"null"))
            var.put('r', var.get('p').callprop('call', var.get(u"this"), var.get('s')))
            return Js([var.get(u"null"), var.get('r').get('1')])
        PyJs_anonymous_97_._set_name('anonymous')
        return (PyJs_anonymous_97_ if var.get('p') else var.get(u"null"))
    PyJs_anonymous_96_._set_name('anonymous')
    @Js
    def PyJs_anonymous_98_(this, arguments, var=var):
        var = Scope({'this':this, 'arguments':arguments}, var)
        var.registers(['rx', 'i', 'px', 'qx'])
        var.put('px', var.get('arguments').get('0'))
        var.put('qx', var.get('Array').get('prototype').get('slice').callprop('call', var.get('arguments'), Js(1.0)))
        var.put('rx', Js([]))
        #for JS loop
        var.put('i', Js(0.0))
        while (var.get('i')<var.get('px').get('length')):
            try:
                var.get('rx').callprop('push', var.get('_').callprop('each', var.get('px').get(var.get('i')), var.get('qx')))
            finally:
                    (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
        return var.get('rx')
    PyJs_anonymous_98_._set_name('anonymous')
    @Js
    def PyJs_anonymous_99_(rule, this, arguments, var=var):
        var = Scope({'rule':rule, 'this':this, 'arguments':arguments}, var)
        var.registers(['r', 'rule', 'cache'])
        PyJs_Object_100_ = Js({})
        var.put('cache', PyJs_Object_100_)
        var.put('r', var.get(u"null"))
        @Js
        def PyJs_anonymous_101_(s, this, arguments, var=var):
            var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
            var.registers(['s'])
            try:
                var.put('r', var.get('cache').put(var.get('s'), (var.get('cache').get(var.get('s')) or var.get('rule').callprop('call', var.get(u"this"), var.get('s')))))
            except PyJsException as PyJsTempException:
                PyJsHolder_65_42142607 = var.own.get('e')
                var.force_own_put('e', PyExceptionToJs(PyJsTempException))
                try:
                    var.put('r', var.get('cache').put(var.get('s'), var.get('e')))
                finally:
                    if PyJsHolder_65_42142607 is not None:
                        var.own['e'] = PyJsHolder_65_42142607
                    else:
                        del var.own['e']
                    del PyJsHolder_65_42142607
            if var.get('r').instanceof(var.get('$P').get('Exception')):
                PyJsTempException = JsToPyException(var.get('r'))
                raise PyJsTempException
            else:
                return var.get('r')
        PyJs_anonymous_101_._set_name('anonymous')
        return PyJs_anonymous_101_
    PyJs_anonymous_99_._set_name('anonymous')
    @Js
    def PyJs_anonymous_102_(this, arguments, var=var):
        var = Scope({'this':this, 'arguments':arguments}, var)
        var.registers(['px'])
        var.put('px', var.get('arguments'))
        @Js
        def PyJs_anonymous_103_(s, this, arguments, var=var):
            var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
            var.registers(['r', 's', 'i'])
            var.put('r', var.get(u"null"))
            #for JS loop
            var.put('i', Js(0.0))
            while (var.get('i')<var.get('px').get('length')):
                try:
                    if (var.get('px').get(var.get('i'))==var.get(u"null")):
                        continue
                    try:
                        var.put('r', var.get('px').get(var.get('i')).callprop('call', var.get(u"this"), var.get('s')))
                    except PyJsException as PyJsTempException:
                        PyJsHolder_65_46440570 = var.own.get('e')
                        var.force_own_put('e', PyExceptionToJs(PyJsTempException))
                        try:
                            var.put('r', var.get(u"null"))
                        finally:
                            if PyJsHolder_65_46440570 is not None:
                                var.own['e'] = PyJsHolder_65_46440570
                            else:
                                del var.own['e']
                            del PyJsHolder_65_46440570
                    if var.get('r'):
                        return var.get('r')
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            PyJsTempException = JsToPyException(var.get('$P').get('Exception').create(var.get('s')))
            raise PyJsTempException
        PyJs_anonymous_103_._set_name('anonymous')
        return PyJs_anonymous_103_
    PyJs_anonymous_102_._set_name('anonymous')
    @Js
    def PyJs_anonymous_104_(this, arguments, var=var):
        var = Scope({'this':this, 'arguments':arguments}, var)
        var.registers(['px'])
        var.put('px', var.get('arguments'))
        @Js
        def PyJs_anonymous_105_(s, this, arguments, var=var):
            var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
            var.registers(['r', 's', 'rx', 'i'])
            var.put('rx', Js([]))
            var.put('r', var.get(u"null"))
            #for JS loop
            var.put('i', Js(0.0))
            while (var.get('i')<var.get('px').get('length')):
                try:
                    if (var.get('px').get(var.get('i'))==var.get(u"null")):
                        continue
                    try:
                        var.put('r', var.get('px').get(var.get('i')).callprop('call', var.get(u"this"), var.get('s')))
                    except PyJsException as PyJsTempException:
                        PyJsHolder_65_62031249 = var.own.get('e')
                        var.force_own_put('e', PyExceptionToJs(PyJsTempException))
                        try:
                            PyJsTempException = JsToPyException(var.get('$P').get('Exception').create(var.get('s')))
                            raise PyJsTempException
                        finally:
                            if PyJsHolder_65_62031249 is not None:
                                var.own['e'] = PyJsHolder_65_62031249
                            else:
                                del var.own['e']
                            del PyJsHolder_65_62031249
                    var.get('rx').callprop('push', var.get('r').get('0'))
                    var.put('s', var.get('r').get('1'))
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            return Js([var.get('rx'), var.get('s')])
        PyJs_anonymous_105_._set_name('anonymous')
        return PyJs_anonymous_105_
    PyJs_anonymous_104_._set_name('anonymous')
    @Js
    def PyJs_anonymous_106_(this, arguments, var=var):
        var = Scope({'this':this, 'arguments':arguments}, var)
        var.registers(['_', 'px'])
        var.put('px', var.get('arguments'))
        var.put('_', var.get('_'))
        return var.get('_').callprop('each', var.get('_').callprop('optional', var.get('px')))
    PyJs_anonymous_106_._set_name('anonymous')
    @Js
    def PyJs_anonymous_107_(px, d, c, this, arguments, var=var):
        var = Scope({'px':px, 'd':d, 'c':c, 'this':this, 'arguments':arguments}, var)
        var.registers(['d', 'c', 'px'])
        var.put('d', (var.get('d') or var.get('_').callprop('rtoken', JsRegExp('/^\\s*/'))))
        var.put('c', (var.get('c') or var.get(u"null")))
        if (var.get('px').get('length')==Js(1.0)):
            return var.get('px').get('0')
        @Js
        def PyJs_anonymous_108_(s, this, arguments, var=var):
            var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
            var.registers(['r', 'q', 'i', 's', 'rx'])
            var.put('r', var.get(u"null"))
            var.put('q', var.get(u"null"))
            var.put('rx', Js([]))
            #for JS loop
            var.put('i', Js(0.0))
            while (var.get('i')<var.get('px').get('length')):
                try:
                    try:
                        var.put('r', var.get('px').get(var.get('i')).callprop('call', var.get(u"this"), var.get('s')))
                    except PyJsException as PyJsTempException:
                        PyJsHolder_65_58412874 = var.own.get('e')
                        var.force_own_put('e', PyExceptionToJs(PyJsTempException))
                        try:
                            break
                        finally:
                            if PyJsHolder_65_58412874 is not None:
                                var.own['e'] = PyJsHolder_65_58412874
                            else:
                                del var.own['e']
                            del PyJsHolder_65_58412874
                    var.get('rx').callprop('push', var.get('r').get('0'))
                    try:
                        var.put('q', var.get('d').callprop('call', var.get(u"this"), var.get('r').get('1')))
                    except PyJsException as PyJsTempException:
                        PyJsHolder_6578_22494441 = var.own.get('ex')
                        var.force_own_put('ex', PyExceptionToJs(PyJsTempException))
                        try:
                            var.put('q', var.get(u"null"))
                            break
                        finally:
                            if PyJsHolder_6578_22494441 is not None:
                                var.own['ex'] = PyJsHolder_6578_22494441
                            else:
                                del var.own['ex']
                            del PyJsHolder_6578_22494441
                    var.put('s', var.get('q').get('1'))
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            if var.get('r').neg():
                PyJsTempException = JsToPyException(var.get('$P').get('Exception').create(var.get('s')))
                raise PyJsTempException
            if var.get('q'):
                PyJsTempException = JsToPyException(var.get('$P').get('Exception').create(var.get('q').get('1')))
                raise PyJsTempException
            if var.get('c'):
                try:
                    var.put('r', var.get('c').callprop('call', var.get(u"this"), var.get('r').get('1')))
                except PyJsException as PyJsTempException:
                    PyJsHolder_6579_19745732 = var.own.get('ey')
                    var.force_own_put('ey', PyExceptionToJs(PyJsTempException))
                    try:
                        PyJsTempException = JsToPyException(var.get('$P').get('Exception').create(var.get('r').get('1')))
                        raise PyJsTempException
                    finally:
                        if PyJsHolder_6579_19745732 is not None:
                            var.own['ey'] = PyJsHolder_6579_19745732
                        else:
                            del var.own['ey']
                        del PyJsHolder_6579_19745732
            return Js([var.get('rx'), (var.get('r').get('1') if var.get('r') else var.get('s'))])
        PyJs_anonymous_108_._set_name('anonymous')
        return PyJs_anonymous_108_
    PyJs_anonymous_107_._set_name('anonymous')
    @Js
    def PyJs_anonymous_109_(d1, p, d2, this, arguments, var=var):
        var = Scope({'d1':d1, 'p':p, 'd2':d2, 'this':this, 'arguments':arguments}, var)
        var.registers(['p', 'd2', 'd1', '_fn'])
        var.put('d2', (var.get('d2') or var.get('d1')))
        var.put('_fn', var.get('_').callprop('each', var.get('_').callprop('ignore', var.get('d1')), var.get('p'), var.get('_').callprop('ignore', var.get('d2'))))
        @Js
        def PyJs_anonymous_110_(s, this, arguments, var=var):
            var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
            var.registers(['rx', 's'])
            var.put('rx', var.get('_fn').callprop('call', var.get(u"this"), var.get('s')))
            return Js([Js([var.get('rx').get('0').get('0'), var.get('r').get('0').get('2')]), var.get('rx').get('1')])
        PyJs_anonymous_110_._set_name('anonymous')
        return PyJs_anonymous_110_
    PyJs_anonymous_109_._set_name('anonymous')
    @Js
    def PyJs_anonymous_111_(p, d, c, this, arguments, var=var):
        var = Scope({'p':p, 'd':d, 'c':c, 'this':this, 'arguments':arguments}, var)
        var.registers(['d', 'p', 'c'])
        var.put('d', (var.get('d') or var.get('_').callprop('rtoken', JsRegExp('/^\\s*/'))))
        var.put('c', (var.get('c') or var.get(u"null")))
        def PyJs_LONG_112_(var=var):
            return (var.get('_').callprop('each', var.get('_').callprop('product', var.get('p').callprop('slice', Js(0.0), (-Js(1.0))), var.get('_').callprop('ignore', var.get('d'))), var.get('p').callprop('slice', (-Js(1.0))), var.get('_').callprop('ignore', var.get('c'))) if var.get('p').instanceof(var.get('Array')) else var.get('_').callprop('each', var.get('_').callprop('many', var.get('_').callprop('each', var.get('p'), var.get('_').callprop('ignore', var.get('d')))), var.get('px'), var.get('_').callprop('ignore', var.get('c'))))
        return PyJs_LONG_112_()
    PyJs_anonymous_111_._set_name('anonymous')
    @Js
    def PyJs_anonymous_113_(px, d, c, this, arguments, var=var):
        var = Scope({'px':px, 'd':d, 'c':c, 'this':this, 'arguments':arguments}, var)
        var.registers(['d', 'c', 'px'])
        var.put('d', (var.get('d') or var.get('_').callprop('rtoken', JsRegExp('/^\\s*/'))))
        var.put('c', (var.get('c') or var.get(u"null")))
        @Js
        def PyJs_anonymous_114_(s, this, arguments, var=var):
            var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
            var.registers(['r', 'q', 'i', 'qx', 's', 'p', 'rx', 'best', 'last', 'j'])
            var.put('r', var.get(u"null"))
            var.put('p', var.get(u"null"))
            var.put('q', var.get(u"null"))
            var.put('rx', var.get(u"null"))
            var.put('best', Js([Js([]), var.get('s')]))
            var.put('last', Js(False))
            #for JS loop
            var.put('i', Js(0.0))
            while (var.get('i')<var.get('px').get('length')):
                try:
                    var.put('q', var.get(u"null"))
                    var.put('p', var.get(u"null"))
                    var.put('r', var.get(u"null"))
                    var.put('last', (var.get('px').get('length')==Js(1.0)))
                    try:
                        var.put('r', var.get('px').get(var.get('i')).callprop('call', var.get(u"this"), var.get('s')))
                    except PyJsException as PyJsTempException:
                        PyJsHolder_65_13199495 = var.own.get('e')
                        var.force_own_put('e', PyExceptionToJs(PyJsTempException))
                        try:
                            continue
                        finally:
                            if PyJsHolder_65_13199495 is not None:
                                var.own['e'] = PyJsHolder_65_13199495
                            else:
                                del var.own['e']
                            del PyJsHolder_65_13199495
                    var.put('rx', Js([Js([var.get('r').get('0')]), var.get('r').get('1')]))
                    if ((var.get('r').get('1').get('length')>Js(0.0)) and var.get('last').neg()):
                        try:
                            var.put('q', var.get('d').callprop('call', var.get(u"this"), var.get('r').get('1')))
                        except PyJsException as PyJsTempException:
                            PyJsHolder_6578_33527988 = var.own.get('ex')
                            var.force_own_put('ex', PyExceptionToJs(PyJsTempException))
                            try:
                                var.put('last', Js(True))
                            finally:
                                if PyJsHolder_6578_33527988 is not None:
                                    var.own['ex'] = PyJsHolder_6578_33527988
                                else:
                                    del var.own['ex']
                                del PyJsHolder_6578_33527988
                    else:
                        var.put('last', Js(True))
                    if (var.get('last').neg() and PyJsStrictEq(var.get('q').get('1').get('length'),Js(0.0))):
                        var.put('last', Js(True))
                    if var.get('last').neg():
                        var.put('qx', Js([]))
                        #for JS loop
                        var.put('j', Js(0.0))
                        while (var.get('j')<var.get('px').get('length')):
                            try:
                                if (var.get('i')!=var.get('j')):
                                    var.get('qx').callprop('push', var.get('px').get(var.get('j')))
                            finally:
                                    (var.put('j',Js(var.get('j').to_number())+Js(1))-Js(1))
                        var.put('p', var.get('_').callprop('set', var.get('qx'), var.get('d')).callprop('call', var.get(u"this"), var.get('q').get('1')))
                        if (var.get('p').get('0').get('length')>Js(0.0)):
                            var.get('rx').put('0', var.get('rx').get('0').callprop('concat', var.get('p').get('0')))
                            var.get('rx').put('1', var.get('p').get('1'))
                    if (var.get('rx').get('1').get('length')<var.get('best').get('1').get('length')):
                        var.put('best', var.get('rx'))
                    if PyJsStrictEq(var.get('best').get('1').get('length'),Js(0.0)):
                        break
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            if PyJsStrictEq(var.get('best').get('0').get('length'),Js(0.0)):
                return var.get('best')
            if var.get('c'):
                try:
                    var.put('q', var.get('c').callprop('call', var.get(u"this"), var.get('best').get('1')))
                except PyJsException as PyJsTempException:
                    PyJsHolder_6579_6439637 = var.own.get('ey')
                    var.force_own_put('ey', PyExceptionToJs(PyJsTempException))
                    try:
                        PyJsTempException = JsToPyException(var.get('$P').get('Exception').create(var.get('best').get('1')))
                        raise PyJsTempException
                    finally:
                        if PyJsHolder_6579_6439637 is not None:
                            var.own['ey'] = PyJsHolder_6579_6439637
                        else:
                            del var.own['ey']
                        del PyJsHolder_6579_6439637
                var.get('best').put('1', var.get('q').get('1'))
            return var.get('best')
        PyJs_anonymous_114_._set_name('anonymous')
        return PyJs_anonymous_114_
    PyJs_anonymous_113_._set_name('anonymous')
    @Js
    def PyJs_anonymous_115_(gr, fname, this, arguments, var=var):
        var = Scope({'gr':gr, 'fname':fname, 'this':this, 'arguments':arguments}, var)
        var.registers(['fname', 'gr'])
        @Js
        def PyJs_anonymous_116_(s, this, arguments, var=var):
            var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
            var.registers(['s'])
            return var.get('gr').get(var.get('fname')).callprop('call', var.get(u"this"), var.get('s'))
        PyJs_anonymous_116_._set_name('anonymous')
        return PyJs_anonymous_116_
    PyJs_anonymous_115_._set_name('anonymous')
    @Js
    def PyJs_anonymous_117_(rule, repl, this, arguments, var=var):
        var = Scope({'rule':rule, 'repl':repl, 'this':this, 'arguments':arguments}, var)
        var.registers(['repl', 'rule'])
        @Js
        def PyJs_anonymous_118_(s, this, arguments, var=var):
            var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
            var.registers(['r', 's'])
            var.put('r', var.get('rule').callprop('call', var.get(u"this"), var.get('s')))
            return Js([var.get('repl'), var.get('r').get('1')])
        PyJs_anonymous_118_._set_name('anonymous')
        return PyJs_anonymous_118_
    PyJs_anonymous_117_._set_name('anonymous')
    @Js
    def PyJs_anonymous_119_(rule, fn, this, arguments, var=var):
        var = Scope({'rule':rule, 'fn':fn, 'this':this, 'arguments':arguments}, var)
        var.registers(['fn', 'rule'])
        @Js
        def PyJs_anonymous_120_(s, this, arguments, var=var):
            var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
            var.registers(['r', 's'])
            var.put('r', var.get('rule').callprop('call', var.get(u"this"), var.get('s')))
            return Js([var.get('fn').callprop('call', var.get(u"this"), var.get('r').get('0')), var.get('r').get('1')])
        PyJs_anonymous_120_._set_name('anonymous')
        return PyJs_anonymous_120_
    PyJs_anonymous_119_._set_name('anonymous')
    @Js
    def PyJs_anonymous_121_(min, rule, this, arguments, var=var):
        var = Scope({'min':min, 'rule':rule, 'this':this, 'arguments':arguments}, var)
        var.registers(['rule', 'min'])
        @Js
        def PyJs_anonymous_122_(s, this, arguments, var=var):
            var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
            var.registers(['rx', 's'])
            var.put('rx', var.get('rule').callprop('call', var.get(u"this"), var.get('s')))
            if (var.get('rx').get('0').get('length')<var.get('min')):
                PyJsTempException = JsToPyException(var.get('$P').get('Exception').create(var.get('s')))
                raise PyJsTempException
            return var.get('rx')
        PyJs_anonymous_122_._set_name('anonymous')
        return PyJs_anonymous_122_
    PyJs_anonymous_121_._set_name('anonymous')
    PyJs_Object_82_ = Js({'rtoken':PyJs_anonymous_83_,'token':PyJs_anonymous_85_,'stoken':PyJs_anonymous_87_,'until':PyJs_anonymous_88_,'many':PyJs_anonymous_90_,'optional':PyJs_anonymous_92_,'not':PyJs_anonymous_94_,'ignore':PyJs_anonymous_96_,'product':PyJs_anonymous_98_,'cache':PyJs_anonymous_99_,'any':PyJs_anonymous_102_,'each':PyJs_anonymous_104_,'all':PyJs_anonymous_106_,'sequence':PyJs_anonymous_107_,'between':PyJs_anonymous_109_,'list':PyJs_anonymous_111_,'set':PyJs_anonymous_113_,'forward':PyJs_anonymous_115_,'replace':PyJs_anonymous_117_,'process':PyJs_anonymous_119_,'min':PyJs_anonymous_121_})
    var.put('_', var.get('$P').put('Operators', PyJs_Object_82_))
    @Js
    def PyJs_anonymous_123_(op, this, arguments, var=var):
        var = Scope({'op':op, 'this':this, 'arguments':arguments}, var)
        var.registers(['op'])
        @Js
        def PyJs_anonymous_124_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers(['px', 'args', 'i', 'rx'])
            var.put('args', var.get(u"null"))
            var.put('rx', Js([]))
            if (var.get('arguments').get('length')>Js(1.0)):
                var.put('args', var.get('Array').get('prototype').get('slice').callprop('call', var.get('arguments')))
            else:
                if var.get('arguments').get('0').instanceof(var.get('Array')):
                    var.put('args', var.get('arguments').get('0'))
            if var.get('args'):
                #for JS loop
                var.put('i', Js(0.0))
                var.put('px', var.get('args').callprop('shift'))
                while (var.get('i')<var.get('px').get('length')):
                    try:
                        var.get('args').callprop('unshift', var.get('px').get(var.get('i')))
                        var.get('rx').callprop('push', var.get('op').callprop('apply', var.get(u"null"), var.get('args')))
                        var.get('args').callprop('shift')
                        return var.get('rx')
                    finally:
                            (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            else:
                return var.get('op').callprop('apply', var.get(u"null"), var.get('arguments'))
        PyJs_anonymous_124_._set_name('anonymous')
        return PyJs_anonymous_124_
    PyJs_anonymous_123_._set_name('anonymous')
    var.put('_generator', PyJs_anonymous_123_)
    var.put('gx', Js('optional not ignore cache').callprop('split', JsRegExp('/\\s/')))
    #for JS loop
    var.put('i', Js(0.0))
    while (var.get('i')<var.get('gx').get('length')):
        try:
            var.get('_').put(var.get('gx').get(var.get('i')), var.get('_generator')(var.get('_').get(var.get('gx').get(var.get('i')))))
        finally:
                (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
    @Js
    def PyJs_anonymous_125_(op, this, arguments, var=var):
        var = Scope({'op':op, 'this':this, 'arguments':arguments}, var)
        var.registers(['op'])
        @Js
        def PyJs_anonymous_126_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            if var.get('arguments').get('0').instanceof(var.get('Array')):
                return var.get('op').callprop('apply', var.get(u"null"), var.get('arguments').get('0'))
            else:
                return var.get('op').callprop('apply', var.get(u"null"), var.get('arguments'))
        PyJs_anonymous_126_._set_name('anonymous')
        return PyJs_anonymous_126_
    PyJs_anonymous_125_._set_name('anonymous')
    var.put('_vector', PyJs_anonymous_125_)
    var.put('vx', Js('each any all').callprop('split', JsRegExp('/\\s/')))
    #for JS loop
    var.put('j', Js(0.0))
    while (var.get('j')<var.get('vx').get('length')):
        try:
            var.get('_').put(var.get('vx').get(var.get('j')), var.get('_vector')(var.get('_').get(var.get('vx').get(var.get('j')))))
        finally:
                (var.put('j',Js(var.get('j').to_number())+Js(1))-Js(1))
PyJs_anonymous_79_._set_name('anonymous')
PyJs_anonymous_79_()
@Js
def PyJs_anonymous_127_(this, arguments, var=var):
    var = Scope({'this':this, 'arguments':arguments}, var)
    var.registers(['_', '_F', 'flattenAndCompact', 't', '_fn', 'g', '_C', '_get'])
    @Js
    def PyJs_anonymous_128_(ax, this, arguments, var=var):
        var = Scope({'ax':ax, 'this':this, 'arguments':arguments}, var)
        var.registers(['i', 'ax', 'rx'])
        var.put('rx', Js([]))
        #for JS loop
        var.put('i', Js(0.0))
        while (var.get('i')<var.get('ax').get('length')):
            try:
                if var.get('ax').get(var.get('i')).instanceof(var.get('Array')):
                    var.put('rx', var.get('rx').callprop('concat', var.get('flattenAndCompact')(var.get('ax').get(var.get('i')))))
                else:
                    if var.get('ax').get(var.get('i')):
                        var.get('rx').callprop('push', var.get('ax').get(var.get('i')))
            finally:
                    (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
        return var.get('rx')
    PyJs_anonymous_128_._set_name('anonymous')
    var.put('flattenAndCompact', PyJs_anonymous_128_)
    PyJs_Object_129_ = Js({})
    var.get('Date').put('Grammar', PyJs_Object_129_)
    @Js
    def PyJs_anonymous_131_(s, this, arguments, var=var):
        var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
        var.registers(['s'])
        @Js
        def PyJs_anonymous_132_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            var.get(u"this").put('hour', var.get('Number')(var.get('s')))
        PyJs_anonymous_132_._set_name('anonymous')
        return PyJs_anonymous_132_
    PyJs_anonymous_131_._set_name('anonymous')
    @Js
    def PyJs_anonymous_133_(s, this, arguments, var=var):
        var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
        var.registers(['s'])
        @Js
        def PyJs_anonymous_134_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            var.get(u"this").put('minute', var.get('Number')(var.get('s')))
        PyJs_anonymous_134_._set_name('anonymous')
        return PyJs_anonymous_134_
    PyJs_anonymous_133_._set_name('anonymous')
    @Js
    def PyJs_anonymous_135_(s, this, arguments, var=var):
        var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
        var.registers(['s'])
        @Js
        def PyJs_anonymous_136_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            var.get(u"this").put('second', var.get('Number')(var.get('s')))
        PyJs_anonymous_136_._set_name('anonymous')
        return PyJs_anonymous_136_
    PyJs_anonymous_135_._set_name('anonymous')
    @Js
    def PyJs_anonymous_137_(s, this, arguments, var=var):
        var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
        var.registers(['s'])
        @Js
        def PyJs_anonymous_138_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            var.get(u"this").put('meridian', var.get('s').callprop('slice', Js(0.0), Js(1.0)).callprop('toLowerCase'))
        PyJs_anonymous_138_._set_name('anonymous')
        return PyJs_anonymous_138_
    PyJs_anonymous_137_._set_name('anonymous')
    @Js
    def PyJs_anonymous_139_(s, this, arguments, var=var):
        var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
        var.registers(['s'])
        @Js
        def PyJs_anonymous_140_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers(['n'])
            var.put('n', var.get('s').callprop('replace', JsRegExp('/[^\\d\\+\\-]/g'), Js('')))
            if var.get('n').get('length'):
                var.get(u"this").put('timezoneOffset', var.get('Number')(var.get('n')))
            else:
                var.get(u"this").put('timezone', var.get('s').callprop('toLowerCase'))
        PyJs_anonymous_140_._set_name('anonymous')
        return PyJs_anonymous_140_
    PyJs_anonymous_139_._set_name('anonymous')
    @Js
    def PyJs_anonymous_141_(x, this, arguments, var=var):
        var = Scope({'x':x, 'this':this, 'arguments':arguments}, var)
        var.registers(['x', 's'])
        var.put('s', var.get('x').get('0'))
        @Js
        def PyJs_anonymous_142_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            var.get(u"this").put('day', var.get('Number')(var.get('s').callprop('match', JsRegExp('/\\d+/')).get('0')))
        PyJs_anonymous_142_._set_name('anonymous')
        return PyJs_anonymous_142_
    PyJs_anonymous_141_._set_name('anonymous')
    @Js
    def PyJs_anonymous_143_(s, this, arguments, var=var):
        var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
        var.registers(['s'])
        @Js
        def PyJs_anonymous_144_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            var.get(u"this").put('month', (var.get('Date').callprop('getMonthNumberFromName', var.get('s')) if (var.get('s').get('length')==Js(3.0)) else (var.get('Number')(var.get('s'))-Js(1.0))))
        PyJs_anonymous_144_._set_name('anonymous')
        return PyJs_anonymous_144_
    PyJs_anonymous_143_._set_name('anonymous')
    @Js
    def PyJs_anonymous_145_(s, this, arguments, var=var):
        var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
        var.registers(['s'])
        @Js
        def PyJs_anonymous_146_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers(['n'])
            var.put('n', var.get('Number')(var.get('s')))
            var.get(u"this").put('year', (var.get('n') if (var.get('s').get('length')>Js(2.0)) else (var.get('n')+(Js(2000.0) if ((var.get('n')+Js(2000.0))<var.get('Date').get('CultureInfo').get('twoDigitYearMax')) else Js(1900.0)))))
        PyJs_anonymous_146_._set_name('anonymous')
        return PyJs_anonymous_146_
    PyJs_anonymous_145_._set_name('anonymous')
    @Js
    def PyJs_anonymous_147_(s, this, arguments, var=var):
        var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
        var.registers(['s'])
        @Js
        def PyJs_anonymous_148_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            while 1:
                SWITCHED = False
                CONDITION = (var.get('s'))
                if SWITCHED or PyJsStrictEq(CONDITION, Js('yesterday')):
                    SWITCHED = True
                    var.get(u"this").put('days', (-Js(1.0)))
                    break
                if SWITCHED or PyJsStrictEq(CONDITION, Js('tomorrow')):
                    SWITCHED = True
                    var.get(u"this").put('days', Js(1.0))
                    break
                if SWITCHED or PyJsStrictEq(CONDITION, Js('today')):
                    SWITCHED = True
                    var.get(u"this").put('days', Js(0.0))
                    break
                if SWITCHED or PyJsStrictEq(CONDITION, Js('now')):
                    SWITCHED = True
                    var.get(u"this").put('days', Js(0.0))
                    var.get(u"this").put('now', Js(True))
                    break
                SWITCHED = True
                break
        PyJs_anonymous_148_._set_name('anonymous')
        return PyJs_anonymous_148_
    PyJs_anonymous_147_._set_name('anonymous')
    @Js
    def PyJs_anonymous_149_(x, this, arguments, var=var):
        var = Scope({'x':x, 'this':this, 'arguments':arguments}, var)
        var.registers(['now', 'i', 'x', 'r'])
        var.put('x', (var.get('x') if var.get('x').instanceof(var.get('Array')) else Js([var.get('x')])))
        var.put('now', var.get('Date').create())
        var.get(u"this").put('year', var.get('now').callprop('getFullYear'))
        var.get(u"this").put('month', var.get('now').callprop('getMonth'))
        var.get(u"this").put('day', Js(1.0))
        var.get(u"this").put('hour', Js(0.0))
        var.get(u"this").put('minute', Js(0.0))
        var.get(u"this").put('second', Js(0.0))
        #for JS loop
        var.put('i', Js(0.0))
        while (var.get('i')<var.get('x').get('length')):
            try:
                if var.get('x').get(var.get('i')):
                    var.get('x').get(var.get('i')).callprop('call', var.get(u"this"))
            finally:
                    (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
        var.get(u"this").put('hour', ((var.get(u"this").get('hour')+Js(12.0)) if ((var.get(u"this").get('meridian')==Js('p')) and (var.get(u"this").get('hour')<Js(13.0))) else var.get(u"this").get('hour')))
        if (var.get(u"this").get('day')>var.get('Date').callprop('getDaysInMonth', var.get(u"this").get('year'), var.get(u"this").get('month'))):
            PyJsTempException = JsToPyException(var.get('RangeError').create((var.get(u"this").get('day')+Js(' is not a valid value for days.'))))
            raise PyJsTempException
        var.put('r', var.get('Date').create(var.get(u"this").get('year'), var.get(u"this").get('month'), var.get(u"this").get('day'), var.get(u"this").get('hour'), var.get(u"this").get('minute'), var.get(u"this").get('second')))
        if var.get(u"this").get('timezone'):
            PyJs_Object_150_ = Js({'timezone':var.get(u"this").get('timezone')})
            var.get('r').callprop('set', PyJs_Object_150_)
        else:
            if var.get(u"this").get('timezoneOffset'):
                PyJs_Object_151_ = Js({'timezoneOffset':var.get(u"this").get('timezoneOffset')})
                var.get('r').callprop('set', PyJs_Object_151_)
        return var.get('r')
    PyJs_anonymous_149_._set_name('anonymous')
    @Js
    def PyJs_anonymous_152_(x, this, arguments, var=var):
        var = Scope({'x':x, 'this':this, 'arguments':arguments}, var)
        var.registers(['mod', 'gap', 'i', 'orient', 'today', 'method', 'expression', 'x'])
        var.put('x', (var.get('flattenAndCompact')(var.get('x')) if var.get('x').instanceof(var.get('Array')) else Js([var.get('x')])))
        if PyJsStrictEq(var.get('x').get('length'),Js(0.0)):
            return var.get(u"null")
        #for JS loop
        var.put('i', Js(0.0))
        while (var.get('i')<var.get('x').get('length')):
            try:
                if (var.get('x').get(var.get('i')).typeof()==Js('function')):
                    var.get('x').get(var.get('i')).callprop('call', var.get(u"this"))
            finally:
                    (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
        if var.get(u"this").get('now'):
            return var.get('Date').create()
        var.put('today', var.get('Date').callprop('today'))
        var.put('method', var.get(u"null"))
        var.put('expression', (((var.get(u"this").get('days')!=var.get(u"null")) or var.get(u"this").get('orient')) or var.get(u"this").get('operator')).neg().neg())
        if var.get('expression'):
            pass
            var.put('orient', ((-Js(1.0)) if ((var.get(u"this").get('orient')==Js('past')) or (var.get(u"this").get('operator')==Js('subtract'))) else Js(1.0)))
            if var.get(u"this").get('weekday'):
                var.get(u"this").put('unit', Js('day'))
                var.put('gap', (var.get('Date').callprop('getDayNumberFromName', var.get(u"this").get('weekday'))-var.get('today').callprop('getDay')))
                var.put('mod', Js(7.0))
                var.get(u"this").put('days', (((var.get('gap')+(var.get('orient')*var.get('mod')))%var.get('mod')) if var.get('gap') else (var.get('orient')*var.get('mod'))))
            if var.get(u"this").get('month'):
                var.get(u"this").put('unit', Js('month'))
                var.put('gap', (var.get(u"this").get('month')-var.get('today').callprop('getMonth')))
                var.put('mod', Js(12.0))
                var.get(u"this").put('months', (((var.get('gap')+(var.get('orient')*var.get('mod')))%var.get('mod')) if var.get('gap') else (var.get('orient')*var.get('mod'))))
                var.get(u"this").put('month', var.get(u"null"))
            if var.get(u"this").get('unit').neg():
                var.get(u"this").put('unit', Js('day'))
            if ((var.get(u"this").get((var.get(u"this").get('unit')+Js('s')))==var.get(u"null")) or (var.get(u"this").get('operator')!=var.get(u"null"))):
                if var.get(u"this").get('value').neg():
                    var.get(u"this").put('value', Js(1.0))
                if (var.get(u"this").get('unit')==Js('week')):
                    var.get(u"this").put('unit', Js('day'))
                    var.get(u"this").put('value', (var.get(u"this").get('value')*Js(7.0)))
                var.get(u"this").put((var.get(u"this").get('unit')+Js('s')), (var.get(u"this").get('value')*var.get('orient')))
            return var.get('today').callprop('add', var.get(u"this"))
        else:
            if (var.get(u"this").get('meridian') and var.get(u"this").get('hour')):
                var.get(u"this").put('hour', ((var.get(u"this").get('hour')+Js(12.0)) if ((var.get(u"this").get('hour')<Js(13.0)) and (var.get(u"this").get('meridian')==Js('p'))) else var.get(u"this").get('hour')))
            if (var.get(u"this").get('weekday') and var.get(u"this").get('day').neg()):
                var.get(u"this").put('day', var.get('today').callprop('addDays', (var.get('Date').callprop('getDayNumberFromName', var.get(u"this").get('weekday'))-var.get('today').callprop('getDay'))).callprop('getDate'))
            if (var.get(u"this").get('month') and var.get(u"this").get('day').neg()):
                var.get(u"this").put('day', Js(1.0))
            return var.get('today').callprop('set', var.get(u"this"))
    PyJs_anonymous_152_._set_name('anonymous')
    PyJs_Object_130_ = Js({'hour':PyJs_anonymous_131_,'minute':PyJs_anonymous_133_,'second':PyJs_anonymous_135_,'meridian':PyJs_anonymous_137_,'timezone':PyJs_anonymous_139_,'day':PyJs_anonymous_141_,'month':PyJs_anonymous_143_,'year':PyJs_anonymous_145_,'rday':PyJs_anonymous_147_,'finishExact':PyJs_anonymous_149_,'finish':PyJs_anonymous_152_})
    var.get('Date').put('Translator', PyJs_Object_130_)
    var.put('_', var.get('Date').get('Parsing').get('Operators'))
    var.put('g', var.get('Date').get('Grammar'))
    var.put('t', var.get('Date').get('Translator'))
    var.get('g').put('datePartDelimiter', var.get('_').callprop('rtoken', JsRegExp('/^([\\s\\-\\.\\,\\/\\x27]+)/')))
    var.get('g').put('timePartDelimiter', var.get('_').callprop('stoken', Js(':')))
    var.get('g').put('whiteSpace', var.get('_').callprop('rtoken', JsRegExp('/^\\s*/')))
    var.get('g').put('generalDelimiter', var.get('_').callprop('rtoken', JsRegExp('/^(([\\s\\,]|at|on)+)/')))
    PyJs_Object_153_ = Js({})
    var.put('_C', PyJs_Object_153_)
    @Js
    def PyJs_anonymous_154_(keys, this, arguments, var=var):
        var = Scope({'keys':keys, 'this':this, 'arguments':arguments}, var)
        var.registers(['fn', 'i', 'px', 'c', 'kx', 'keys'])
        var.put('fn', var.get('_C').get(var.get('keys')))
        if var.get('fn').neg():
            var.put('c', var.get('Date').get('CultureInfo').get('regexPatterns'))
            var.put('kx', var.get('keys').callprop('split', JsRegExp('/\\s+/')))
            var.put('px', Js([]))
            #for JS loop
            var.put('i', Js(0.0))
            while (var.get('i')<var.get('kx').get('length')):
                try:
                    var.get('px').callprop('push', var.get('_').callprop('replace', var.get('_').callprop('rtoken', var.get('c').get(var.get('kx').get(var.get('i')))), var.get('kx').get(var.get('i'))))
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            var.put('fn', var.get('_C').put(var.get('keys'), var.get('_').get('any').callprop('apply', var.get(u"null"), var.get('px'))))
        return var.get('fn')
    PyJs_anonymous_154_._set_name('anonymous')
    var.get('g').put('ctoken', PyJs_anonymous_154_)
    @Js
    def PyJs_anonymous_155_(key, this, arguments, var=var):
        var = Scope({'key':key, 'this':this, 'arguments':arguments}, var)
        var.registers(['key'])
        return var.get('_').callprop('rtoken', var.get('Date').get('CultureInfo').get('regexPatterns').get(var.get('key')))
    PyJs_anonymous_155_._set_name('anonymous')
    var.get('g').put('ctoken2', PyJs_anonymous_155_)
    var.get('g').put('h', var.get('_').callprop('cache', var.get('_').callprop('process', var.get('_').callprop('rtoken', JsRegExp('/^(0[0-9]|1[0-2]|[1-9])/')), var.get('t').get('hour'))))
    var.get('g').put('hh', var.get('_').callprop('cache', var.get('_').callprop('process', var.get('_').callprop('rtoken', JsRegExp('/^(0[0-9]|1[0-2])/')), var.get('t').get('hour'))))
    var.get('g').put('H', var.get('_').callprop('cache', var.get('_').callprop('process', var.get('_').callprop('rtoken', JsRegExp('/^([0-1][0-9]|2[0-3]|[0-9])/')), var.get('t').get('hour'))))
    var.get('g').put('HH', var.get('_').callprop('cache', var.get('_').callprop('process', var.get('_').callprop('rtoken', JsRegExp('/^([0-1][0-9]|2[0-3])/')), var.get('t').get('hour'))))
    var.get('g').put('m', var.get('_').callprop('cache', var.get('_').callprop('process', var.get('_').callprop('rtoken', JsRegExp('/^([0-5][0-9]|[0-9])/')), var.get('t').get('minute'))))
    var.get('g').put('mm', var.get('_').callprop('cache', var.get('_').callprop('process', var.get('_').callprop('rtoken', JsRegExp('/^[0-5][0-9]/')), var.get('t').get('minute'))))
    var.get('g').put('s', var.get('_').callprop('cache', var.get('_').callprop('process', var.get('_').callprop('rtoken', JsRegExp('/^([0-5][0-9]|[0-9])/')), var.get('t').get('second'))))
    var.get('g').put('ss', var.get('_').callprop('cache', var.get('_').callprop('process', var.get('_').callprop('rtoken', JsRegExp('/^[0-5][0-9]/')), var.get('t').get('second'))))
    var.get('g').put('hms', var.get('_').callprop('cache', var.get('_').callprop('sequence', Js([var.get('g').get('H'), var.get('g').get('mm'), var.get('g').get('ss')]), var.get('g').get('timePartDelimiter'))))
    var.get('g').put('t', var.get('_').callprop('cache', var.get('_').callprop('process', var.get('g').callprop('ctoken2', Js('shortMeridian')), var.get('t').get('meridian'))))
    var.get('g').put('tt', var.get('_').callprop('cache', var.get('_').callprop('process', var.get('g').callprop('ctoken2', Js('longMeridian')), var.get('t').get('meridian'))))
    var.get('g').put('z', var.get('_').callprop('cache', var.get('_').callprop('process', var.get('_').callprop('rtoken', JsRegExp('/^(\\+|\\-)?\\s*\\d\\d\\d\\d?/')), var.get('t').get('timezone'))))
    var.get('g').put('zz', var.get('_').callprop('cache', var.get('_').callprop('process', var.get('_').callprop('rtoken', JsRegExp('/^(\\+|\\-)\\s*\\d\\d\\d\\d/')), var.get('t').get('timezone'))))
    var.get('g').put('zzz', var.get('_').callprop('cache', var.get('_').callprop('process', var.get('g').callprop('ctoken2', Js('timezone')), var.get('t').get('timezone'))))
    var.get('g').put('timeSuffix', var.get('_').callprop('each', var.get('_').callprop('ignore', var.get('g').get('whiteSpace')), var.get('_').callprop('set', Js([var.get('g').get('tt'), var.get('g').get('zzz')]))))
    var.get('g').put('time', var.get('_').callprop('each', var.get('_').callprop('optional', var.get('_').callprop('ignore', var.get('_').callprop('stoken', Js('T')))), var.get('g').get('hms'), var.get('g').get('timeSuffix')))
    var.get('g').put('d', var.get('_').callprop('cache', var.get('_').callprop('process', var.get('_').callprop('each', var.get('_').callprop('rtoken', JsRegExp('/^([0-2]\\d|3[0-1]|\\d)/')), var.get('_').callprop('optional', var.get('g').callprop('ctoken2', Js('ordinalSuffix')))), var.get('t').get('day'))))
    var.get('g').put('dd', var.get('_').callprop('cache', var.get('_').callprop('process', var.get('_').callprop('each', var.get('_').callprop('rtoken', JsRegExp('/^([0-2]\\d|3[0-1])/')), var.get('_').callprop('optional', var.get('g').callprop('ctoken2', Js('ordinalSuffix')))), var.get('t').get('day'))))
    @Js
    def PyJs_anonymous_156_(s, this, arguments, var=var):
        var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
        var.registers(['s'])
        @Js
        def PyJs_anonymous_157_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            var.get(u"this").put('weekday', var.get('s'))
        PyJs_anonymous_157_._set_name('anonymous')
        return PyJs_anonymous_157_
    PyJs_anonymous_156_._set_name('anonymous')
    var.get('g').put('ddd', var.get('g').put('dddd', var.get('_').callprop('cache', var.get('_').callprop('process', var.get('g').callprop('ctoken', Js('sun mon tue wed thu fri sat')), PyJs_anonymous_156_))))
    var.get('g').put('M', var.get('_').callprop('cache', var.get('_').callprop('process', var.get('_').callprop('rtoken', JsRegExp('/^(1[0-2]|0\\d|\\d)/')), var.get('t').get('month'))))
    var.get('g').put('MM', var.get('_').callprop('cache', var.get('_').callprop('process', var.get('_').callprop('rtoken', JsRegExp('/^(1[0-2]|0\\d)/')), var.get('t').get('month'))))
    var.get('g').put('MMM', var.get('g').put('MMMM', var.get('_').callprop('cache', var.get('_').callprop('process', var.get('g').callprop('ctoken', Js('jan feb mar apr may jun jul aug sep oct nov dec')), var.get('t').get('month')))))
    var.get('g').put('y', var.get('_').callprop('cache', var.get('_').callprop('process', var.get('_').callprop('rtoken', JsRegExp('/^(\\d\\d?)/')), var.get('t').get('year'))))
    var.get('g').put('yy', var.get('_').callprop('cache', var.get('_').callprop('process', var.get('_').callprop('rtoken', JsRegExp('/^(\\d\\d)/')), var.get('t').get('year'))))
    var.get('g').put('yyy', var.get('_').callprop('cache', var.get('_').callprop('process', var.get('_').callprop('rtoken', JsRegExp('/^(\\d\\d?\\d?\\d?)/')), var.get('t').get('year'))))
    var.get('g').put('yyyy', var.get('_').callprop('cache', var.get('_').callprop('process', var.get('_').callprop('rtoken', JsRegExp('/^(\\d\\d\\d\\d)/')), var.get('t').get('year'))))
    @Js
    def PyJs_anonymous_158_(this, arguments, var=var):
        var = Scope({'this':this, 'arguments':arguments}, var)
        var.registers([])
        return var.get('_').callprop('each', var.get('_').get('any').callprop('apply', var.get(u"null"), var.get('arguments')), var.get('_').callprop('not', var.get('g').callprop('ctoken2', Js('timeContext'))))
    PyJs_anonymous_158_._set_name('anonymous')
    var.put('_fn', PyJs_anonymous_158_)
    var.get('g').put('day', var.get('_fn')(var.get('g').get('d'), var.get('g').get('dd')))
    var.get('g').put('month', var.get('_fn')(var.get('g').get('M'), var.get('g').get('MMM')))
    var.get('g').put('year', var.get('_fn')(var.get('g').get('yyyy'), var.get('g').get('yy')))
    @Js
    def PyJs_anonymous_159_(s, this, arguments, var=var):
        var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
        var.registers(['s'])
        @Js
        def PyJs_anonymous_160_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            var.get(u"this").put('orient', var.get('s'))
        PyJs_anonymous_160_._set_name('anonymous')
        return PyJs_anonymous_160_
    PyJs_anonymous_159_._set_name('anonymous')
    var.get('g').put('orientation', var.get('_').callprop('process', var.get('g').callprop('ctoken', Js('past future')), PyJs_anonymous_159_))
    @Js
    def PyJs_anonymous_161_(s, this, arguments, var=var):
        var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
        var.registers(['s'])
        @Js
        def PyJs_anonymous_162_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            var.get(u"this").put('operator', var.get('s'))
        PyJs_anonymous_162_._set_name('anonymous')
        return PyJs_anonymous_162_
    PyJs_anonymous_161_._set_name('anonymous')
    var.get('g').put('operator', var.get('_').callprop('process', var.get('g').callprop('ctoken', Js('add subtract')), PyJs_anonymous_161_))
    var.get('g').put('rday', var.get('_').callprop('process', var.get('g').callprop('ctoken', Js('yesterday tomorrow today now')), var.get('t').get('rday')))
    @Js
    def PyJs_anonymous_163_(s, this, arguments, var=var):
        var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
        var.registers(['s'])
        @Js
        def PyJs_anonymous_164_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            var.get(u"this").put('unit', var.get('s'))
        PyJs_anonymous_164_._set_name('anonymous')
        return PyJs_anonymous_164_
    PyJs_anonymous_163_._set_name('anonymous')
    var.get('g').put('unit', var.get('_').callprop('process', var.get('g').callprop('ctoken', Js('minute hour day week month year')), PyJs_anonymous_163_))
    @Js
    def PyJs_anonymous_165_(s, this, arguments, var=var):
        var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
        var.registers(['s'])
        @Js
        def PyJs_anonymous_166_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            var.get(u"this").put('value', var.get('s').callprop('replace', JsRegExp('/\\D/g'), Js('')))
        PyJs_anonymous_166_._set_name('anonymous')
        return PyJs_anonymous_166_
    PyJs_anonymous_165_._set_name('anonymous')
    var.get('g').put('value', var.get('_').callprop('process', var.get('_').callprop('rtoken', JsRegExp('/^\\d\\d?(st|nd|rd|th)?/')), PyJs_anonymous_165_))
    var.get('g').put('expression', var.get('_').callprop('set', Js([var.get('g').get('rday'), var.get('g').get('operator'), var.get('g').get('value'), var.get('g').get('unit'), var.get('g').get('orientation'), var.get('g').get('ddd'), var.get('g').get('MMM')])))
    @Js
    def PyJs_anonymous_167_(this, arguments, var=var):
        var = Scope({'this':this, 'arguments':arguments}, var)
        var.registers([])
        return var.get('_').callprop('set', var.get('arguments'), var.get('g').get('datePartDelimiter'))
    PyJs_anonymous_167_._set_name('anonymous')
    var.put('_fn', PyJs_anonymous_167_)
    var.get('g').put('mdy', var.get('_fn')(var.get('g').get('ddd'), var.get('g').get('month'), var.get('g').get('day'), var.get('g').get('year')))
    var.get('g').put('ymd', var.get('_fn')(var.get('g').get('ddd'), var.get('g').get('year'), var.get('g').get('month'), var.get('g').get('day')))
    var.get('g').put('dmy', var.get('_fn')(var.get('g').get('ddd'), var.get('g').get('day'), var.get('g').get('month'), var.get('g').get('year')))
    @Js
    def PyJs_anonymous_168_(s, this, arguments, var=var):
        var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
        var.registers(['s'])
        return (var.get('g').get(var.get('Date').get('CultureInfo').get('dateElementOrder')) or var.get('g').get('mdy')).callprop('call', var.get(u"this"), var.get('s'))
    PyJs_anonymous_168_._set_name('anonymous')
    var.get('g').put('date', PyJs_anonymous_168_)
    def PyJs_LONG_172_(var=var):
        @Js
        def PyJs_anonymous_169_(fmt, this, arguments, var=var):
            var = Scope({'fmt':fmt, 'this':this, 'arguments':arguments}, var)
            var.registers(['fmt'])
            if var.get('g').get(var.get('fmt')):
                return var.get('g').get(var.get('fmt'))
            else:
                PyJsTempException = JsToPyException(var.get('Date').get('Parsing').callprop('Exception', var.get('fmt')))
                raise PyJsTempException
        PyJs_anonymous_169_._set_name('anonymous')
        @Js
        def PyJs_anonymous_170_(s, this, arguments, var=var):
            var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
            var.registers(['s'])
            return var.get('_').callprop('ignore', var.get('_').callprop('stoken', var.get('s')))
        PyJs_anonymous_170_._set_name('anonymous')
        @Js
        def PyJs_anonymous_171_(rules, this, arguments, var=var):
            var = Scope({'rules':rules, 'this':this, 'arguments':arguments}, var)
            var.registers(['rules'])
            return var.get('_').callprop('process', var.get('_').get('each').callprop('apply', var.get(u"null"), var.get('rules')), var.get('t').get('finishExact'))
        PyJs_anonymous_171_._set_name('anonymous')
        return var.get('g').put('format', var.get('_').callprop('process', var.get('_').callprop('many', var.get('_').callprop('any', var.get('_').callprop('process', var.get('_').callprop('rtoken', JsRegExp('/^(dd?d?d?|MM?M?M?|yy?y?y?|hh?|HH?|mm?|ss?|tt?|zz?z?)/')), PyJs_anonymous_169_), var.get('_').callprop('process', var.get('_').callprop('rtoken', JsRegExp('/^[^dMyhHmstz]+/')), PyJs_anonymous_170_))), PyJs_anonymous_171_))
    PyJs_LONG_172_()
    PyJs_Object_173_ = Js({})
    var.put('_F', PyJs_Object_173_)
    @Js
    def PyJs_anonymous_174_(f, this, arguments, var=var):
        var = Scope({'f':f, 'this':this, 'arguments':arguments}, var)
        var.registers(['f'])
        return var.get('_F').put(var.get('f'), (var.get('_F').get(var.get('f')) or var.get('g').callprop('format', var.get('f')).get('0')))
    PyJs_anonymous_174_._set_name('anonymous')
    var.put('_get', PyJs_anonymous_174_)
    @Js
    def PyJs_anonymous_175_(fx, this, arguments, var=var):
        var = Scope({'fx':fx, 'this':this, 'arguments':arguments}, var)
        var.registers(['fx', 'i', 'rx'])
        if var.get('fx').instanceof(var.get('Array')):
            var.put('rx', Js([]))
            #for JS loop
            var.put('i', Js(0.0))
            while (var.get('i')<var.get('fx').get('length')):
                try:
                    var.get('rx').callprop('push', var.get('_get')(var.get('fx').get(var.get('i'))))
                finally:
                        (var.put('i',Js(var.get('i').to_number())+Js(1))-Js(1))
            return var.get('_').get('any').callprop('apply', var.get(u"null"), var.get('rx'))
        else:
            return var.get('_get')(var.get('fx'))
    PyJs_anonymous_175_._set_name('anonymous')
    var.get('g').put('formats', PyJs_anonymous_175_)
    var.get('g').put('_formats', var.get('g').callprop('formats', Js([Js('yyyy-MM-ddTHH:mm:ss'), Js('ddd, MMM dd, yyyy H:mm:ss tt'), Js('ddd MMM d yyyy HH:mm:ss zzz'), Js('d')])))
    var.get('g').put('_start', var.get('_').callprop('process', var.get('_').callprop('set', Js([var.get('g').get('date'), var.get('g').get('time'), var.get('g').get('expression')]), var.get('g').get('generalDelimiter'), var.get('g').get('whiteSpace')), var.get('t').get('finish')))
    @Js
    def PyJs_anonymous_176_(s, this, arguments, var=var):
        var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
        var.registers(['r', 's'])
        try:
            PyJs_Object_177_ = Js({})
            var.put('r', var.get('g').get('_formats').callprop('call', PyJs_Object_177_, var.get('s')))
            if PyJsStrictEq(var.get('r').get('1').get('length'),Js(0.0)):
                return var.get('r')
        except PyJsException as PyJsTempException:
            PyJsHolder_65_62812308 = var.own.get('e')
            var.force_own_put('e', PyExceptionToJs(PyJsTempException))
            try:
                pass
            finally:
                if PyJsHolder_65_62812308 is not None:
                    var.own['e'] = PyJsHolder_65_62812308
                else:
                    del var.own['e']
                del PyJsHolder_65_62812308
        PyJs_Object_178_ = Js({})
        return var.get('g').get('_start').callprop('call', PyJs_Object_178_, var.get('s'))
    PyJs_anonymous_176_._set_name('anonymous')
    var.get('g').put('start', PyJs_anonymous_176_)
PyJs_anonymous_127_._set_name('anonymous')
PyJs_anonymous_127_()
var.get('Date').put('_parse', var.get('Date').get('parse'))
@Js
def PyJs_anonymous_179_(s, this, arguments, var=var):
    var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
    var.registers(['r', 's'])
    var.put('r', var.get(u"null"))
    if var.get('s').neg():
        return var.get(u"null")
    try:
        PyJs_Object_180_ = Js({})
        var.put('r', var.get('Date').get('Grammar').get('start').callprop('call', PyJs_Object_180_, var.get('s')))
    except PyJsException as PyJsTempException:
        PyJsHolder_65_5134994 = var.own.get('e')
        var.force_own_put('e', PyExceptionToJs(PyJsTempException))
        try:
            return var.get(u"null")
        finally:
            if PyJsHolder_65_5134994 is not None:
                var.own['e'] = PyJsHolder_65_5134994
            else:
                del var.own['e']
            del PyJsHolder_65_5134994
    return (var.get('r').get('0') if PyJsStrictEq(var.get('r').get('1').get('length'),Js(0.0)) else var.get(u"null"))
PyJs_anonymous_179_._set_name('anonymous')
var.get('Date').put('parse', PyJs_anonymous_179_)
@Js
def PyJs_anonymous_181_(fx, this, arguments, var=var):
    var = Scope({'fx':fx, 'this':this, 'arguments':arguments}, var)
    var.registers(['fn', 'fx'])
    var.put('fn', var.get('Date').get('Grammar').callprop('formats', var.get('fx')))
    @Js
    def PyJs_anonymous_182_(s, this, arguments, var=var):
        var = Scope({'s':s, 'this':this, 'arguments':arguments}, var)
        var.registers(['r', 's'])
        var.put('r', var.get(u"null"))
        try:
            PyJs_Object_183_ = Js({})
            var.put('r', var.get('fn').callprop('call', PyJs_Object_183_, var.get('s')))
        except PyJsException as PyJsTempException:
            PyJsHolder_65_84408237 = var.own.get('e')
            var.force_own_put('e', PyExceptionToJs(PyJsTempException))
            try:
                return var.get(u"null")
            finally:
                if PyJsHolder_65_84408237 is not None:
                    var.own['e'] = PyJsHolder_65_84408237
                else:
                    del var.own['e']
                del PyJsHolder_65_84408237
        return (var.get('r').get('0') if PyJsStrictEq(var.get('r').get('1').get('length'),Js(0.0)) else var.get(u"null"))
    PyJs_anonymous_182_._set_name('anonymous')
    return PyJs_anonymous_182_
PyJs_anonymous_181_._set_name('anonymous')
var.get('Date').put('getParseFunction', PyJs_anonymous_181_)
@Js
def PyJs_anonymous_184_(s, fx, this, arguments, var=var):
    var = Scope({'s':s, 'fx':fx, 'this':this, 'arguments':arguments}, var)
    var.registers(['fx', 's'])
    return var.get('Date').callprop('getParseFunction', var.get('fx'))(var.get('s'))
PyJs_anonymous_184_._set_name('anonymous')
var.get('Date').put('parseExact', PyJs_anonymous_184_)
pass


# Add lib to the module scope
js_date = var.to_python()