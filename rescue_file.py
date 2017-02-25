
# //////////////////////////////////////////////////////////////
# ////////////////// Not Regular Used Function /////////////////
# //////////////////////////////////////////////////////////////


def rescue_title_to_lower():
    from course_management.models import Course, Subject, Chapter, Topic, ModuleData
    from classes.models import BoardCategory, ClassCategory

    for cls in [BoardCategory, ClassCategory, Course, Subject, Chapter, Topic, ModuleData]:
        for obj in cls:
            obj.title = obj.title.lower()
            obj.save()


def rescue_codename_of_permission():
    from course_management.models import Course, Subject, Chapter, Topic, ModuleData
    from classes.models import BoardCategory, ClassCategory
    perm_list = Permission.objects.filter(name__contains='crud |')
    print_obj = lambda obj: ''
    # Save all title to lower in DB
    # rescue_title_to_lower()

    _count = 0
    error_list = set()
    perm_error_list = list()
    for perm in perm_list:
        name_string = perm.codename
        _branches = name_string.split(' | ')
        # static_branches = [BoardCategory, ClassCategory, Course, Subject, Chapter, Topic, ModuleData]
        topic = None
        len_branches = len(_branches)
        bc = BoardCategory.objects.get(title=_branches[0])
        cc = ClassCategory.objects.get(title=_branches[1], board=bc)
        if len_branches >= 2+1:
            print(perm)
            print('Course .. ', _branches[2])
            try:
                co = Course.objects.get(title=_branches[2], class_category=cc)
            except Exception:
                perm_error_list.append(perm)
                continue

            if len_branches >= 3+1:
                print('Subject .. ', _branches[3])
                sub = Subject.objects.get(title=_branches[3], course=co)
                if len_branches >= 4+1:
                    # print(_branches[4])
                    print('Chapter .. ', _branches[4])
                    chap = Chapter.objects.get(title=_branches[4], subject=sub)
                    if len_branches >= 5+1:
                        try:
                            print('Topic .. ', _branches[5])
                            topic = Topic.objects.get(title=_branches[5], chapter=chap)
                            # print('--------------------------')
                        except Exception as e:
                            print(e.args)
                            # error_list.add(_branches[5])
                            # print('>>><<<<',
                            #       Topic.objects.filter(title__icontains=_branches[5], chapter=chap).count())

                        if len_branches >= 6+1:
                            try:
                                _count += 1
                                print('ModuleData .. ', _branches[6])
                                mod = ModuleData.objects.get(title=_branches[6], topic=topic)
                                print('=====', print_obj(mod))
                            except Exception as e:
                                print(_branches[6])
                                error_list.add(str(topic)+" | "+_branches[6])
                                perm.uuid_codename = ''
                                perm.save()
                        else:
                            _count += 1
                            perm.uuid_codename = topic.get_uuid_name_definition()
                            perm.save()
                    else:
                        perm.uuid_codename = chap.get_uuid_name_definition()
                        perm.save()
                        _count += 1
                else:
                    perm.uuid_codename = sub.get_uuid_name_definition()
                    perm.save()
                    _count += 1
            else:
                perm.uuid_codename = co.get_uuid_name_definition()
                perm.save()
                _count += 1
        else:
            perm.uuid_codename = cc.get_uuid_name_definition()
            perm.save()
            _count += 1
    print(_count, len(perm_list))
    print(error_list, '----', 'effected-per: ---', perm_error_list)

# ///////////////////////////////////-END-//////////////////////////////////
