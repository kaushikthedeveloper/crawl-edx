# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field

class School(Item):
    title=Field()                #title
    name=Field()                 #name
    uri=Field()                  #uri
    language=Field()             #language

class Staff(Item):
    name=Field()                 #title
    title=Field()                #[display_position][title]
    org=Field()                  #[display_position][org]
    bio_uri=Field()              #uri
    language=Field()             #language

class Subject(Item):
    title=Field()                #title
    uri=Field()                  #uri
    language=Field()             #language


class Course(Item):
    cid=Field()                  #cid
    current_language=Field()     #current_language
    title=Field()                #title
    course_uri=Field()           #course_about_uri
    created=Field()              #created
    course_number=Field()        #display_course_number
    json_course_id=Field()       #course_id
    subtitle=Field()             #subtitle
    description=Field()          #description
    what_you_will_learn=Field()  #what_you_will_learn
    syllabus=Field()             #syllabus
    start_date=Field()           #start
    end_date=Field()             #end
    availability=Field()         #[availability][title]
    level=Field()                #[level][title]
    length=Field()               #length
    prescribed_effort=Field()    #effort
    prerequisites=Field()        #prerequisites
    pacing_type=Field()          #pacing_type

    schools=Field()                  #schools | [array]
    staffs=Field()                   #staff | [array]
    subjects=Field()                 #subjects | [array]
