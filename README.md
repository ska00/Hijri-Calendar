# A New (Solar-true) Hirji Calendar

## The Hirji (Islamic) Calendar

The traditional Hirji (Islamic) calendar is always ~11 days short of the Solar (Gregorian) calendar. This leads to the Hirji months shifting little by little each year. For example, 
Ramadan would start in summer, then (with time) in spring, then in winter and fall until finally it starts again in summer after ~33 years. The issue is that the
Hijri years no longer represent _true_ years in the sense that years represent the passing of all the seasons and the reset of Earth's position relative to the sun. 
The Hijri (Islamic) calendar right now does not involve the solar year in its calculations, something that must be accounted for. Some of the Hijri months are named 
with accordance to the season they appear in. For example, Rabi means spring in English. Take today's date: Rabi II 12, 1446 (October 16, 2024). According to the
Islamic calendar it is the second month of spring; autumn is the season we are currently in. The disjunction of the seasons with the Hijri calendar
is what motivated this project.

## The New Hirji Calendar

This project attempts make a new type of Hirji Calendar that remains in sync with the Solar (Gregorian) calendar. To achieve this, a 13th month must be added every 2 to 3 years.
The Hijri months are as follows: Safar I, Safar II, Rabi I, Rabi II, Jumada I, Jumada II, Rajab, Sha'ban, Ramadan, Shawwal, Dhul Qadah, and Dhul Hijjah. Notice, that the month 
Muharram has been removed; instead it has been replaced by Safar I, and Safar II has been introduced. The 13th month _is_ Muharram, which sometimes appears at the start of the 
year or at the end depending on when the gap between the solar year and Hijri year diverge most. This keeps the Hijri months in their relative seasons. Since the number of days 
for each Hijri month is fixed, an additional day must sometimes be added to Dhul Hijjah. This also means that the beginning of the month does not always coincide with the full moon
and might start earlier or later. Check out the file [hijri_calendar_aware.py](https://github.com/ska00/Hijra-Calendar/blob/main/hijri_calendar_aware.py).

The 'aware' hirji calendar calculates whether to put the 13th month at the start of the year or at the end. The 'naive' version always puts the 13th month at the end.

## The New Observation-Based Hirji Calendar

This is an alternative of the new Hijra Calendar. Similar to the traditional Hijra (Islamic) calendar, the months officially start on the day after observing the new moon.
Except that this calendar, like the new Hijra Calendar, starts on the day after the _full moon_ is observed. Check out the file named [hijri_calendar_aware_simple.py](https://github.com/ska00/Hijra-Calendar/blob/main/hijri_calendar_aware_simple.py)

## Implementing a Metonic Cycle in the Hijri calendar

In the Metonic cycle, seven years are leap years (in which the 13th month is added) and 12 years are common years. In this section, the leap months are added whenever the Hijri year
is one of the 3, 6, 8, 11, 14, 17, 19 years in the 19-year cycle. Though, in this piece of code, the 13th month is always added to the end of the Hijri year. Check out the file
named [hijri_calendar_naive_metonic.py](https://github.com/ska00/Hijra-Calendar/blob/main/hijri_calendar_naive_metonic.py).

## Implementing the Metonic Cycle in the Observation-Based Hirji Calendar

This section implements the Metonic cycle in the observation-based Hijri calendar. Given any Hijri year it can be known whether there is a leap month or not. Note that the 13th month
is always added to the end of the year.
Check out the file named [hijri_calendar_naive_simple_metonic.py](https://github.com/ska00/Hijra-Calendar/blob/main/hijri_calendar_naive_simple_metonic.py)


_Moon Phases Table courtesy of Fred Espenak, www.Astropixels.com._
