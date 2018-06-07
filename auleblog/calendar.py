# -*- coding: utf-8 -*-
from calendar import HTMLCalendar
from datetime import date
from itertools import groupby


class WorkoutCalendar(HTMLCalendar):

    def __init__(self, workouts):
        super(WorkoutCalendar, self).__init__()
        self.workouts = self.group_by_day(workouts)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.workouts:
                cssclass += ' post'
                linkp = []
                linkk = []
                for workout in self.workouts[day]:
                    linkp.append('<a href="%s" data-toggle ="tooltip" data-placement="top" title="%s">' % (workout.get_absolute_url(), workout.absolute_title()))
                    linkk.append('</a>')
                return self.day_cell(cssclass, '%s %s %s' % (''.join(linkp), day, ''.join(linkk)))
            return self.day_cell(cssclass, day)
        else:
            return '<td class="noday">&nbsp;</td>'

    def day_cell(selfself, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)

    def formatmonth(self, year, month, withyear=True):
        self.year, self.month = year, month
        month_create_list = []
        month_list_append = month_create_list.append
        month_list_append('<table class="table table-striped table-bordered">')
        month_list_append('\n')
        month_list_append(self.formatmonthname(year, month, withyear=withyear))
        month_list_append('\n')
        month_list_append(self.formatweekheader())
        month_list_append('\n')
        for week in self.monthdays2calendar(year, month):
            month_list_append(self.formatweek(week))
        month_list_append('</table>')
        return ''.join(month_create_list)

    def group_by_day(self, workouts):
        field = lambda workout: workout.date_pub.day
        return dict(
            [(day, list(items)) for day, items in groupby(workouts, field)]
        )
