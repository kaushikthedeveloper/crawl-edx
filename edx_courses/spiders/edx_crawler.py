import json
import scrapy
from datetime import datetime


from edx_courses.items import Course, School,Staff,Subject

class Edx_pageSpider(scrapy.Spider):
    name = "edxcourses"

    start_urls=[
        'https://www.edx.org/course/?course=all'
    ]


    #Courses list : starting list (JSON)
    def getFirstCourseUrls(self,response):
        self.log("\n\n----------- JSON response 1 : %s -----------\n\n" %response)
        JSONresponse=json.loads(response.body_as_unicode())

        #get passed Course Urls
        for i,course_obj in enumerate(JSONresponse["objects"]["results"]):
            course_url=course_obj["marketing_url"]
            yield scrapy.Request(url=course_url, callback=self.parseCourse,errback=self.errorLog)

        self.log('\n\n----------- Next Url : '+ str(JSONresponse["objects"]["next"])+'-----------\n\n')

        #Check if more JSON are there and foward to next if not null
        next_url=JSONresponse["objects"]["next"]
        if next_url is not None:
            #manually increase result count from 9 to 500 (increase efficiency)
            next_url=str(next_url).replace("page_size=9","page_size=500")
            yield scrapy.Request(url=next_url, callback=self.getNextCourseUrls,errback=self.errorLog)
        else:
            self.log("\n\n----------- DONE ! ! ! Last Url : %s-----------\n\n", response)

    #Courses list : next list (JSON)
    def getNextCourseUrls(self,response):
        self.log("\n\n----------- JSON response Next : %s -----------\n\n" %response)
        JSONresponse=json.loads(response.body_as_unicode())

        # get passed Course Urls
        for i,course_obj in enumerate(JSONresponse["objects"]["results"]):
            course_url = course_obj["marketing_url"]
            yield scrapy.Request(url=course_url, callback=self.parseCourse,errback=self.errorLog)

        self.log('\n\n----------- Next Url : ' + str(JSONresponse["objects"]["next"]) + '-----------\n\n')

        # Check if more JSON are there and foward to next if not null
        next_url = JSONresponse["objects"]["next"]
        if next_url is not None:
            #manually increase result count from 9 to 500
            next_url = str(next_url).replace("page_size=9", "page_size=500")
            yield scrapy.Request(url=next_url, callback=self.getNextCourseUrls,errback=self.errorLog)
        else:
            self.log("\n\n----------- DONE ! ! ! Last Url : %s-----------\n\n" %response)

    #Course selected : in course page
    def parseCourse(self, response):
        self.log("\n\n---------- Inside %s -----------\n\n" %response)

        JSONDataUrl=response.xpath('//main[@id="course-info-page"]/@data-course-id').extract_first()
        self.log("\n\n---------- GET at : %s -----------\n\n" %JSONDataUrl)

        full_url='https://www.edx.org/api/catalog/v2/courses/'+JSONDataUrl
        yield scrapy.Request(url=full_url,callback=self.parseCourseJSON,errback=self.errorLog)

    #Course selected : JSON values
    def parseCourseJSON(self,response):
        self.log("\n\n----------- Course JSON response : %s -----------\n\n" %response)
        JSONresponse=json.loads(response.body_as_unicode())
        #self.log('\n\n'+ str(JSONresponse)+'\n\n')
        self.log("\n\nCourse ID : "+JSONresponse["cid"]+"\n\n")
        #yield JSONresponse
        item=Course()
        item["cid"] = JSONresponse["cid"]
        item["course_number"] = JSONresponse["display_course_number"]
        item["current_language"] = JSONresponse["current_language"]
        item["title"] = JSONresponse["title"]
        item["course_uri"] = JSONresponse["course_about_uri"]
        item["created"] = JSONresponse["created"]
        item["json_course_id"] = JSONresponse["course_id"]
        item["subtitle"] = JSONresponse["subtitle"]
        item["description"] = JSONresponse["description"]
        item["what_you_will_learn"] = JSONresponse["what_you_will_learn"]
        item["syllabus"] = JSONresponse["syllabus"]
        item["start_date"] = JSONresponse["start"]
        item["end_date"] = JSONresponse["end"]
        item["availability"] = JSONresponse["availability"]["title"]
        item["level"] = JSONresponse["level"]["title"]
        item["length"] = JSONresponse["length"]
        item["prescribed_effort"] = JSONresponse["effort"]
        item["prerequisites"] = JSONresponse["prerequisites"]
        item["pacing_type"] = JSONresponse["pacing_type"]
#        item["schools"]["title"] = JSONresponse["schools"]["title"]

        schoolList=[]
        item_schools=School()
        for i,schoolObj in enumerate(JSONresponse["schools"]):
            item_schools["title"]=schoolObj["title"]
            item_schools["name"]=schoolObj["name"]
            item_schools["uri"]=schoolObj["uri"]
            item_schools["language"]=schoolObj["language"]
            schoolList.append(dict(item_schools))
        item["schools"]=schoolList

        staffsList=[]
        item_staff=Staff()
        for i,schoolObj in enumerate(JSONresponse["staff"]):
            item_staff['name']=schoolObj['title']
            item_staff['title']=schoolObj['display_position']['title']
            item_staff['org']=schoolObj['display_position']['org']
            item_staff['bio_uri']=schoolObj['uri']
            item_staff['language']=schoolObj['language']
            staffsList.append(dict(item_staff))
        item['staffs']=staffsList


        subjectsList=[]
        item_subject=Subject()
        for i, schoolObj in enumerate(JSONresponse["subjects"]):
            item_subject['title']=schoolObj['title']
            item_subject['uri']=schoolObj['uri']
            item_subject['language']=schoolObj['language']
            subjectsList.append(dict(item_subject))
        item['subjects']=subjectsList

        #item[""] = JSONresponse[""]
        yield item


    #Error Logging
    def errorLog(self,failure):
        #log all failures
        self.logger.error(str(datetime.now()) + " : " + repr(failure))
        with open("./Output/error_crawl.txt", 'a') as f:
            f.write(str(datetime.now()) + " : " + repr(failure) + "\n")


    #---------------main--------------------
    def parse(self, response):
        self.log("\n\n---------- Getting Courses main page : %s -----------\n\n" %response)

        #link to get the course list at start (following url found by checking http calls)
        JSONDataUrl='https://www.edx.org/api/v1/catalog/search?selected_facets[]=content_type_exact%3Acourserun&featured_course_ids=course-v1:Microsoft+DAT101x+2T2017,course-v1:W3Cx+HTML5.0x+1T2017,course-v1:ASUx+ENG101x+2174C,course-v1:Microsoft+DEV236x+1T2017,course-v1:HKUSTx+COMP102.1x+2T2017,course-v1:PennX+ROBO1x+1T2017&featured_programs_uuids=98b7344e-cd44-4a99-9542-09dfdb11d31b,482dee71-e4b9-4b42-a47b-3e16bb69e8f2,865bbad4-6643-4d59-85d3-936cf3a7acf4,a015ce08-a727-46c8-92d1-679b23338bc1,7fdfb297-34f3-425a-9dcd-4a278164754a,8ac6657e-a06a-4a47-aba7-5c86b5811fa1'
        #Forward to the JSON link
        yield scrapy.Request(url=JSONDataUrl,callback=self.getFirstCourseUrls,errback=self.errorLog)