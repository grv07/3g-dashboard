# //////////////////////////////////////////////////////////////
# ////////////////////////// CONSTANTS /////////////////////////
# //////////////////////////////////////////////////////////////


from classes.models import (BoardCategory, ClassCategory)
from course_management.models import (Course, Topic, Subject, Chapter, ModuleData)

PERMISSION_NAME_FORMAT = ['crud', 'BoardCategory', 'ClassCategory', 'Course',
                          'Subject', 'Chapter', 'Topic', 'ModuleData']

PERMISSION_CODENAME_FORMAT = {'boardcategory': BoardCategory, 'classcategory': ClassCategory,
                              'course': Course, 'subject': Subject, 'chapter': Chapter,
                              'topic': Topic, 'moduledata': ModuleData
                              }
